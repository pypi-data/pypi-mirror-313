import asyncio
import datetime
from typing import Any, Dict, TypeVar
from typing import Union, Optional

import dask.dataframe as dd
import dask_expr
import pandas as pd
from pydantic import BaseModel

from sibi_dst.utils import ParquetSaver, ClickHouseWriter
from sibi_dst.df_helper.core import QueryConfig, ParamsConfig
from sibi_dst.utils import Logger
from .plugins.django import *
from .plugins.http import HttpConfig
from .plugins.parquet import ParquetConfig, ParquetFilterHandler
from .plugins.sql_alchemy import *

# Define a generic type variable for BaseModel subclasses
T = TypeVar("T", bound=BaseModel)

class DfHelper:
    df: Union[dd.DataFrame, pd.DataFrame] = None
    plugin_django_connection: Optional[DjangoConnectionConfig] = None
    plugin_query: Optional[QueryConfig] = None
    plugin_params: Optional[ParamsConfig] = None
    plugin_parquet: Optional[ParquetConfig] = None
    plugin_http: Optional[HttpConfig] = None
    plugin_sqlalchemy: Optional[SqlAlchemyConnectionConfig] = None
    parquet_filename: str = None
    logger: Logger
    default_config: Dict = None

    def __init__(self, source='django_db', **kwargs):
        # Ensure default_config is not shared across instances
        self.default_config = self.default_config or {}
        kwargs = {**self.default_config.copy(), **kwargs}
        self.source = source
        self.logger = Logger.default_logger(logger_name=self.__class__.__name__)
        self.debug = kwargs.setdefault("debug", False)
        self.verbose_debug = kwargs.setdefault("verbose_debug", False)
        self.parquet_storage_path = kwargs.setdefault("parquet_storage_path", None)
        self.dt_field=kwargs.setdefault("dt_field", None)
        self.as_pandas = kwargs.setdefault("as_pandas", False)
        kwargs.setdefault("live", True)
        kwargs.setdefault("logger", self.logger)
        self.post_init(**kwargs)


    def post_init(self, **kwargs):
        self.logger.info(f"Source used: {self.source}")
        self.plugin_query = self.__get_config(QueryConfig, kwargs)
        self.plugin_params = self.__get_config(ParamsConfig, kwargs)
        if self.source == 'django_db':
            self.plugin_django_connection = self.__get_config(DjangoConnectionConfig, kwargs)
        elif self.source == 'parquet':
            self.parquet_filename = kwargs.setdefault("parquet_filename", None)
            self.plugin_parquet = ParquetConfig(**kwargs)
        elif self.source == 'http':
            self.plugin_http = HttpConfig(**kwargs)
        elif self.source == 'sqlalchemy':
            self.plugin_sqlalchemy = self.__get_config(SqlAlchemyConnectionConfig,kwargs)

    @staticmethod
    def __get_config(model: [T], kwargs: Dict[str, Any]) -> Union[T]:
        """
        Initializes a Pydantic model with the keys it recognizes from the kwargs,
        and removes those keys from the kwargs dictionary.
        :param model: The Pydantic model class to initialize.
        :param kwargs: The dictionary of keyword arguments.
        :return: The initialized Pydantic model instance.
        """
        # Extract keys that the model can accept
        recognized_keys = set(model.__annotations__.keys())
        model_kwargs = {k: kwargs.pop(k) for k in list(kwargs.keys()) if k in recognized_keys}
        return model(**model_kwargs)

    def load(self, **options):
        # this will be the universal method to load data from a df irrespective of the source
        df = self._load(**options)
        if self.as_pandas:
            return df.compute()
        return df

    def _load(self, **options):

        if self.source == 'django_db':
            self.plugin_params.parse_params(options)
            return self._load_from_db(**options)
        elif self.source == 'sqlalchemy':
            self.plugin_params.parse_params(options)
            return self._load_from_sqlalchemy(**options)
        elif self.source == 'parquet':
            return self._load_from_parquet(**options)
        elif self.source == 'http':
            if asyncio.get_event_loop().is_running():
                self.logger.info("Running as a task from an event loop")
                return asyncio.create_task(self._load_from_http(**options))
            else:
                self.logger.info("Regular asyncio run...")
                return asyncio.run(self._load_from_http(**options))


    def _load_from_sqlalchemy(self, **options):
        try:
            options.setdefault("debug", self.debug)
            options.setdefault("verbose_debug", self.verbose_debug)
            db_loader = SqlAlchemyLoadFromDb(
                self.plugin_sqlalchemy,
                self.plugin_query,
                self.plugin_params,
                self.logger,
                **options
            )
            self.df = db_loader.build_and_load()
            self._process_loaded_data()
            self._post_process_df()
            self.logger.info("Data successfully loaded from sqlalchemy database.")
        except Exception as e:
            self.logger.error(f"Failed to load data from sqlalchemy database: {e}: options: {options}")
            self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    def _load_from_db(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        try:
            options.setdefault("debug", self.debug)
            options.setdefault("verbose_debug", self.verbose_debug)
            db_loader = DjangoLoadFromDb(
                self.plugin_django_connection,
                self.plugin_query,
                self.plugin_params,
                self.logger,
                **options
            )
            self.df = db_loader.build_and_load()
            self._process_loaded_data()
            self._post_process_df()
            self.logger.info("Data successfully loaded from django database.")
        except Exception as e:
            self.logger.error(f"Failed to load data from django database: {e}")
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    async def _load_from_http(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        """Delegate asynchronous HTTP data loading to HttpDataSource plugin."""
        if not self.plugin_http:
            self.logger.error("HTTP plugin not configured properly.")
            return dd.from_pandas(pd.DataFrame(), npartitions=1)
        try:
            self.df = await self.plugin_http.fetch_data(**options)
        except Exception as e:
            self.logger.error(f"Failed to load data from http plugin: {e}")
            self.df=dd.from_pandas(pd.DataFrame(), npartitions=1)
        return self.df


    def _post_process_df(self):
        """
        Efficiently process the DataFrame by filtering, renaming, and setting indices.
        Optimized for large datasets with Dask compatibility.
        """
        df_params = self.plugin_params.df_params
        fieldnames = df_params.get("fieldnames", None)
        index_col = df_params.get("index_col", None)
        datetime_index = df_params.get("datetime_index", False)
        column_names = df_params.get("column_names", None)

        # Filter columns
        if fieldnames:
            existing_columns = set(self.df.columns)
            valid_fieldnames = list(filter(existing_columns.__contains__, fieldnames))
            self.df = self.df[valid_fieldnames]

        # Rename columns
        if column_names is not None:
            if len(fieldnames) != len(column_names):
                raise ValueError(
                    f"Length mismatch: fieldnames ({len(fieldnames)}) and column_names ({len(column_names)}) must match."
                )
            rename_mapping = dict(zip(fieldnames, column_names))
            self.df = self.df.map_partitions(lambda df: df.rename(columns=rename_mapping))

        # Set index column
        if index_col is not None:
            if index_col in self.df.columns:
                self.df = self.df.set_index(index_col)
            else:
                raise ValueError(f"Index column '{index_col}' not found in DataFrame.")

        # Handle datetime index
        if datetime_index and self.df.index.dtype != 'datetime64[ns]':
            self.df = self.df.map_partitions(lambda df: df.set_index(pd.to_datetime(df.index, errors='coerce')))

        self.logger.info("Post-processing of DataFrame completed.")

    def _process_loaded_data(self):
        self.logger.info(f"Type of self.df: {type(self.df)}")
        if self.df.map_partitions(len).compute().sum() > 0:
            field_map = self.plugin_params.field_map or {}
            if isinstance(field_map, dict):
                rename_mapping = {k: v for k, v in field_map.items() if k in self.df.columns}
                missing_columns = [k for k in field_map.keys() if k not in self.df.columns]

                if missing_columns:
                    self.logger.warning(
                        f"The following columns in field_map are not in the DataFrame: {missing_columns}")

                def rename_columns(df, mapping):
                    return df.rename(columns=mapping)

                if rename_mapping:
                    # Apply renaming
                    self.df = self.df.map_partitions(rename_columns, mapping=rename_mapping)

            self.logger.info("Processing of loaded data completed.")

    def save_to_parquet(self, parquet_filename: Optional[str] = None):
        ps = ParquetSaver(self.df, self.parquet_storage_path, self.logger)
        ps.save_to_parquet(parquet_filename)
        self.logger.info(f"Parquet saved to {parquet_filename} in parquet storage: {self.parquet_storage_path}.")

    def save_to_clickhouse(self, **credentials):
        if self.df.map_partitions(len).compute().sum() == 0:
            self.logger.info("Cannot write to clickhouse since Dataframe is empty")
            return
        cs=ClickHouseWriter(logger=self.logger, **credentials)
        cs.save_to_clickhouse(self.df)
        self.logger.info("Save to ClickHouse completed.")

    def _load_from_parquet(self, **options) -> Union[pd.DataFrame, dd.DataFrame]:
        self.df = self.plugin_parquet.load_files()
        if options:
            self.df = ParquetFilterHandler(logger=self.logger).apply_filters_dask(self.df, options)
        return self.df

    def load_period(self, **kwargs):
        return self.__load_period(**kwargs)

    def __load_period(self, **kwargs):
        dt_field = kwargs.pop("dt_field", self.dt_field)
        if dt_field is None:
            raise ValueError("dt_field must be provided")

        start = kwargs.pop("start", None)
        end = kwargs.pop("end", None)

        # Ensure start and end are provided
        if start is None or end is None:
            raise ValueError("Both 'start' and 'end' must be provided.")

        # Parse string dates
        if isinstance(start, str):
            start = self.parse_date(start)
        if isinstance(end, str):
            end = self.parse_date(end)

        # Validate that start <= end
        if start > end:
            raise ValueError("The 'start' date cannot be later than the 'end' date.")

        # Reverse map to original field name
        field_map = getattr(self.plugin_params, 'field_map', {}) or {}
        reverse_map = {v: k for k, v in field_map.items()}
        mapped_field = reverse_map.get(dt_field, dt_field)

        # Common logic for Django and SQLAlchemy
        if self.source == 'django_db':
            model_fields = {field.name: field for field in self.plugin_django_connection.model._meta.get_fields()}
            if mapped_field not in model_fields:
                raise ValueError(f"Field '{dt_field}' does not exist in the Django model.")
            field_type = type(model_fields[mapped_field]).__name__
            is_date_field = field_type == 'DateField'
            is_datetime_field = field_type == 'DateTimeField'
        elif self.source == 'sqlalchemy':
            model = self.plugin_sqlalchemy.model
            fields = [column.name for column in model.__table__.columns]
            if mapped_field not in fields:
                raise ValueError(f"Field '{dt_field}' does not exist in the SQLAlchemy model.")
            column = getattr(model, mapped_field)
            field_type = str(column.type).upper()
            is_date_field = field_type == 'DATE'
            is_datetime_field = field_type == 'DATETIME'
        else:
            raise ValueError(f"Unsupported source '{self.source}'")
            # Build query filters
        if start == end:
            if is_date_field:
                kwargs[mapped_field] = start
            elif is_datetime_field:
                kwargs[f"{mapped_field}__date"] = start
        else:
            if is_date_field:
                kwargs[f"{mapped_field}__gte"] = start
                kwargs[f"{mapped_field}__lte"] = end
            elif is_datetime_field:
                kwargs[f"{mapped_field}__date__gte"] = start
                kwargs[f"{mapped_field}__date__lte"] = end
        return self.load(**kwargs)


    @staticmethod
    def parse_date(date_str: str) -> Union[datetime.datetime, datetime.date]:
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

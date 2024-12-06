import dask.dataframe as dd
import pandas as pd
from django.db.models import Q

from sibi_dst.df_helper.plugins.django import ReadFrameDask
from sibi_dst.utils import Logger
from sibi_dst.df_helper.core import django_field_conversion_map_dask

class DjangoLoadFromDb:
    df: dd.DataFrame

    def __init__(self, db_connection, db_query, db_params, logger, **kwargs):
        self.connection_config = db_connection
        self.debug = kwargs.pop('debug', False)
        self.verbose_debug = kwargs.pop('verbose_debug', False)
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)
        if self.connection_config.model is None:
            if self.debug:
                self.logger.critical('Model must be specified')
                if self.verbose_debug:
                    print('Model must be specified')
            raise ValueError('Model must be specified')

        self.query_config = db_query
        self.params_config = db_params
        self.params_config.parse_params(kwargs)

    def build_and_load(self):
        self.df = self._build_and_load()
        #self.df = self._convert_columns(self.df)
        return self.df


    def _build_and_load(self) -> dd.DataFrame:
        query = self.connection_config.model.objects.using(self.connection_config.connection_name)
        if not self.params_config.filters:
            # IMPORTANT: if no filters are provided show only the first n_records
            # this is to prevent loading the entire table by mistake
            n_records = self.query_config.n_records if self.query_config.n_records else 100
            queryset=query.all()[:n_records]
        else:
            q_objects = self.__build_query_objects(self.params_config.filters, self.query_config.use_exclude)
            queryset = query.filter(q_objects)
        if queryset is not None:
            try:
                self.df = ReadFrameDask(queryset, **self.params_config.df_params).read_frame()
            except Exception as e:
                self.logger.critical(f'Error loading query: {str(queryset.query)}, error message: {e}')
                self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)
        else:
            self.df = dd.from_pandas(pd.DataFrame(), npartitions=1)

        return self.df

    @staticmethod
    def __build_query_objects(filters: dict, use_exclude: bool):
        q_objects = Q()
        for key, value in filters.items():
            if not use_exclude:
                q_objects.add(Q(**{key: value}), Q.AND)
            else:
                q_objects.add(~Q(**{key: value}), Q.AND)
        return q_objects

    def _convert_columns(self, df: dd.DataFrame) -> dd.DataFrame:
        """
        Convert the data types of columns in a Dask DataFrame based on the field type in the Django model.

        :param df: Dask DataFrame whose columns' data types are to be converted.
        :return: Dask DataFrame with converted column data types.
        """

        def log_debug(message: str, is_verbose: bool = False):
            """Helper to handle debug and verbose debug logging."""
            if self.debug:
                self.logger.debug(message)
                if is_verbose and self.verbose_debug:
                    print(message)

        if self.debug:
            self.logger.info(f'Converting columns: {list(df.columns)}')

        # Get field information from the Django model
        model_fields = self.connection_config.model._meta.get_fields()
        field_type_map = {field.name: type(field).__name__ for field in model_fields}
        # Simplified loop to apply conversions partition-wise
        for field_name, field_type in field_type_map.items():
            if field_name not in df.columns:

                log_debug(f"Column '{field_name}' not found in DataFrame columns.")
                continue

            conversion_func = django_field_conversion_map_dask.get(field_type)
            if not conversion_func:
                message=f"Field type '{field_type}' not found in conversion_map."
                log_debug(message, is_verbose=True)
                continue

            def apply_conversion(partition):
                """
                Apply the conversion function to a single partition for the given column.
                """
                try:
                    if field_name in partition.columns:
                        partition[field_name] = conversion_func(partition[field_name])
                except Exception as e:
                    self.logger.error(f"Error converting column '{field_name}' in partition: {str(e)}")
                return partition

            try:
                # Apply conversion lazily to each partition
                df = df.map_partitions(
                    apply_conversion,
                    meta=df,
                )
                log_debug(f"Successfully queued conversion for column '{field_name}' to type '{field_type}'.",
                          is_verbose=True)
            except Exception as e:
                log_debug(f"Failed to queue conversion for column '{field_name}': {str(e)}", is_verbose=True)

        return df
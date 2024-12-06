import itertools

import dask.dataframe as dd
import pandas as pd
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import sessionmaker

from sibi_dst.df_helper.plugins.sql_alchemy._sqlachemy_filter_handler import SqlAlchemyFilterHandler
from sibi_dst.utils import Logger


class SQLAlchemyDask:
    def __init__(self, model, filters, engine_url, chunk_size=1000, logger=None, verbose=True):
        """
        Initialize with an SQLAlchemy query and database engine URL.

        :param model: SQLAlchemy ORM model.
        :param filters: Filters to apply on the query.
        :param engine_url: Database connection string for SQLAlchemy engine.
        :param chunk_size: Number of records per chunk for Dask partitions.
        :param logger: Logger instance for logging.
        :param verbose: Whether to print detailed logs.
        """
        self.query = None
        self.model = model
        self.filters = filters
        self.chunk_size = chunk_size
        self.verbose = verbose
        self.engine = create_engine(engine_url)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    @staticmethod
    def infer_dtypes_from_model(model):
        """
        Infer data types for Dask DataFrame based on SQLAlchemy ORM model columns.
        """
        mapper = inspect(model)
        sqlalchemy_to_dask_dtype = {
            #'INTEGER': pd.to_numeric(x, errors="coerce"),
            'INTEGER': 'Int64',
            'SMALLINT': 'Int64',
            'BIGINT': 'Int64',
            'FLOAT': 'float64',
            'NUMERIC': 'float64',
            'BOOLEAN': 'bool',
            'VARCHAR': 'object',
            'TEXT': 'object',
            'DATE': 'datetime64[ns]',
            'DATETIME': 'datetime64[ns]',
            'TIME': 'object',
            'UUID': 'object',
        }

        dtypes = {}
        for column in mapper.columns:
            dtype = sqlalchemy_to_dask_dtype.get(str(column.type).upper(), 'object')
            dtypes[column.name] = dtype

        return dtypes

    def read_frame(self, fillna_value=None):
        """
        Load data from an SQLAlchemy query into a Dask DataFrame.

        :param fillna_value: Value to replace NaN or NULL values with, if any.
        :return: Dask DataFrame.
        """
        with self.Session() as session:
            try:
                # Build query
                self.query = select(self.model)
                if self.filters:
                    self.query = SqlAlchemyFilterHandler.apply_filters_sqlalchemy(self.query, self.model, self.filters)
                else:
                    n_records = 100
                    self.query = self.query.limit(n_records)

                # Infer dtypes
                dtypes = self.infer_dtypes_from_model(self.model)
                # Get the column order from the SQLAlchemy model
                ordered_columns = [column.name for column in self.model.__table__.columns]

                # Execute query and fetch results in chunks
                result_proxy = session.execute(self.query)
                results = result_proxy.scalars().all()  # Fetch all rows
                iterator = iter(results)

                partitions = []

                while True:
                    chunk = list(itertools.islice(iterator, self.chunk_size))
                    if not chunk:
                        break

                    # Convert chunk to Pandas DataFrame
                    df = pd.DataFrame.from_records(
                        [row._asdict() if hasattr(row, '_asdict') else row.__dict__ for row in chunk]
                    )
                    # Drop internal SQLAlchemy state if it exists
                    df = df.loc[:, ~df.columns.str.contains('_sa_instance_state')]

                    # Reorder columns to match the model's order
                    df = df[ordered_columns]

                    # Fill NaN values
                    if fillna_value is not None:
                        df = df.fillna(fillna_value)

                    # Convert timezone-aware columns to naive
                    for col in df.columns:
                        if isinstance(df[col].dtype, pd.DatetimeTZDtype):
                            df[col] = df[col].dt.tz_localize(None)

                    # Apply inferred dtypes
                    df = df.astype(dtypes)
                    # Create a Dask partition
                    partitions.append(dd.from_pandas(df, npartitions=1))

                # Concatenate all partitions
                # print(partitions)
                if partitions:
                    dask_df = dd.concat(partitions, axis=0, ignore_index=True)
                else:
                    dask_df = dd.from_pandas(pd.DataFrame(columns=ordered_columns), npartitions=1)

                if self.verbose:
                    self.logger.info(f"Loaded {len(dask_df)} rows into Dask DataFrame.")
                return dask_df

            except Exception as e:
                self.logger.error(f"Error executing query: {str(e)}")
                return dd.from_pandas(pd.DataFrame(columns=ordered_columns), npartitions=1)

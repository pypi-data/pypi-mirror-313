import datetime
from pathlib import Path
from typing import Optional

import dask.dataframe as dd
import fsspec
import pandas as pd
import pyarrow as pa
from sibi_dst.utils import Logger

class ParquetSaver:
    def __init__(self, df_result, parquet_storage_path, logger=None):
        # Ensure df_result is a Dask DataFrame
        if not isinstance(df_result, dd.DataFrame):
            df_result = dd.from_pandas(df_result, npartitions=1)
        self.df_result = df_result
        self.parquet_storage_path = parquet_storage_path
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    def save_to_parquet(self, parquet_filename: Optional[str] = None, clear_existing=True):
        full_path = self._construct_full_path(parquet_filename)

        # We cannot check for empty DataFrame directly with Dask without computation
        # Proceed with saving; if the DataFrame is empty, an empty Parquet file will be created

        # Ensure directory exists and clear if necessary
        self._ensure_directory_exists(full_path, clear_existing=clear_existing)

        # Define schema and save DataFrame to Parquet
        schema = self._define_schema()
        self._convert_dtypes(schema)
        self._save_dataframe_to_parquet(full_path, schema)

    def _define_schema(self) -> pa.Schema:
        """Define a PyArrow schema dynamically based on df_result column types."""
        pandas_dtype_to_pa = {
            'object': pa.string(),
            'string': pa.string(),
            'Int64': pa.int64(),
            'int64': pa.int64(),
            'float64': pa.float64(),
            'float32': pa.float32(),
            'bool': pa.bool_(),
            'boolean': pa.bool_(),  # pandas nullable boolean
            'datetime64[ns]': pa.timestamp('ns'),
            'timedelta[ns]': pa.duration('ns')
        }

        dtypes = self.df_result.dtypes  # No need to call .compute()

        fields = [
            pa.field(col, pandas_dtype_to_pa.get(str(dtype), pa.string()))
            for col, dtype in dtypes.items()
        ]
        return pa.schema(fields)

    def _convert_dtypes(self, schema: pa.Schema):
        """Convert DataFrame columns to match the specified schema."""
        dtype_mapping = {}
        for field in schema:
            col_name = field.name
            if col_name in self.df_result.columns:
                if pa.types.is_string(field.type):
                    dtype_mapping[col_name] = 'string'
                elif pa.types.is_int64(field.type):
                    dtype_mapping[col_name] = 'Int64'  # pandas nullable integer
                elif pa.types.is_float64(field.type):
                    dtype_mapping[col_name] = 'float64'
                elif pa.types.is_float32(field.type):
                    dtype_mapping[col_name] = 'float32'
                elif pa.types.is_boolean(field.type):
                    dtype_mapping[col_name] = 'boolean'  # pandas nullable boolean
                elif pa.types.is_timestamp(field.type):
                    dtype_mapping[col_name] = 'datetime64[ns]'
                else:
                    dtype_mapping[col_name] = 'object'  # Fallback to object
        # Convert dtypes
        self.df_result = self.df_result.astype(dtype_mapping)

    def _construct_full_path(self, parquet_filename: Optional[str]) -> Path:
        """Construct and return the full path for the Parquet file."""
        _, base_path = fsspec.core.url_to_fs(self.parquet_storage_path)
        parquet_filename = parquet_filename or "default.parquet"
        return Path(base_path) / parquet_filename

    @staticmethod
    def _ensure_directory_exists(full_path: Path, clear_existing=False):
        """Ensure that the directory for the path exists, clearing it if specified."""
        fs, _ = fsspec.core.url_to_fs(str(full_path))
        directory = str(full_path.parent)

        if fs.exists(directory):
            if clear_existing:
                fs.rm(directory, recursive=True)
        else:
            fs.mkdirs(directory, exist_ok=True)

    def _save_dataframe_to_parquet(self, full_path: Path, schema: pa.Schema):
        """Save the DataFrame to Parquet using the specified schema."""
        fs, _ = fsspec.core.url_to_fs(str(full_path))
        if fs.exists(str(full_path)):
            fs.rm(str(full_path), recursive=True)

        # Save the Dask DataFrame to Parquet
        self.df_result.to_parquet(
            str(full_path), engine="pyarrow", schema=schema, write_index=False
        )

# import datetime
# from pathlib import Path
# from typing import Optional
#
# import dask.dataframe as dd
# import fsspec
# import pandas as pd
# import pyarrow as pa
# from sibi_dst.utils import Logger
#
# class ParquetSaver:
#     def __init__(self, df_result, parquet_storage_path, logger):
#         self.df_result = df_result
#         self.parquet_storage_path = parquet_storage_path
#         self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)
#
#
#     def save_to_parquet(self, parquet_filename: Optional[str] = None, clear_existing=True):
#         full_path = self._construct_full_path(parquet_filename)
#
#         if len(self.df_result) == 0:
#             self.logger.warning('No data to save')
#             return  # Exit early if there's no data to save
#
#         # Ensure directory exists and clear if necessary
#         self._ensure_directory_exists(full_path, clear_existing=True)
#
#         # Define schema and save DataFrame to parquet
#         schema = self._define_schema()
#         self._convert_dtypes(schema)
#         self._save_dataframe_to_parquet(full_path, schema)
#
#     def _define_schema(self) -> pa.Schema:
#         """Define a PyArrow schema dynamically based on df_result column types."""
#         pandas_dtype_to_pa = {
#             'object': pa.string(),
#             'string': pa.string(),
#             'Int64': pa.int64(),
#             'int64': pa.int64(),
#             'float64': pa.float64(),
#             'bool': pa.bool_(),
#             'boolean': pa.bool_(),  # pandas nullable boolean
#             'datetime64[ns]': pa.timestamp('ns'),
#             'timedelta[ns]': pa.duration('ns')
#         }
#
#         fields = [
#             pa.field(col, pandas_dtype_to_pa.get(str(dtype), pa.string()))
#             for col, dtype in self.df_result.dtypes.items()
#         ]
#         return pa.schema(fields)
#
#     def _convert_dtypes(self, schema: pa.Schema):
#         """Convert DataFrame columns to match the specified schema."""
#         dtype_mapping = {}
#         for field in schema:
#             col_name = field.name
#             if col_name in self.df_result.columns:
#                 if pa.types.is_string(field.type):
#                     dtype_mapping[col_name] = 'string'
#                 elif pa.types.is_int64(field.type):
#                     dtype_mapping[col_name] = 'Int64'  # pandas nullable integer
#                 elif pa.types.is_float64(field.type):
#                     dtype_mapping[col_name] = 'float64'
#                 elif pa.types.is_boolean(field.type):
#                     dtype_mapping[col_name] = 'boolean'  # pandas nullable boolean
#                 elif pa.types.is_timestamp(field.type):
#                     dtype_mapping[col_name] = 'datetime64[ns]'
#                 else:
#                     dtype_mapping[col_name] = 'object'  # Fallback to object
#         self.df_result = self.df_result.astype(dtype_mapping)
#
#     def _construct_full_path(self, parquet_filename: Optional[str]) -> Path:
#         """Construct and return the full path for the parquet file."""
#         fs, base_path = fsspec.core.url_to_fs(self.parquet_storage_path)
#         parquet_filename = parquet_filename or "default.parquet"
#         return Path(base_path) / parquet_filename
#
#     @staticmethod
#     def _ensure_directory_exists(full_path: Path, clear_existing=False):
#         """Ensure that the directory for the path exists, clearing it if specified."""
#         fs, _ = fsspec.core.url_to_fs(str(full_path))
#         directory = str(full_path.parent)
#
#         if fs.exists(directory):
#             if clear_existing:
#                 fs.rm(directory, recursive=True)
#         else:
#             fs.mkdirs(directory, exist_ok=True)
#
#     def _save_dataframe_to_parquet(self, full_path: Path, schema: pa.Schema):
#         """Save the DataFrame to parquet with fsspec using specified schema."""
#         fs, _ = fsspec.core.url_to_fs(str(full_path))
#         if fs.exists(full_path):
#             fs.rm(full_path, recursive=True)
#         if isinstance(self.df_result, dd.DataFrame):
#             self.df_result.to_parquet(
#                 str(full_path), engine="pyarrow", schema=schema, write_index=False
#             )
#         elif isinstance(self.df_result, pd.DataFrame):
#             dd.from_pandas(self.df_result, npartitions=1).to_parquet(
#                 str(full_path), engine="pyarrow", schema=schema, write_index=False
#             )

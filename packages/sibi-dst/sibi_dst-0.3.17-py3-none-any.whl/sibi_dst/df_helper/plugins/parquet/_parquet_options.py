from pathlib import Path
from typing import Optional, List
import dask.dataframe as dd
from pydantic import BaseModel, model_validator, DirectoryPath, FilePath, ConfigDict
import fsspec
import datetime
from sibi_dst.utils import FilePathGenerator
from sibi_dst.utils import Logger

class ParquetConfig(BaseModel):
    load_parquet: bool = False
    parquet_filename: Optional[str] = None
    parquet_storage_path: Optional[DirectoryPath] = None
    parquet_full_path: Optional[FilePath] = None
    parquet_folder_list: Optional[List[str]] = None
    parquet_size_bytes: int = 0
    parquet_max_age_minutes: int = 0
    parquet_is_recent: bool = False
    parquet_start_date: Optional[str] = None
    parquet_end_date: Optional[str] = None
    fs: Optional[fsspec.spec.AbstractFileSystem] = None  # Your fsspec filesystem object
    logger: Optional[Logger] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode='after')
    def check_parquet_params(self):
        # Configure paths based on fsspec
        if self.logger is None:
            self.logger = Logger.default_logger(logger_name=self.__class__.__name__)
        self.fs = fsspec.filesystem("file") if "://" not in str(self.parquet_storage_path) else fsspec.filesystem(str(self.parquet_storage_path).split("://")[0])

        # Validation for parquet path
        if self.parquet_storage_path is None:
            raise ValueError('Parquet storage path must be specified')
        if not self.fs.exists(self.parquet_storage_path):
            raise ValueError('Parquet storage path does not exist')
        self.load_parquet = False
        if self.parquet_filename is not None:
            self.parquet_full_path = self.ensure_file_extension(
                filepath=self.fs.sep.join([str(self.parquet_storage_path), str(self.parquet_filename)]), extension='parquet'
            )
            self.parquet_is_recent = self.is_file_recent()
            self.load_parquet = self.parquet_is_recent and self.fs.exists(self.parquet_full_path)

        if self.parquet_start_date is not None:
            if self.parquet_end_date is None:
                raise ValueError('Parquet end date must be specified if start date is provided')

            start_date = datetime.datetime.strptime(self.parquet_start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(self.parquet_end_date, '%Y-%m-%d')
            if end_date < start_date:
                raise ValueError('Parquet end date must be greater than start date')

            # Saving to parquet is disabled when start and end dates are provided, as we will load parquet files
            self.parquet_folder_list = FilePathGenerator(str(self.parquet_storage_path)).generate_file_paths(start_date, end_date)
            self.parquet_size_bytes = self.get_parquet_size_bytes()
            self.load_parquet = True
            #self.load_parquet = all([self.fs.exists(folder) for folder in self.parquet_folder_list]) and self.parquet_size_bytes > 0
        elif self.parquet_end_date is not None:
            raise ValueError('Parquet start date must be specified if end date is provided')

        return self

    def is_file_recent(self):
        if not self.fs.exists(self.parquet_full_path):
            return False
        if self.parquet_max_age_minutes == 0:
            return True
        file_time = datetime.datetime.fromtimestamp(self.fs.modified(self.parquet_full_path))
        return (datetime.datetime.now() - file_time) <= datetime.timedelta(minutes=self.parquet_max_age_minutes)

    def get_parquet_size_bytes(self):
        total_size = 0
        for folder in self.parquet_folder_list:
            # Use a double wildcard ** to match any level of nested directories
            for path in self.fs.glob(f"{folder}/**/*.parquet"):
                total_size += self.fs.size(path)
        return total_size

    def load_files(self):
        if self.load_parquet:
            if self.parquet_folder_list:
                return dd.read_parquet(self.parquet_folder_list, engine="pyarrow")
            else:
                return dd.read_parquet(self.parquet_full_path, engine="pyarrow")

    @staticmethod
    def ensure_file_extension(filepath: str, extension: str) -> str:
        path = Path(filepath)
        return str(path.with_suffix(f".{extension}")) if path.suffix != f".{extension}" else filepath


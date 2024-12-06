from typing import Optional, Any, Dict
import dask.dataframe as dd
import fsspec
from sibi_dst.df_helper import DfHelper
from sibi_dst.utils import DataWrapper
from sibi_dst.utils import DateUtils


class ParquetArtifact(DfHelper):
    DEFAULT_CONFIG = {
        'source': 'parquet'
    }

    def __init__(self, data_wrapper_class, filesystem_type="file", filesystem_options=None, **kwargs):
        self.config = {
            **self.DEFAULT_CONFIG,
            **kwargs,
        }
        self.df: Optional[dd.DataFrame] = None
        self.data_wrapper_class = data_wrapper_class
        self.date_field = self.config.setdefault('date_field', None)
        if self.date_field is None:
            raise ValueError('date_field must be set')
        self.parquet_storage_path = self.config.setdefault('parquet_storage_path', None)
        if self.parquet_storage_path is None:
            raise ValueError('parquet_storage_path must be set')

        self.parquet_filename = self.config.setdefault('parquet_filename', None)
        if self.parquet_filename is None:
            raise ValueError('parquet_filename must be set')
        self.parquet_start_date = self.config.setdefault('parquet_start_date', None)
        if self.parquet_start_date is None:
            raise ValueError('parquet_start_date must be set')

        self.parquet_end_date = self.config.setdefault('parquet_end_date', None)
        if self.parquet_end_date is None:
            raise ValueError('parquet_end_date must be set')

        # Filesystem setup
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fsspec.filesystem(self.filesystem_type, **self.filesystem_options)

        # Ensure the directory exists
        self.ensure_directory_exists(self.parquet_storage_path)

        super().__init__(**self.config)

    def load(self, **kwargs):
        self.df = super().load(**kwargs)
        return self.df

    def generate_parquet(self, **kwargs) -> None:
        """
        Generate a Parquet file using the configured DataWrapper class.
        """
        params = self._prepare_params(kwargs)
        dw = DataWrapper(self.data_wrapper_class, **params)
        dw.process()

    def update_parquet(self, period: str = 'today', **kwargs) -> None:
        """Update the Parquet file with data from a specific period."""
        kwargs.update(self.parse_parquet_period(period=period))
        self.generate_parquet(**kwargs)

    def rebuild_parquet(self, **kwargs) -> None:
        """Rebuild the Parquet file from the start to end date."""
        kwargs.update(self._get_rebuild_params(kwargs))
        self.generate_parquet(**kwargs)

    def _get_rebuild_params(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare parameters for rebuilding the Parquet file."""
        return {
            'overwrite': True,
            'reverse_order': True,
            'start_date': kwargs.get('parquet_start_date', self.parquet_start_date),
            'end_date': kwargs.get('parquet_end_date', self.parquet_end_date),
        }

    def _prepare_params(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the parameters for generating the Parquet file."""
        return {
            'class_params': kwargs.pop('class_params', None),
            'date_field': kwargs.pop('date_field', self.date_field),
            'data_path': self.parquet_storage_path,
            'parquet_filename': kwargs.pop('parquet_filename', self.parquet_filename),
            'start_date': kwargs.pop('parquet_start_date', self.parquet_start_date),
            'end_date': kwargs.pop('parquet_end_date', self.parquet_end_date),
            'verbose': kwargs.pop('verbose', False),
            'load_params': kwargs.pop('load_params', None),
            'reverse_order': kwargs.pop('reverse_order', True),
            'overwrite': kwargs.pop('overwrite', False),
            'ignore_missing': kwargs.pop('ignore_missing', False),
            'logger': self.logger,
            'history_days_threshold': kwargs.pop('history_days_threshold', 30),
            'max_age_minutes': kwargs.pop('max_age_minutes', 10),
            'show_progress': kwargs.pop('show_progress', False),
            'filesystem_type': self.filesystem_type,
            'filesystem_options': self.filesystem_options,
        }

    @staticmethod
    def parse_parquet_period(**kwargs):
        start_date, end_date = DateUtils.parse_period(**kwargs)
        return {
            'parquet_start_date': start_date.strftime('%Y-%m-%d'),
            'parquet_end_date': end_date.strftime('%Y-%m-%d'),
        }
    def ensure_directory_exists(self, path: str) -> None:
        """Ensure the directory exists in the specified filesystem."""
        try:
            self.fs.makedirs(path, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Error creating directory {path} in filesystem {self.filesystem_type}: {e}")
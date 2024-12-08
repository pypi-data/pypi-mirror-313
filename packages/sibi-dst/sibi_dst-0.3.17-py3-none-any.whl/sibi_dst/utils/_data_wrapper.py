import datetime
from typing import Type, Any, Dict, Optional

import fsspec
import pandas as pd
from IPython.display import display
from tqdm import tqdm

from sibi_dst.utils import Logger
from sibi_dst.utils import ParquetSaver


class DataWrapper:
    DEFAULT_MAX_AGE_MINUTES = 1440
    DEFAULT_HISTORY_DAYS_THRESHOLD = 30

    def __init__(self,
                 dataclass: Type,
                 date_field: str,
                 data_path: str,
                 parquet_filename: str,
                 start_date: Any,
                 end_date: Any,
                 filesystem_type: str = "file",
                 filesystem_options: Optional[Dict] = None,
                 verbose: bool = False,
                 class_params: Optional[Dict] = None,
                 load_params: Optional[Dict] = None,
                 reverse_order: bool = False,
                 overwrite: bool = False,
                 ignore_missing: bool = False,
                 logger: Optional[Logger] = None,
                 max_age_minutes: int = DEFAULT_MAX_AGE_MINUTES,
                 history_days_threshold: int = DEFAULT_HISTORY_DAYS_THRESHOLD,
                 show_progress: bool = False):
        self.dataclass = dataclass
        self.date_field = date_field
        self.data_path = self.ensure_forward_slash(data_path)
        self.parquet_filename = parquet_filename
        self.filesystem_type = filesystem_type
        self.filesystem_options = filesystem_options or {}
        self.fs = fsspec.filesystem(filesystem_type, **self.filesystem_options)
        self.verbose = verbose
        self.class_params = class_params or {}
        self.load_params = load_params or {}
        self.reverse_order = reverse_order
        self.overwrite = overwrite
        self.ignore_missing = ignore_missing
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)
        self.max_age_minutes = max_age_minutes
        self.history_days_threshold = history_days_threshold
        self.show_progress = show_progress

        self.start_date = self.convert_to_date(start_date)
        self.end_date = self.convert_to_date(end_date)

    @staticmethod
    def convert_to_date(date: Any) -> datetime.date:
        if isinstance(date, datetime.date):
            return date
        try:
            return pd.to_datetime(date).date()
        except ValueError as e:
            raise ValueError(f"Error converting {date} to datetime: {e}")

    @staticmethod
    def ensure_forward_slash(path: str) -> str:
        return path if path.endswith('/') else path + '/'

    def generate_date_range(self):
        """Generate a range of dates between start_date and end_date."""
        date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        if self.reverse_order:
            date_range = date_range[::-1]
        for date in date_range:
            yield date.date()

    def process(self):
        """Execute the update plan following the specified hierarchy."""
        update_plan_table = self.generate_update_plan_with_conditions()

        # Display the update plan table to the user if show_progress is True
        if self.show_progress:
            display(update_plan_table)

        # Process files according to the hierarchy, considering only `update_required` dates
        for category, description in [
            ("overwrite", "Processing files due to overwrite=True"),
            ("history_days", "Processing files within history_days_threshold"),
            ("missing_files", "Processing missing files")
        ]:
            # Filter dates in the category where `update_required` is True
            dates_to_process = update_plan_table[
                (update_plan_table["update_category"] == category) & (update_plan_table["update_required"])
            ]["date"].tolist()

            date_iterator = dates_to_process
            if self.show_progress:
                date_iterator = tqdm(date_iterator, desc=description, unit="date")

            for current_date in date_iterator:
                self.process_date(current_date)

    def is_file_older_than(self, file_path: str) -> bool:
        """
        Check if a file is older than the specified max_age_minutes.
        """
        try:
            info = self.fs.info(file_path)
            file_modification_time = info['mtime']
            file_modification_datetime = datetime.datetime.fromtimestamp(
                file_modification_time, tz=datetime.timezone.utc
            )
            current_time = datetime.datetime.now(datetime.timezone.utc)
            file_age_minutes = (current_time - file_modification_datetime).total_seconds() / 60

            if self.verbose:
                self.logger.debug(
                    f"File {file_path} is {round(file_age_minutes, 2)} minutes old "
                    f"(threshold: {self.max_age_minutes} minutes)"
                )

            return file_age_minutes > self.max_age_minutes
        except FileNotFoundError:
            return True  # Treat missing files as old

    def process_date(self, date: datetime.date):
        """Process a specific date by regenerating data as necessary."""
        folder = f'{self.data_path}{date.year}/{date.month:02d}/{date.day:02d}/'
        full_parquet_filename = f"{folder}{self.parquet_filename}"

        start_time = datetime.datetime.now()

        if self.verbose:
            self.logger.debug(f"Processing {full_parquet_filename}...")

        data_object = self.dataclass(**self.class_params)
        df = data_object.load_period(dt_field=self.date_field, start=date, end=date)

        if len(df.index)==0:
            if self.verbose:
                self.logger.debug("No data found for the specified date.")
            return

        parquet_saver = ParquetSaver(df, folder, self.logger)
        parquet_saver.save_to_parquet(self.parquet_filename, clear_existing=True)

        end_time = datetime.datetime.now()
        duration_seconds = (end_time - start_time).total_seconds()

        if self.verbose:
            self.logger.debug(
                f"Data saved to {full_parquet_filename}. Processing time: {duration_seconds:.2f} seconds"
            )

    def generate_update_plan_with_conditions(self):
        """
        Generate an update plan that evaluates files based on the specified hierarchy:
        1. Overwrite (all files regenerated).
        2. History threshold: Files within `history_days_threshold` are evaluated for `max_age_minutes`.
        3. Missing files: Detect missing files, ignoring future dates.
        """
        rows = []

        today = datetime.date.today()
        history_start_date = today - datetime.timedelta(days=self.history_days_threshold)

        date_range = self.generate_date_range()
        if self.show_progress:
            date_range = tqdm(date_range, desc=f"Evaluating update plan {self.__class__.__name__}", unit="date")

        for current_date in date_range:
            folder = f'{self.data_path}{current_date.year}/{current_date.month:02d}/{current_date.day:02d}/'
            full_parquet_filename = f"{folder}{self.parquet_filename}"

            file_exists = self.fs.exists(full_parquet_filename)
            within_history = history_start_date <= current_date <= today
            missing_file = not file_exists and not self.ignore_missing
            category = None

            # Hierarchy 1: Overwrite
            if self.overwrite:
                category = "overwrite"
                update_required = True
            # Hierarchy 2: History threshold evaluation
            elif within_history:
                if self.is_file_older_than(full_parquet_filename):
                    category = "history_days"
                    update_required = True
                else:
                    update_required = False
            # Hierarchy 3: Missing files
            elif missing_file and current_date <= today:
                category = "missing_files"
                update_required = True
            else:
                update_required = False

            # Collect condition descriptions for the update plan table
            rows.append({
                "date": current_date,
                "file_exists": file_exists,
                "within_history": within_history,
                "missing_file": missing_file,
                "update_required": update_required,
                "update_category": category
            })

        update_plan_table = pd.DataFrame(rows)
        return update_plan_table



# # Usage:
# # wrapper = DataWrapper(
# #     dataclass=YourDataClass,
# #     date_field="created_at",
# #     data_path="/path/to/data",
# #     parquet_filename="data.parquet",
# #     start_date="2022-01-01",
# #     end_date="2022-12-31",
# #     filesystem_type="file",
# #     verbose=True
# # )
# # wrapper.process()
# # wrapper = DataWrapper(
# #    dataclass=YourDataClass,
# #    date_field="created_at",
# #    data_path="s3://your-bucket-name/path/to/data",
# #    parquet_filename="data.parquet",
# #    start_date="2022-01-01",
# #    end_date="2022-12-31",
# #    filesystem_type="s3",
# #    filesystem_options={
# #        "key": "your_aws_access_key",
# #        "secret": "your_aws_secret_key",
# #        "client_kwargs": {"endpoint_url": "https://s3.amazonaws.com"}
# #    },
# #    verbose=True
# #)
# #wrapper.process()

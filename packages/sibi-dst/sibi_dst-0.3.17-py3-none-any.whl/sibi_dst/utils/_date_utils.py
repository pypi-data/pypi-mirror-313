import datetime
from typing import Union, Tuple, Callable, Dict, Any

import numpy as np
import pandas as pd
from sibi_dst.utils import Logger


class DateUtils:
    _PERIOD_FUNCTIONS: Dict[str, Callable[[], Tuple[datetime.date, datetime.date]]] = {}

    def __init__(self, logger=None):
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    @classmethod
    def _ensure_date(cls, value: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Ensure the input is converted to a datetime.date object.
        """
        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, pd.Timestamp):
            return value.to_pydatetime().date()
        elif isinstance(value, str):
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    return datetime.datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Unsupported date format: {value}")

    @classmethod
    def calc_week_range(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> Tuple[datetime.date, datetime.date]:
        """
        Calculate the start and end of the week for a given reference date.
        """
        reference_date = cls._ensure_date(reference_date)
        start = reference_date - datetime.timedelta(days=reference_date.weekday())
        end = start + datetime.timedelta(days=6)
        return start, end

    @staticmethod
    def get_year_timerange(year: int) -> Tuple[datetime.date, datetime.date]:
        """
        Get the start and end dates for a given year.
        """
        return datetime.date(year, 1, 1), datetime.date(year, 12, 31)

    @classmethod
    def get_first_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the first day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        return datetime.date(reference_date.year, 3 * quarter - 2, 1)

    @classmethod
    def get_last_day_of_the_quarter(cls, reference_date: Union[str, datetime.date, datetime.datetime, pd.Timestamp]) -> datetime.date:
        """
        Get the last day of the quarter for a given date.
        """
        reference_date = cls._ensure_date(reference_date)
        quarter = (reference_date.month - 1) // 3 + 1
        first_day_of_next_quarter = datetime.date(reference_date.year, 3 * quarter + 1, 1)
        return first_day_of_next_quarter - datetime.timedelta(days=1)

    @classmethod
    def get_month_range(cls, n: int = 0) -> Tuple[datetime.date, datetime.date]:
        """
        Get the date range for the current month or the month `n` months in the past or future.
        """
        today = datetime.date.today()
        target_month = (today.month - 1 + n) % 12 + 1
        target_year = today.year + (today.month - 1 + n) // 12
        start = datetime.date(target_year, target_month, 1)
        if n == 0:
            return start, today
        next_month = (target_month % 12) + 1
        next_year = target_year + (target_month == 12)
        end = datetime.date(next_year, next_month, 1) - datetime.timedelta(days=1)
        return start, end

    @classmethod
    def register_period(cls, name: str, func: Callable[[], Tuple[datetime.date, datetime.date]]):
        """
        Dynamically register a new period function.
        """
        cls._PERIOD_FUNCTIONS[name] = func

    @classmethod
    def parse_period(cls, **kwargs) -> Tuple[datetime.date, datetime.date]:
        """
        Parse the period keyword to determine the start and end date for date range operations.
        """
        period = kwargs.setdefault('period', 'today')
        period_functions = cls._get_default_periods()
        period_functions.update(cls._PERIOD_FUNCTIONS)
        if period not in period_functions:
            raise ValueError(f"Unknown period '{period}'. Available periods: {list(period_functions.keys())}")
        return period_functions[period]()

    @classmethod
    def _get_default_periods(cls) -> Dict[str, Callable[[], Tuple[datetime.date, datetime.date]]]:
        """
        Get default period functions.
        """
        today = datetime.date.today
        return {
            'today': lambda: (today(), today()),
            'yesterday': lambda: (today() - datetime.timedelta(days=1), today() - datetime.timedelta(days=1)),
            'current_week': lambda: cls.calc_week_range(today()),
            'last_week': lambda: cls.calc_week_range(today() - datetime.timedelta(days=7)),
            'current_month': lambda: cls.get_month_range(n=0),
            'last_month': lambda: cls.get_month_range(n=-1),
            'current_year': lambda: cls.get_year_timerange(today().year),
            'current_quarter': lambda: (cls.get_first_day_of_the_quarter(today()), cls.get_last_day_of_the_quarter(today())),
            'ytd': lambda: (datetime.date(today().year, 1, 1), today()),
        }

class BusinessDays:
    def __init__(self, holiday_list, logger):
        """
        Initialize a BusinessDays object with a given holiday list.
        """
        self.logger = logger
        self.HOLIDAY_LIST = holiday_list
        bd_holidays = [day for year in self.HOLIDAY_LIST for day in self.HOLIDAY_LIST[year]]
        self.bd_cal = np.busdaycalendar(holidays=bd_holidays, weekmask="1111100")
        self.holidays = self.bd_cal.holidays
        self.week_mask = self.bd_cal.weekmask

    def get_business_days_count(self, begin_date, end_date):
        """
        Calculate the number of business days between two dates.
        """
        try:
            begin_date = pd.to_datetime(begin_date)
            end_date = pd.to_datetime(end_date)
        except Exception as e:
            raise ValueError(f"Invalid date format: {e}")

        years = [str(year) for year in range(begin_date.year, end_date.year + 1)]
        if not all(year in self.HOLIDAY_LIST for year in years):
            raise ValueError("Not all years in date range are in the holiday list")

        return np.busday_count(
            begin_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            busdaycal=self.bd_cal,
        )

    def calc_business_days_from_df(self, df, begin_date_col, end_date_col, result_col="business_days"):
        """
        Add a column to a Dask DataFrame with the number of business days between two date columns.
        """
        if not all(col in df.columns for col in [begin_date_col, end_date_col]):
            self.logger.error("Column names not found in DataFrame")
            raise ValueError("Required columns are missing")

        # Extract holidays and weekmask to recreate the busdaycalendar
        holidays = self.bd_cal.holidays
        weekmask = self.bd_cal.weekmask

        # Define a function to calculate business days
        def calculate_business_days(row, holidays, weekmask):
            begin_date = pd.to_datetime(row[begin_date_col])
            end_date = pd.to_datetime(row[end_date_col])
            busdaycal = np.busdaycalendar(holidays=holidays, weekmask=weekmask)
            return np.busday_count(
                begin_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                busdaycal=busdaycal,
            )

        # Define a wrapper function for partition-wise operations
        def apply_business_days(partition, holidays, weekmask):
            return partition.apply(
                calculate_business_days, axis=1, holidays=holidays, weekmask=weekmask
            )

        # Apply the function using map_partitions
        df[result_col] = df.map_partitions(
            apply_business_days,
            holidays,
            weekmask,
            meta=(result_col, "int64"),
        )

        return df

    def add_business_days(self, start_date, n_days):
        """
        Add n_days business days to start_date.
        """
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date should be a string in the format YYYY-MM-DD")

        if str(start_date.year) not in self.HOLIDAY_LIST:
            self.logger.warning(f"Year {start_date.year} is not in the holiday list")

        return np.busday_offset(
            start_date.strftime("%Y-%m-%d"),
            n_days,
            roll="forward",
            busdaycal=self.bd_cal,
        )

    def calc_sla_end_date(self, df, start_date_col, n_days_col, result_col="sla_end_date"):
        """
        Add a column to a Dask DataFrame with SLA end dates based on start date and SLA days.
        """
        if not all(col in df.columns for col in [start_date_col, n_days_col]):
            raise ValueError("Column names not found in DataFrame")

        # Extract holidays and weekmask to recreate the busdaycalendar
        holidays = self.bd_cal.holidays
        weekmask = self.bd_cal.weekmask

        # Define a function to calculate SLA end dates
        def calculate_sla_end_date(row, holidays, weekmask):
            start_date = pd.to_datetime(row[start_date_col])
            n_days = row[n_days_col]
            busdaycal = np.busdaycalendar(holidays=holidays, weekmask=weekmask)
            return np.busday_offset(
                start_date.strftime("%Y-%m-%d"),
                n_days,
                roll="forward",
                busdaycal=busdaycal,
            )

        # Define a wrapper for partition-wise operation
        def apply_sla_end_date(partition, holidays, weekmask):
            return partition.apply(
                calculate_sla_end_date, axis=1, holidays=holidays, weekmask=weekmask
            )

        # Apply the function using map_partitions
        df[result_col] = df.map_partitions(
            apply_sla_end_date,
            holidays,
            weekmask,
            meta=(result_col, "object"),
        )

        return df
# Class enhancements
# DateUtils.register_period('next_week', lambda: (datetime.date.today() + datetime.timedelta(days=7),
#                                                 datetime.date.today() + datetime.timedelta(days=13)))
# start, end = DateUtils.parse_period(period='next_week')
# print(f"Next Week: {start} to {end}")

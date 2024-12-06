import pandas as pd
import dask.dataframe as dd
from sibi_dst.utils import Logger

class DataUtils:

    def __init__(self, logger=None):
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    def transform_numeric_cols(self, df, columns, fill_value=0, dtype=int):
        if not columns:
            self.logger.warning('No columns specified')

        columns = [column for column in columns if column in df.columns]
        for col in columns:
            if isinstance(df, dd.DataFrame):
                # Replace NaN with 0, then convert to boolean
                df[col] = df[col].map_partitions(
                    lambda s: pd.to_numeric(s, errors='coerce')  # Convert to numeric, invalid to NaN
                    .fillna(fill_value)  # Replace NaN with 0
                    .astype(dtype),
                    meta=(col, dtype)
                )
            else:
                # For Pandas DataFrame, handle mixed types and invalid values
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, invalid to NaN
                df[col] = df[col].fillna(fill_value).astype(dtype)

        return df

    @staticmethod
    def transform_numeric_columns(df, columns=None, fill_value=0, transform_func=None):
        """
        Transform numeric columns in a DataFrame (Pandas or Dask), handling missing values and applying optional transformations.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - columns (list of str, optional): Specific columns to transform. If None, all numeric columns are transformed.
        - fill_value (int or float): The value to replace NA values with.
        - transform_func (callable, optional): The transformation function to apply.
          If None, no additional transformation is applied.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with transformed numeric columns.
        """
        if columns is None:
            # Detect numeric columns
            columns = df.select_dtypes(include=['number']).columns.tolist()

        if not columns:
            return df

        columns = [column for column in columns if column in df.columns]
        # Default transformation function (identity) if none is provided
        if transform_func is None:
            transform_func = lambda x: x

        # Batch processing for Dask
        if isinstance(df, dd.DataFrame):
            def transform_partition(partition):
                # Apply transformations for all numeric columns in a single pass
                partition[columns] = partition[columns].fillna(fill_value).map(transform_func)
                return partition

            # Apply the transformation function to all specified columns
            df = df.map_partitions(transform_partition, meta=df)
        else:
            # Pandas: Vectorized operations for all specified columns
            df[columns] = df[columns].fillna(fill_value).map(transform_func)

        return df

    @staticmethod
    def transform_boolean_columns(df, columns=None):
        """
        Detect if the provided columns in a DataFrame (Pandas or Dask) contain only 0 and 1
        and convert them to boolean. Detection is performed using a sample.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - columns (list of str): List of columns to check and transform.
        - sample_size (int): Number of rows to sample for detection. Ignored for Pandas DataFrames.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with transformed boolean columns.
        """
        # Apply transformation to each specified column
        for col in columns:
            if col in df.columns:
                if isinstance(df, dd.DataFrame):
                    # Replace NaN with 0, then convert to boolean
                    df[col] = df[col].map_partitions(
                        lambda s: pd.to_numeric(s, errors='coerce')  # Convert to numeric, invalid to NaN
                        .fillna(0)  # Replace NaN with 0
                        .astype(int)  # Ensure integer type
                        .astype(bool),  # Convert to boolean
                        meta=(col, 'bool')
                    )
                else:
                    # For Pandas DataFrame, handle mixed types and invalid values
                    df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric, invalid to NaN
                    df[col] = df[col].fillna(0).astype(int).astype(bool)

        return df

    def merge_lookup_data(self, classname, df, **kwargs):
        """
        Merge lookup data into the DataFrame based on specified columns.

        Parameters:
        - classname: The class instance to use for loading lookup data.
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.
        - kwargs: Additional keyword arguments for configuration.

        Returns:
        - pandas.DataFrame or dask.dataframe.DataFrame: Updated DataFrame with merged lookup data.
        """
        # Return early if the DataFrame is empty
        if self.is_dataframe_empty(df):
            return df

        # Extract and validate required parameters
        required_params = ['source_col', 'lookup_col', 'lookup_description_col', 'source_description_alias']
        missing_params = [param for param in required_params if param not in kwargs]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

        source_col = kwargs.pop('source_col')
        lookup_col = kwargs.pop('lookup_col')
        lookup_description_col = kwargs.pop('lookup_description_col')
        source_description_alias = kwargs.pop('source_description_alias')

        # Optional parameters with default values
        fillna_source_description_alias = kwargs.pop('fillna_source_description_alias', False)
        fieldnames = kwargs.pop('fieldnames', (lookup_col, lookup_description_col))
        column_names = kwargs.pop('column_names', ['temp_join_col', source_description_alias])

        if source_col not in df.columns:
            self.logger.info(f"{source_col} not in DataFrame columns")
            return df

        # Get unique IDs from source column
        ids = df[source_col].dropna().unique()
        if isinstance(ids, dd.Series):
            ids = ids.compute()
        if not len(ids):
            self.logger.info(f"No IDs found in the source column: {source_col}")
            return df
        ids = sorted(ids.tolist())
        # Prepare kwargs for loading lookup data
        load_kwargs = kwargs.copy()
        load_kwargs.update({
            'fieldnames': fieldnames,
            'column_names': column_names,
            f'{lookup_col}__in': ids
        })
        # Load lookup data
        lookup_instance = classname(debug=True, verbose_debug=True)
        result = lookup_instance.load(**load_kwargs)
        if len(result.index) == 0:
            self.logger.info(f"No IDs found in the source column: {source_col}")
            return df
        # Determine the join column on the result DataFrame
        temp_join_col = 'temp_join_col' if 'temp_join_col' in column_names else lookup_col

        # Merge DataFrames
        df = df.merge(result, how='left', left_on=source_col, right_on=temp_join_col)

        if fillna_source_description_alias and source_description_alias in df.columns:
            df[source_description_alias]=df[source_description_alias].fillna('')

        # Drop temp_join_col if present
        df = df.drop(columns='temp_join_col', errors='ignore')

        return df


    def is_dataframe_empty(self, df):
        """
        Check if a DataFrame (Pandas or Dask) is empty.

        Parameters:
        - df (pandas.DataFrame or dask.dataframe.DataFrame): The DataFrame.

        Returns:
        - bool: True if the DataFrame is empty, False otherwise.
        """
        if isinstance(df, dd.DataFrame):
            try:
                return len(df.index) == 0
            except Exception as e:
                self.logger.error(f"Error while processing Dask DataFrame: {e}")
                return False
        elif isinstance(df, pd.DataFrame):
            return df.empty
        else:
            self.logger.error("Input must be a pandas or dask DataFrame.")
            return False

    @staticmethod
    def convert_to_datetime_dask(df, date_fields):
        """
        Convert specified columns in a Dask DataFrame to datetime, handling errors gracefully.

        Parameters:
        - df (dask.dataframe.DataFrame): The Dask DataFrame containing the columns.
        - date_fields (list of str): List of column names to convert to datetime.

        Returns:
        - dask.dataframe.DataFrame: Updated DataFrame with specified columns converted to datetime.
        """
        for col in date_fields:
            if col in df.columns:
                df[col] = df[col].map_partitions(pd.to_datetime, errors="coerce", meta=(col, "datetime64[ns]"))
        return df

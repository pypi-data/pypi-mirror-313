import dask.dataframe as dd
from sqlmodel import Session, select, text
from typing import Any, Dict, Optional
import logging
import pandas as pd

class SQLModelLoadFromDb:
    df: dd.DataFrame

    def __init__(
        self,
        db_connection,
        db_query: Optional[Dict[str, Any]] = None,
        db_params: Optional[Dict[str, Any]] = None,
        logger=None,
        **kwargs,
    ):
        """
        Initialize the loader with database connection, query, and parameters.
        """
        self.db_connection = db_connection
        self.table_name = self.db_connection.table
        self.model = self.db_connection.model
        self.engine = self.db_connection.engine
        self.logger = logger or self._default_logger()
        self.query_config = db_query or {}
        self.params_config = db_params or {}
        self.debug = kwargs.pop("debug", False)
        self.verbose_debug = kwargs.pop("verbose_debug", False)

    def _default_logger(self):
        """Create a default logger."""
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger("SQLModelLoadFromDb")

    def build_and_load(self) -> dd.DataFrame:
        """
        Load data into a Dask DataFrame based on the query and parameters.
        """
        self.df = self._build_and_load()
        if not self.df.empty:
            self._process_loaded_data()
        return self.df

    def _build_and_load(self) -> dd.DataFrame:
        """
        Query the database and load results into a Dask DataFrame.
        """
        print(self.model.__name__)
        with Session(self.engine) as session:
            try:
                query = select(text(self.model.__table__))
                print("query:", query)

                # Apply filters if provided
                filters = self.params_config.df_params.get("filters")
                if filters:
                    # Apply ORM filters (simple equality conditions)
                    for column_name, value in filters.items():
                        column = getattr(self.model, column_name, None)
                        if column is not None:
                            query = query.filter(column == value)
                        else:
                            self.logger.warning(f"Filter column '{column_name}' not found in model.")

                # Apply limit if provided in query_config
                n_records = self.query_config.n_records
                if n_records:
                    query = query.limit(n_records)

                # Debug: Log the SQL query
                self.logger.info(f"Executing query: {str(query)}")

                # Execute the query
                results = session.exec(query).fetchall()

                # Convert query results to a Dask DataFrame
                print("results:",results)
                if results:
                    df = dd.from_pandas(pd.DataFrame([r.dict() for r in results]), npartitions=1)
                else:
                    self.logger.warning("Query returned no results.")
                    df = dd.from_pandas(pd.DataFrame(), npartitions=1)

            except Exception as e:
                print(e)
                self.logger.error(f"Error loading data: {e}")
                df = dd.from_pandas(pd.DataFrame(), npartitions=1)

        return df

    def _process_loaded_data(self):
        """
        Process and clean the loaded data.
        """
        field_map = self.params_config.get("field_map", {})
        if field_map:
            rename_mapping = {k: v for k, v in field_map.items() if k in self.df.columns}
            if rename_mapping:
                self.df = self.df.rename(columns=rename_mapping, meta={v: "object" for v in rename_mapping.values()})
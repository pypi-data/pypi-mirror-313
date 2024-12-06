import dask.dataframe as dd
import pandas as pd

from sibi_dst.df_helper.core import ParamsConfig, QueryConfig
from sibi_dst.utils import Logger
from ._io_sqlalchemy_dask import SQLAlchemyDask
from ._sqlalchemy_db_connection import SqlAlchemyConnectionConfig

class SqlAlchemyLoadFromDb:
    df: dd.DataFrame = None

    def __init__(
            self,
            plugin_sqlalchemy: SqlAlchemyConnectionConfig,  # Expected to be an instance of SqlAlchemyConnection
            plugin_query: QueryConfig = None,
            plugin_params: ParamsConfig = None,
            logger: Logger = None,
            **kwargs,
    ):
        """
        Initialize the loader with database connection, query, and parameters.
        """
        self.db_connection = plugin_sqlalchemy
        self.table_name = self.db_connection.table
        self.model = self.db_connection.model
        self.engine = self.db_connection.engine
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)
        self.query_config = plugin_query
        self.params_config = plugin_params
        self.debug = kwargs.pop("debug", False)
        self.verbose_debug = kwargs.pop("verbose_debug", False)

    def build_and_load(self) -> dd.DataFrame:
        """
        Load data into a Dask DataFrame based on the query and parameters.
        """
        self._build_and_load()
        return self.df

    def _build_and_load(self) -> dd.DataFrame:

        try:
            # reader = SQLAlchemyDask(model=self.model, filters=self.params_config.filters,engine_url=self.engine.url, logger=self.logger, chunk_size=1000, debug=self.debug)
            self.df = SQLAlchemyDask(
                model=self.model,
                filters=self.params_config.filters,
                engine_url=self.engine.url,
                logger=self.logger,
                chunk_size=1000,
                debug=self.debug).read_frame()
            if self.df is None or len(self.df.head().index) == 0:
                self.logger.warning("Query returned no results.")
                return dd.from_pandas(pd.DataFrame(), npartitions=1)

            return self.df
        except Exception as e:
            self.logger.error(f"Failed to load data into Dask DataFrame.{e}")
            return dd.from_pandas(pd.DataFrame(), npartitions=1)

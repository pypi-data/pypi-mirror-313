from pydantic import BaseModel, HttpUrl, Field, ConfigDict, SecretStr
from typing import Dict, Optional, Any
import httpx
import dask.dataframe as dd
import pandas as pd
from sibi_dst.utils import Logger

class HttpConfig(BaseModel):
    base_url: HttpUrl
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)
    logger: Optional[Logger] = None
    timeout: Optional[int] = 300
    api_key: Optional[SecretStr] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, logger=None, **data):
        super().__init__(**data)
        # Initialize the logger if not provided
        self.logger = logger or Logger.default_logger(logger_name=self.__class__.__name__)

    async def fetch_data(self, **options) -> dd.DataFrame:
        """Asynchronously fetch JSON data from HTTP endpoint, substituting options into the URL path."""
        try:
            # Build URL with options as path segments

            if options:
                formatted_url = str(self.base_url).rstrip("/")
                formatted_url += "/" + "/".join(str(value) for value in options.values()) + "/"
            else:
                formatted_url = str(self.base_url)
                # Set up headers with API key if provided
            headers = {"Authorization": f"Bearer {self.api_key.get_secret_value()}"} if self.api_key else {}

            self.logger.debug(f"Fetching data from {formatted_url} with params {self.params}")
            async with httpx.AsyncClient() as client:
                response = await client.get(formatted_url, params=self.params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()
                df = dd.from_pandas(pd.json_normalize(data), npartitions=1)
                self.logger.debug("Data successfully loaded from HTTP JSON source.")
                return df
        except httpx.RequestError as e:
            self.logger.debug(f"HTTP request error: {e}")
            raise
        except ValueError as e:
            self.logger.debug(f"Error parsing JSON data: {e}")
            raise
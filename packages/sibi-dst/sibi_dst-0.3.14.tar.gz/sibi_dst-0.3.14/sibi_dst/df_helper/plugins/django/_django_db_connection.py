from typing import Any, Dict, Union

from pydantic import BaseModel, model_validator

from ._django_sql_model_builder import DjangoSqlModelBuilder


class DjangoConnectionConfig(BaseModel):
    live: bool = False
    connection_name: str = None
    table: str = None
    model: Any = None

    @model_validator(mode="after")
    def check_model(self):
        # connection_name is mandatory
        if self.connection_name is None:
            raise ValueError("Connection name must be specified")

        # If table is provided, enforce live=False
        if self.table:
            self.live = False

        # If model is not provided, build it dynamically
        if not self.model:
            if not self.table:
                raise ValueError("Table name must be specified to build the model")
            try:
                self.model = DjangoSqlModelBuilder(
                    connection_name=self.connection_name, table=self.table
                ).build_model()
            except Exception as e:
                raise ValueError(f"Failed to build model: {e}")
        else:
            self.live = True
        # Validate the connection after building the model
        self.validate_connection()
        return self

    def validate_connection(self):
        """Test if the database connection is valid by executing a simple query."""
        try:
            # Perform a simple query to test the connection
            self.model.objects.using(self.connection_name).exists()
        except Exception as e:
            raise ValueError(
                f"Failed to connect to the database '{self.connection_name}': {e}"
            )

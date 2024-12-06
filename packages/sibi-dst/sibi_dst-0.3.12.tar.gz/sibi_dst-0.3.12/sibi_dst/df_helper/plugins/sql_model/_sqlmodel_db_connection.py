from typing import Any, Optional, Dict, Type
from pydantic import BaseModel, model_validator
from sqlmodel import SQLModel, Field, create_engine
from sqlalchemy import inspect
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql.sqltypes import (
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Date,
    Time,
    Numeric,
)
import datetime


class SQLModelConnectionConfig(BaseModel):
    live: bool = False
    connection_url: str
    table: Optional[str] = None
    model: Optional[Any] = None
    engine: Optional[Any] = None  # Save engine to reuse it

    class Config:
        arbitrary_types_allowed = True

    @model_validator(mode="after")
    def validate_and_initialize(self):
        """
        Validate connection parameters, initialize the engine, and build the dynamic model if necessary.
        """
        # Validate `connection_url`
        if not self.connection_url:
            raise ValueError("`connection_url` must be provided.")

        # Initialize the engine
        self.engine = create_engine(self.connection_url)

        # Validate the connection
        self.validate_connection()

        # If table is provided, set `live=False`
        if self.table:
            self.live = False

        # If model is not provided, build dynamically
        if not self.model:
            if not self.table:
                raise ValueError("`table_name` must be provided to build the model.")
            try:
                self.model = self.build_model()
            except Exception as e:
                raise ValueError(f"Failed to build model for table '{self.table}': {e}")
        else:
            self.live = True

        return self

    def validate_connection(self):
        """
        Test the database connection by executing a simple query.
        """
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except OperationalError as e:
            raise ValueError(f"Failed to connect to the database: {e}")

    def build_model(self) -> Type[SQLModel]:
        """
        Dynamically build a SQLModel class based on the table schema.
        """
        inspector = inspect(self.engine)

        # Validate table existence
        if self.table not in inspector.get_table_names():
            raise ValueError(f"Table '{self.table}' does not exist in the database.")

        columns = inspector.get_columns(self.table)
        if not columns:
            raise ValueError(f"No columns found for table '{self.table}'.")

        type_mapping = {
            Integer: int,
            String: str,
            Float: float,
            Boolean: bool,
            DateTime: datetime.datetime,
            Date: datetime.date,
            Time: datetime.time,
            Numeric: float,
        }

        annotations: Dict[str, Type] = {}
        model_fields = {}

        for column in columns:
            name = column["name"]
            sa_type = column["type"]
            nullable = column["nullable"]
            default = column.get("default", None)
            primary_key = column.get("primary_key", False)

            py_type = None
            for sa_base_type, py_base_type in type_mapping.items():
                if isinstance(sa_type, sa_base_type):
                    py_type = py_base_type
                    break

            if py_type is None:
                raise ValueError(f"Unsupported SQLAlchemy type for column '{name}': {sa_type}")

            # Define field type and attributes
            annotations[name] = py_type
            model_fields[name] = Field(
                default=default,
                nullable=nullable,
                primary_key=primary_key,
                sa_column_args={"type_": sa_type},
            )

        model_fields["__annotations__"] = annotations
        model_fields["__table__"] = self.table
        model_name = self._table2model(self.table)
        return type(model_name, (SQLModel,), model_fields)

    @staticmethod
    def _table2model(table_name: str) -> str:
        """Convert table name to PascalCase model name."""
        return "".join(word.capitalize() for word in table_name.split("_"))
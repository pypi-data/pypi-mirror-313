from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

DEFAULT_NAME = 'default'


class ConnectionConfig(BaseModel):
    """
    Configuration model for a connection.

    Attributes:
        name (str): The name of the connection.
        backend (str): The backend implementation for the connection.
        credentials (dict[str, Any]): The credentials required for the connection.
    """

    name: str = DEFAULT_NAME
    backend: str = 'amsdal_data.connections.implementations.iceberg_history.IcebergHistoricalConnection'
    credentials: dict[str, Any] = Field(default_factory=dict)

    @field_validator('credentials', mode='before')
    @classmethod
    def set_credentials(cls, value: list[dict[str, Any]] | dict[str, Any]) -> dict[str, Any]:
        """
        Validates and sets the credentials attribute.

        Args:
            cls (type): The class type.
            value (list[dict[str, Any]] | dict[str, Any]): The credentials to set,
                either as a dictionary or a list of dictionaries.

        Returns:
            dict[str, Any]: The validated credentials as a dictionary.
        """
        if isinstance(value, dict):
            return value

        credentials = {}

        for credential in value:
            credentials.update(credential)

        return credentials

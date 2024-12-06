from pydantic import BaseModel

from amsdal_utils.config.data_models.repository_config import RepositoryConfig


class ResourcesConfig(BaseModel):
    """
    Configuration model for resources.

    Attributes:
        lakehouse (str): The lakehouse configuration.
        lock (str): The lock configuration.
        repository (RepositoryConfig): The repository configuration.
    """

    lakehouse: str
    lock: str | None = None
    repository: RepositoryConfig | None = None
    worker: str | None = None

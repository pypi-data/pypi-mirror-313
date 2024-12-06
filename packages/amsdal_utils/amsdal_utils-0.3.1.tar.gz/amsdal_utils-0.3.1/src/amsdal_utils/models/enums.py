from enum import Enum


class Versions(str, Enum):
    """
    Enumeration for version types.

    Attributes:
        ALL (str): Represents all versions.
        LATEST (str): Represents the latest version.
    """

    ALL = 'ALL'
    LATEST = 'LATEST'

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class SchemaTypes(str, Enum):
    """
    Enumeration for schema types.

    Attributes:
        TYPE (str): Represents the type schema.
        CORE (str): Represents the core schema.
        USER (str): Represents the user schema.
        CONTRIB (str): Represents the contrib schema.
    """

    TYPE = 'type'
    CORE = 'core'
    USER = 'user'
    CONTRIB = 'contrib'

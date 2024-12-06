from typing import Any
from typing import Union

from pydantic import BaseModel


class DictSchema(BaseModel):
    """
    Schema for a dictionary type.

    This class represents the schema for a dictionary type, where the keys and values
    are defined by the `TypeData` class.

    Attributes:
        key (TypeData): The schema for the dictionary keys.
        value (TypeData): The schema for the dictionary values.
    """

    key: 'TypeData'
    value: 'TypeData'


class LegacyDictSchema(BaseModel):
    """
    Schema for a legacy dictionary type.

    This class represents the schema for a legacy dictionary type, where the key and value types
    are defined as strings.

    Attributes:
        key_type (str): The type of the dictionary keys.
        value_type (str): The type of the dictionary values.
    """

    key_type: str
    value_type: str


class TypeData(BaseModel):
    """
    Schema for type data.

    This class represents the schema for type data, which includes the type, items,
    and default value.

    Attributes:
        type (str): The type of the data.
        items (Union[TypeData, DictSchema, LegacyDictSchema] | None): The items contained within the type data,
            which can be another TypeData, DictSchema, or LegacyDictSchema instance.
        default (Any): The default value for the type data.
    """

    type: str
    items: Union['TypeData', DictSchema, LegacyDictSchema] | None = None
    default: Any = None

from enum import Enum


class MetaClasses(str, Enum):
    """
    Enumeration for meta classes.

    This enum defines the different types of meta classes used in the application.
    These meta classes categorize objects by their roles within the system.

    Attributes:
        TYPE (str): Represents the 'TypeMeta' class.
        CLASS_OBJECT (str): Represents the 'ClassObject' class.
    """

    TYPE = 'TypeMeta'
    CLASS_OBJECT = 'ClassObject'


class BaseClasses(str, Enum):
    """
    Enumeration for base classes.

    This enum defines the different types of base classes used in the application.
    These base classes categorize objects by their fundamental roles within the system.

    Attributes:
        OBJECT (str): Represents the 'Object' class.
        CLASS_OBJECT (str): Represents the 'ClassObject' class.
        CLASS_OBJECT_META (str): Represents the 'ClassObjectMeta' class.
    """

    OBJECT = 'Object'
    CLASS_OBJECT = 'ClassObject'
    CLASS_OBJECT_META = 'ClassObjectMeta'


class CoreTypes(str, Enum):
    """
    Enumeration of core data types.

    This enum class defines the core data types used in the schema definitions.

    Attributes:
        NUMBER (str): Represents a numeric type.
        STRING (str): Represents a string type.
        BOOLEAN (str): Represents a boolean type.
        DICTIONARY (str): Represents a dictionary type.
        ARRAY (str): Represents an array type.
        ANYTHING (str): Represents any type.
        BINARY (str): Represents a binary type.
        OBJECT (str): Represents an object type.
        DATETIME (str): Represents a datetime type.
        DATE (str): Represents a date type.
    """

    NUMBER = 'number'
    STRING = 'string'
    BOOLEAN = 'boolean'
    DICTIONARY = 'dictionary'
    ARRAY = 'array'
    ANYTHING = 'anything'
    BINARY = 'binary'
    OBJECT = 'object'
    DATETIME = 'datetime'
    DATE = 'date'

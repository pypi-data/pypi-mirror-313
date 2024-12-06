from typing import TypeVar

from pydantic import BaseModel
from pydantic import field_validator

from amsdal_utils.models.enums import Versions
from amsdal_utils.query.mixin import QueryableMixin
from amsdal_utils.query.utils import Q

RESOURCE_DELIMITER = '#'
ADDRESS_PARTS_DELIMITER = ':'

AddressType = TypeVar('AddressType', bound='Address')


class Address(QueryableMixin, BaseModel):
    """
    Represents an address in the system.

    Attributes:
        resource (str): The resource/connection name.
        class_name (str): The class name.
        class_version (Versions | str): The class specific version or LATEST/ALL.
        object_id (str): The object id.
        object_version (Versions | str): The object specific version or LATEST/ALL.
    """

    resource: str
    class_name: str
    class_version: Versions | str
    object_id: str
    object_version: Versions | str

    @property
    def is_full(self) -> bool:
        """
        Checks if the address is fully specified.

        Returns:
            bool: True if the address is fully specified, False otherwise.
        """
        return all(
            element and not isinstance(element, Versions)
            for element in [
                self.class_name,
                self.class_version,
                self.object_id,
                self.object_version,
            ]
        )

    @classmethod
    def from_string(cls: type[AddressType], address: str) -> AddressType:
        """
        Creates an Address instance from a string representation.

        Args:
            cls (type[AddressType]): The class type.
            address (str): The string representation of the address.

        Returns:
            AddressType: The Address instance created from the string.

        Raises:
            ValueError: If the resource name is not specified in the address.
        """
        if RESOURCE_DELIMITER not in address:
            msg = f'Resource name is not specified for this address: "{address}".'
            raise ValueError(msg)

        resource, components = address.split(RESOURCE_DELIMITER, 1)

        components_dict = dict(enumerate(components.split(ADDRESS_PARTS_DELIMITER)))

        return cls(
            resource=resource,
            class_name=components_dict.get(0, ''),
            class_version=components_dict.get(1, ''),
            object_id=components_dict.get(2, ''),
            object_version=components_dict.get(3, ''),
        )

    @field_validator('class_version', 'object_version', mode='before')
    @classmethod
    def set_version(cls, version_id: str | Versions) -> str | Versions:
        """
        Validates and sets the version for class_version and object_version fields.

        Args:
            cls (type): The class type.
            version_id (str | Versions): The version identifier, which can be a string or a Versions enum.

        Returns:
            str | Versions: The validated version identifier.

        Raises:
            ValueError: If the version_id is a string that cannot be converted to a Versions enum.
        """
        if isinstance(version_id, str):
            try:
                return Versions(version_id)
            except ValueError:
                pass

        return version_id

    def to_string(self) -> str:
        """
        Converts the Address instance to its string representation.

        Returns:
            str: The string representation of the Address instance.
        """
        parts = [
            str(item)
            for item in [
                self.class_name,
                self.class_version,
                self.object_id,
                self.object_version,
            ]
        ]
        keys_part = ADDRESS_PARTS_DELIMITER.join(parts)

        return f'{self.resource}{RESOURCE_DELIMITER}{keys_part}'

    def to_query(self, prefix: str = '') -> Q:
        """
        Converts the Address instance to a query.
        Args:
            prefix (str, optional): The prefix for the query fields. Defaults to ''.
        Returns:
            Q: The query object.
        """
        object_id_q = Q(**{f'{prefix}object_id': self.object_id})

        if self.object_version == Versions.LATEST:
            object_id_q &= Q(**{f'{prefix}object_version': 'LATEST'}) | Q(**{f'{prefix}object_version': ''})
        elif self.object_version != Versions.ALL:
            object_id_q &= Q(**{f'{prefix}object_version': self.object_version})
        return object_id_q

    # def to_query(self, parent_field: glue.Field | None = None, table_name: str = '') -> glue.Conditions:
    #     object_id_field = glue.Field(name='object_id')
    #     object_version_field = glue.Field(name='object_version')

    #     if parent_field:
    #         _copy_parent = copy(parent_field)
    #         _copy_parent.child = object_id_field
    #         object_id_field.parent = _copy_parent

    #         _copy_parent = copy(parent_field)
    #         _copy_parent.child = object_version_field
    #         object_version_field.parent = _copy_parent

    #     object_id_cond = glue.Conditions(
    #         glue.Condition(
    #             field=glue.FieldReference(
    #                 field=object_id_field,
    #                 table_name=table_name,
    #             ),
    #             operator=glue.FilterConnector.EQ,
    #             value=glue.Value(self.object_id),
    #         ),
    #     )

    #     if self.object_version == Versions.LATEST:
    #         object_id_cond &= glue.Conditions(
    #             glue.Condition(
    #                 field=glue.FieldReference(
    #                     field=object_version_field,
    #                     table_name=table_name,
    #                 ),
    #                 operator=glue.FilterConnector.EQ,
    #                 value=glue.Value(Versions.LATEST.value),
    #             ),
    #             glue.Condition(
    #                 field=glue.FieldReference(
    #                     field=object_version_field,
    #                     table_name=table_name,
    #                 ),
    #                 operator=glue.FilterConnector.EQ,
    #                 value=glue.Value(''),
    #             ),
    #             connector=glue.FilterConnector.OR,
    #         )
    #     elif self.object_version != Versions.ALL:
    #         object_id_cond &= glue.Conditions(
    #             glue.Condition(
    #                 field=glue.FieldReference(
    #                     field=object_version_field,
    #                     table_name=table_name,
    #                 ),
    #                 operator=glue.FilterConnector.EQ,
    #                 value=glue.Value(self.object_version),
    #             ),
    #         )

    #     return object_id_cond

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string()

    def __hash__(self) -> int:
        return hash(self.to_string())

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Address):
            return False

        return self.to_string() == __value.to_string()

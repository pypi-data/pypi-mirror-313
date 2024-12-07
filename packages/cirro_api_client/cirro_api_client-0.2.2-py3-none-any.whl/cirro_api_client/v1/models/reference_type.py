from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.reference_type_validation_item import ReferenceTypeValidationItem


T = TypeVar("T", bound="ReferenceType")


@_attrs_define
class ReferenceType:
    """
    Attributes:
        name (str):
        description (str):
        directory (str):
        validation (List['ReferenceTypeValidationItem']):
    """

    name: str
    description: str
    directory: str
    validation: List["ReferenceTypeValidationItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        directory = self.directory

        validation = []
        for validation_item_data in self.validation:
            validation_item = validation_item_data.to_dict()
            validation.append(validation_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "directory": directory,
                "validation": validation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.reference_type_validation_item import ReferenceTypeValidationItem

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        directory = d.pop("directory")

        validation = []
        _validation = d.pop("validation")
        for validation_item_data in _validation:
            validation_item = ReferenceTypeValidationItem.from_dict(validation_item_data)

            validation.append(validation_item)

        reference_type = cls(
            name=name,
            description=description,
            directory=directory,
            validation=validation,
        )

        reference_type.additional_properties = d
        return reference_type

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

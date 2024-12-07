from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ClassificationInput")


@_attrs_define
class ClassificationInput:
    """
    Attributes:
        name (str):
        description (str):
    """

    name: str
    description: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        classification_input = cls(
            name=name,
            description=description,
        )

        classification_input.additional_properties = d
        return classification_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

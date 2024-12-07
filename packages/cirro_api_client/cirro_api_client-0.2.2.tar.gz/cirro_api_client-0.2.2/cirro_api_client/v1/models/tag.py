from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Tag")


@_attrs_define
class Tag:
    """
    Attributes:
        key (str):
        value (str):
        editable (bool):
    """

    key: str
    value: str
    editable: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key

        value = self.value

        editable = self.editable

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "value": value,
                "editable": editable,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        value = d.pop("value")

        editable = d.pop("editable")

        tag = cls(
            key=key,
            value=value,
            editable=editable,
        )

        tag.additional_properties = d
        return tag

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FormSchemaForm")


@_attrs_define
class FormSchemaForm:
    """JSONSchema representation of the parameters"""

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        form_schema_form = cls()

        form_schema_form.additional_properties = d
        return form_schema_form

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

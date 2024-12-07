from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuditEventChanges")


@_attrs_define
class AuditEventChanges:
    """The changes made to the entity (if applicable)

    Example:
        {'.settings.retentionPolicyDays': '1 -> 2'}

    """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        audit_event_changes = cls()

        audit_event_changes.additional_properties = d
        return audit_event_changes

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

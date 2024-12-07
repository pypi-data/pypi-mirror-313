from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogEntry")


@_attrs_define
class LogEntry:
    """
    Attributes:
        message (str):
        timestamp (Union[Unset, int]): UNIX timestamp in milliseconds, might be blank if we don't have this info
    """

    message: str
    timestamp: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message

        timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "message": message,
            }
        )
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message")

        timestamp = d.pop("timestamp", UNSET)

        log_entry = cls(
            message=message,
            timestamp=timestamp,
        )

        log_entry.additional_properties = d
        return log_entry

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

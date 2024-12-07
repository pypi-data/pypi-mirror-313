from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NotebookInstanceStatusResponse")


@_attrs_define
class NotebookInstanceStatusResponse:
    """
    Attributes:
        status (str):
        status_message (str):
    """

    status: str
    status_message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status

        status_message = self.status_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "statusMessage": status_message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        status_message = d.pop("statusMessage")

        notebook_instance_status_response = cls(
            status=status,
            status_message=status_message,
        )

        notebook_instance_status_response.additional_properties = d
        return notebook_instance_status_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

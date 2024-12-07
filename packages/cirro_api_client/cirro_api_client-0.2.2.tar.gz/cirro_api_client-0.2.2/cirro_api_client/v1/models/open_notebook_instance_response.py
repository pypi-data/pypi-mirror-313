from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OpenNotebookInstanceResponse")


@_attrs_define
class OpenNotebookInstanceResponse:
    """
    Attributes:
        url (str):
        message (str):
    """

    url: str
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        message = d.pop("message")

        open_notebook_instance_response = cls(
            url=url,
            message=message,
        )

        open_notebook_instance_response.additional_properties = d
        return open_notebook_instance_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

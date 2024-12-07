from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateResponse")


@_attrs_define
class CreateResponse:
    """
    Attributes:
        id (str):
        message (str):
    """

    id: str
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        message = d.pop("message")

        create_response = cls(
            id=id,
            message=message,
        )

        create_response.additional_properties = d
        return create_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

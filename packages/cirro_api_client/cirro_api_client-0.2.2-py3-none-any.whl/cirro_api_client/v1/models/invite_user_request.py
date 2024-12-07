from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="InviteUserRequest")


@_attrs_define
class InviteUserRequest:
    """
    Attributes:
        name (str):
        organization (str):
        email (str):
    """

    name: str
    organization: str
    email: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        organization = self.organization

        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "organization": organization,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        organization = d.pop("organization")

        email = d.pop("email")

        invite_user_request = cls(
            name=name,
            organization=organization,
            email=email,
        )

        invite_user_request.additional_properties = d
        return invite_user_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

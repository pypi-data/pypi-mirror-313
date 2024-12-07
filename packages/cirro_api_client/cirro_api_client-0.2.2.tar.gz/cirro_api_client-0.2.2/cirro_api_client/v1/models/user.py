from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="User")


@_attrs_define
class User:
    """
    Attributes:
        name (str):
        username (str):
        organization (str):
        department (str):
    """

    name: str
    username: str
    organization: str
    department: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        username = self.username

        organization = self.organization

        department = self.department

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "username": username,
                "organization": organization,
                "department": department,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        username = d.pop("username")

        organization = d.pop("organization")

        department = d.pop("department")

        user = cls(
            name=name,
            username=username,
            organization=organization,
            department=department,
        )

        user.additional_properties = d
        return user

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

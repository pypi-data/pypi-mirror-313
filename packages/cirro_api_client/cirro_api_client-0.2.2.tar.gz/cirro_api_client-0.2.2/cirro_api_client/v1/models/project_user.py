from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_role import ProjectRole

T = TypeVar("T", bound="ProjectUser")


@_attrs_define
class ProjectUser:
    """
    Attributes:
        name (str):
        username (str):
        organization (str):
        department (str):
        email (str):
        role (ProjectRole):
    """

    name: str
    username: str
    organization: str
    department: str
    email: str
    role: ProjectRole
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        username = self.username

        organization = self.organization

        department = self.department

        email = self.email

        role = self.role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "username": username,
                "organization": organization,
                "department": department,
                "email": email,
                "role": role,
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

        email = d.pop("email")

        role = ProjectRole(d.pop("role"))

        project_user = cls(
            name=name,
            username=username,
            organization=organization,
            department=department,
            email=email,
            role=role,
        )

        project_user.additional_properties = d
        return project_user

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

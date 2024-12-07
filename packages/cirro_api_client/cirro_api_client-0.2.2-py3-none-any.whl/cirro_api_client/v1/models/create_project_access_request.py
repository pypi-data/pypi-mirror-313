from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_role import ProjectRole

T = TypeVar("T", bound="CreateProjectAccessRequest")


@_attrs_define
class CreateProjectAccessRequest:
    """
    Attributes:
        role (ProjectRole):
        message (str):
    """

    role: ProjectRole
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        role = self.role.value

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        role = ProjectRole(d.pop("role"))

        message = d.pop("message")

        create_project_access_request = cls(
            role=role,
            message=message,
        )

        create_project_access_request.additional_properties = d
        return create_project_access_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

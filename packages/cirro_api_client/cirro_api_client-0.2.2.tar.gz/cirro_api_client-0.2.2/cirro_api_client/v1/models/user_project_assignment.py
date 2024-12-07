import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_role import ProjectRole
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserProjectAssignment")


@_attrs_define
class UserProjectAssignment:
    """
    Attributes:
        project_id (str):
        role (ProjectRole):
        created_by (str):
        created_at (Union[None, Unset, datetime.datetime]):
    """

    project_id: str
    role: ProjectRole
    created_by: str
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id

        role = self.role.value

        created_by = self.created_by

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "projectId": project_id,
                "role": role,
                "createdBy": created_by,
            }
        )
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        project_id = d.pop("projectId")

        role = ProjectRole(d.pop("role"))

        created_by = d.pop("createdBy")

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        user_project_assignment = cls(
            project_id=project_id,
            role=role,
            created_by=created_by,
            created_at=created_at,
        )

        user_project_assignment.additional_properties = d
        return user_project_assignment

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

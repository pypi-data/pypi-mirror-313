import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.project_role import ProjectRole
from ..models.request_status import RequestStatus

T = TypeVar("T", bound="ProjectAccessRequest")


@_attrs_define
class ProjectAccessRequest:
    """
    Attributes:
        id (str):
        username (str):
        project_id (str):
        role (ProjectRole):
        message (str):
        status (RequestStatus):
        reviewer_username (str):
        created_at (datetime.datetime):
        expiry (datetime.datetime):
    """

    id: str
    username: str
    project_id: str
    role: ProjectRole
    message: str
    status: RequestStatus
    reviewer_username: str
    created_at: datetime.datetime
    expiry: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        username = self.username

        project_id = self.project_id

        role = self.role.value

        message = self.message

        status = self.status.value

        reviewer_username = self.reviewer_username

        created_at = self.created_at.isoformat()

        expiry = self.expiry.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "username": username,
                "projectId": project_id,
                "role": role,
                "message": message,
                "status": status,
                "reviewerUsername": reviewer_username,
                "createdAt": created_at,
                "expiry": expiry,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        username = d.pop("username")

        project_id = d.pop("projectId")

        role = ProjectRole(d.pop("role"))

        message = d.pop("message")

        status = RequestStatus(d.pop("status"))

        reviewer_username = d.pop("reviewerUsername")

        created_at = isoparse(d.pop("createdAt"))

        expiry = isoparse(d.pop("expiry"))

        project_access_request = cls(
            id=id,
            username=username,
            project_id=project_id,
            role=role,
            message=message,
            status=status,
            reviewer_username=reviewer_username,
            created_at=created_at,
            expiry=expiry,
        )

        project_access_request.additional_properties = d
        return project_access_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

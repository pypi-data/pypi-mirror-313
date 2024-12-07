import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SftpCredentials")


@_attrs_define
class SftpCredentials:
    """
    Attributes:
        username (str):
        password (str):
        project_id (str):
        expires_at (datetime.datetime):
    """

    username: str
    password: str
    project_id: str
    expires_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username

        password = self.password

        project_id = self.project_id

        expires_at = self.expires_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "password": password,
                "projectId": project_id,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        password = d.pop("password")

        project_id = d.pop("projectId")

        expires_at = isoparse(d.pop("expiresAt"))

        sftp_credentials = cls(
            username=username,
            password=password,
            project_id=project_id,
            expires_at=expires_at,
        )

        sftp_credentials.additional_properties = d
        return sftp_credentials

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

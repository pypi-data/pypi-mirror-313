import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Task")


@_attrs_define
class Task:
    """
    Attributes:
        name (str):
        native_job_id (str):
        status (str):
        requested_at (datetime.datetime):
        stopped_at (Union[Unset, datetime.datetime]):
        container_image (Union[Unset, str]):
        command_line (Union[Unset, str]):
        log_location (Union[Unset, str]):
    """

    name: str
    native_job_id: str
    status: str
    requested_at: datetime.datetime
    stopped_at: Union[Unset, datetime.datetime] = UNSET
    container_image: Union[Unset, str] = UNSET
    command_line: Union[Unset, str] = UNSET
    log_location: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        native_job_id = self.native_job_id

        status = self.status

        requested_at = self.requested_at.isoformat()

        stopped_at: Union[Unset, str] = UNSET
        if not isinstance(self.stopped_at, Unset):
            stopped_at = self.stopped_at.isoformat()

        container_image = self.container_image

        command_line = self.command_line

        log_location = self.log_location

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "nativeJobId": native_job_id,
                "status": status,
                "requestedAt": requested_at,
            }
        )
        if stopped_at is not UNSET:
            field_dict["stoppedAt"] = stopped_at
        if container_image is not UNSET:
            field_dict["containerImage"] = container_image
        if command_line is not UNSET:
            field_dict["commandLine"] = command_line
        if log_location is not UNSET:
            field_dict["logLocation"] = log_location

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        native_job_id = d.pop("nativeJobId")

        status = d.pop("status")

        requested_at = isoparse(d.pop("requestedAt"))

        _stopped_at = d.pop("stoppedAt", UNSET)
        stopped_at: Union[Unset, datetime.datetime]
        if isinstance(_stopped_at, Unset):
            stopped_at = UNSET
        else:
            stopped_at = isoparse(_stopped_at)

        container_image = d.pop("containerImage", UNSET)

        command_line = d.pop("commandLine", UNSET)

        log_location = d.pop("logLocation", UNSET)

        task = cls(
            name=name,
            native_job_id=native_job_id,
            status=status,
            requested_at=requested_at,
            stopped_at=stopped_at,
            container_image=container_image,
            command_line=command_line,
            log_location=log_location,
        )

        task.additional_properties = d
        return task

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

import datetime
from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status

T = TypeVar("T", bound="NotebookInstance")


@_attrs_define
class NotebookInstance:
    """
    Attributes:
        id (str):
        name (str):
        status (Status):
        status_message (str):
        instance_type (str):
        accelerator_types (List[str]):
        volume_size_gb (int):
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    name: str
    status: Status
    status_message: str
    instance_type: str
    accelerator_types: List[str]
    volume_size_gb: int
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        status = self.status.value

        status_message = self.status_message

        instance_type = self.instance_type

        accelerator_types = self.accelerator_types

        volume_size_gb = self.volume_size_gb

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "status": status,
                "statusMessage": status_message,
                "instanceType": instance_type,
                "acceleratorTypes": accelerator_types,
                "volumeSizeGB": volume_size_gb,
                "createdBy": created_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        status = Status(d.pop("status"))

        status_message = d.pop("statusMessage")

        instance_type = d.pop("instanceType")

        accelerator_types = cast(List[str], d.pop("acceleratorTypes"))

        volume_size_gb = d.pop("volumeSizeGB")

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        notebook_instance = cls(
            id=id,
            name=name,
            status=status,
            status_message=status_message,
            instance_type=instance_type,
            accelerator_types=accelerator_types,
            volume_size_gb=volume_size_gb,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
        )

        notebook_instance.additional_properties = d
        return notebook_instance

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

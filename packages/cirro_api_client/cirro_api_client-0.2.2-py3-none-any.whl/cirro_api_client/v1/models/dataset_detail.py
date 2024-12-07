import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status

if TYPE_CHECKING:
    from ..models.dataset_detail_info import DatasetDetailInfo
    from ..models.dataset_detail_params import DatasetDetailParams
    from ..models.tag import Tag


T = TypeVar("T", bound="DatasetDetail")


@_attrs_define
class DatasetDetail:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        s3 (str):
        process_id (str):
        project_id (str):
        source_dataset_ids (List[str]):
        status (Status):
        status_message (str):
        tags (List['Tag']):
        params (DatasetDetailParams):
        info (DatasetDetailInfo):
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    name: str
    description: str
    s3: str
    process_id: str
    project_id: str
    source_dataset_ids: List[str]
    status: Status
    status_message: str
    tags: List["Tag"]
    params: "DatasetDetailParams"
    info: "DatasetDetailInfo"
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        s3 = self.s3

        process_id = self.process_id

        project_id = self.project_id

        source_dataset_ids = self.source_dataset_ids

        status = self.status.value

        status_message = self.status_message

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        params = self.params.to_dict()

        info = self.info.to_dict()

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "s3": s3,
                "processId": process_id,
                "projectId": project_id,
                "sourceDatasetIds": source_dataset_ids,
                "status": status,
                "statusMessage": status_message,
                "tags": tags,
                "params": params,
                "info": info,
                "createdBy": created_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dataset_detail_info import DatasetDetailInfo
        from ..models.dataset_detail_params import DatasetDetailParams
        from ..models.tag import Tag

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        s3 = d.pop("s3")

        process_id = d.pop("processId")

        project_id = d.pop("projectId")

        source_dataset_ids = cast(List[str], d.pop("sourceDatasetIds"))

        status = Status(d.pop("status"))

        status_message = d.pop("statusMessage")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = Tag.from_dict(tags_item_data)

            tags.append(tags_item)

        params = DatasetDetailParams.from_dict(d.pop("params"))

        info = DatasetDetailInfo.from_dict(d.pop("info"))

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        dataset_detail = cls(
            id=id,
            name=name,
            description=description,
            s3=s3,
            process_id=process_id,
            project_id=project_id,
            source_dataset_ids=source_dataset_ids,
            status=status,
            status_message=status_message,
            tags=tags,
            params=params,
            info=info,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
        )

        dataset_detail.additional_properties = d
        return dataset_detail

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

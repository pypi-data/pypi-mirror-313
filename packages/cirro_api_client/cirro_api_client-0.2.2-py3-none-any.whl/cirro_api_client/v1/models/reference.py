import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.file_entry import FileEntry


T = TypeVar("T", bound="Reference")


@_attrs_define
class Reference:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        type (str):
        files (List['FileEntry']):
        created_by (str):
        created_at (datetime.datetime):
    """

    id: str
    name: str
    description: str
    type: str
    files: List["FileEntry"]
    created_by: str
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        type = self.type

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "type": type,
                "files": files,
                "createdBy": created_by,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_entry import FileEntry

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        type = d.pop("type")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = FileEntry.from_dict(files_item_data)

            files.append(files_item)

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        reference = cls(
            id=id,
            name=name,
            description=description,
            type=type,
            files=files,
            created_by=created_by,
            created_at=created_at,
        )

        reference.additional_properties = d
        return reference

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

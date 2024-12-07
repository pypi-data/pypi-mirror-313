from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UploadDatasetCreateResponse")


@_attrs_define
class UploadDatasetCreateResponse:
    """
    Attributes:
        id (str):
        message (str):
        upload_path (str):
    """

    id: str
    message: str
    upload_path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        message = self.message

        upload_path = self.upload_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "message": message,
                "uploadPath": upload_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        message = d.pop("message")

        upload_path = d.pop("uploadPath")

        upload_dataset_create_response = cls(
            id=id,
            message=message,
            upload_path=upload_path,
        )

        upload_dataset_create_response.additional_properties = d
        return upload_dataset_create_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

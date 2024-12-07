from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UploadDatasetRequest")


@_attrs_define
class UploadDatasetRequest:
    """
    Attributes:
        name (str): Name of the dataset
        process_id (str): ID of the ingest process Example: paired_dnaseq.
        expected_files (List[str]):
        description (Union[Unset, str]): Description of the dataset
    """

    name: str
    process_id: str
    expected_files: List[str]
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        process_id = self.process_id

        expected_files = self.expected_files

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "processId": process_id,
                "expectedFiles": expected_files,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        process_id = d.pop("processId")

        expected_files = cast(List[str], d.pop("expectedFiles"))

        description = d.pop("description", UNSET)

        upload_dataset_request = cls(
            name=name,
            process_id=process_id,
            expected_files=expected_files,
            description=description,
        )

        upload_dataset_request.additional_properties = d
        return upload_dataset_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ValidateFileRequirementsRequest")


@_attrs_define
class ValidateFileRequirementsRequest:
    """
    Attributes:
        file_names (List[str]):
        sample_sheet (str):
    """

    file_names: List[str]
    sample_sheet: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file_names = self.file_names

        sample_sheet = self.sample_sheet

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "fileNames": file_names,
                "sampleSheet": sample_sheet,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_names = cast(List[str], d.pop("fileNames"))

        sample_sheet = d.pop("sampleSheet")

        validate_file_requirements_request = cls(
            file_names=file_names,
            sample_sheet=sample_sheet,
        )

        validate_file_requirements_request.additional_properties = d
        return validate_file_requirements_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_name_pattern import FileNamePattern


T = TypeVar("T", bound="FileMappingRule")


@_attrs_define
class FileMappingRule:
    """
    Attributes:
        description (str): Describes the group of possible files that meet a single file type criteria.
        file_name_patterns (List['FileNamePattern']): Describes the possible file patterns to expect for the file type
            group.
        min_ (Union[Unset, int]): Minimum number of files to expect for the file type group.
        max_ (Union[Unset, int]): Maximum number of files to expect for the file type group.
        is_sample (Union[Unset, bool]): Specifies if the file type will be associated with a sample.
    """

    description: str
    file_name_patterns: List["FileNamePattern"]
    min_: Union[Unset, int] = UNSET
    max_: Union[Unset, int] = UNSET
    is_sample: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description

        file_name_patterns = []
        for file_name_patterns_item_data in self.file_name_patterns:
            file_name_patterns_item = file_name_patterns_item_data.to_dict()
            file_name_patterns.append(file_name_patterns_item)

        min_ = self.min_

        max_ = self.max_

        is_sample = self.is_sample

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "fileNamePatterns": file_name_patterns,
            }
        )
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_
        if is_sample is not UNSET:
            field_dict["isSample"] = is_sample

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_name_pattern import FileNamePattern

        d = src_dict.copy()
        description = d.pop("description")

        file_name_patterns = []
        _file_name_patterns = d.pop("fileNamePatterns")
        for file_name_patterns_item_data in _file_name_patterns:
            file_name_patterns_item = FileNamePattern.from_dict(file_name_patterns_item_data)

            file_name_patterns.append(file_name_patterns_item)

        min_ = d.pop("min", UNSET)

        max_ = d.pop("max", UNSET)

        is_sample = d.pop("isSample", UNSET)

        file_mapping_rule = cls(
            description=description,
            file_name_patterns=file_name_patterns,
            min_=min_,
            max_=max_,
            is_sample=is_sample,
        )

        file_mapping_rule.additional_properties = d
        return file_mapping_rule

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

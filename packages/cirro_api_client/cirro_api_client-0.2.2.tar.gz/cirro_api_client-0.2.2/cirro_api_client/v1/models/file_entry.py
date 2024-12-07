from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.file_entry_metadata import FileEntryMetadata


T = TypeVar("T", bound="FileEntry")


@_attrs_define
class FileEntry:
    """
    Attributes:
        path (Union[Unset, str]): Relative path to file Example: data/fastq/SRX12875516_SRR16674827_1.fastq.gz.
        size (Union[Unset, int]): File size (in bytes) Example: 1435658507.
        metadata (Union[Unset, FileEntryMetadata]): Metadata associated with the file Example: {'read': 1}.
    """

    path: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    metadata: Union[Unset, "FileEntryMetadata"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path

        size = self.size

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if size is not UNSET:
            field_dict["size"] = size
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_entry_metadata import FileEntryMetadata

        d = src_dict.copy()
        path = d.pop("path", UNSET)

        size = d.pop("size", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, FileEntryMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = FileEntryMetadata.from_dict(_metadata)

        file_entry = cls(
            path=path,
            size=size,
            metadata=metadata,
        )

        file_entry.additional_properties = d
        return file_entry

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

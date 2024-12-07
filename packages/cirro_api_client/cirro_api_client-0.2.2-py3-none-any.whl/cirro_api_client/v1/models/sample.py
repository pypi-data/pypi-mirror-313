import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sample_metadata import SampleMetadata


T = TypeVar("T", bound="Sample")


@_attrs_define
class Sample:
    """
    Attributes:
        id (str):
        name (str):
        metadata (Union['SampleMetadata', None, Unset]):
        dataset_ids (Union[List[str], None, Unset]):
        created_at (Union[None, Unset, datetime.datetime]):
        updated_at (Union[None, Unset, datetime.datetime]):
    """

    id: str
    name: str
    metadata: Union["SampleMetadata", None, Unset] = UNSET
    dataset_ids: Union[List[str], None, Unset] = UNSET
    created_at: Union[None, Unset, datetime.datetime] = UNSET
    updated_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.sample_metadata import SampleMetadata

        id = self.id

        name = self.name

        metadata: Union[Dict[str, Any], None, Unset]
        if isinstance(self.metadata, Unset):
            metadata = UNSET
        elif isinstance(self.metadata, SampleMetadata):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        dataset_ids: Union[List[str], None, Unset]
        if isinstance(self.dataset_ids, Unset):
            dataset_ids = UNSET
        elif isinstance(self.dataset_ids, list):
            dataset_ids = self.dataset_ids

        else:
            dataset_ids = self.dataset_ids

        created_at: Union[None, Unset, str]
        if isinstance(self.created_at, Unset):
            created_at = UNSET
        elif isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        updated_at: Union[None, Unset, str]
        if isinstance(self.updated_at, Unset):
            updated_at = UNSET
        elif isinstance(self.updated_at, datetime.datetime):
            updated_at = self.updated_at.isoformat()
        else:
            updated_at = self.updated_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if dataset_ids is not UNSET:
            field_dict["datasetIds"] = dataset_ids
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sample_metadata import SampleMetadata

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        def _parse_metadata(data: object) -> Union["SampleMetadata", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = SampleMetadata.from_dict(data)

                return metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["SampleMetadata", None, Unset], data)

        metadata = _parse_metadata(d.pop("metadata", UNSET))

        def _parse_dataset_ids(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                dataset_ids_type_0 = cast(List[str], data)

                return dataset_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        dataset_ids = _parse_dataset_ids(d.pop("datasetIds", UNSET))

        def _parse_created_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("createdAt", UNSET))

        def _parse_updated_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                updated_at_type_0 = isoparse(data)

                return updated_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        updated_at = _parse_updated_at(d.pop("updatedAt", UNSET))

        sample = cls(
            id=id,
            name=name,
            metadata=metadata,
            dataset_ids=dataset_ids,
            created_at=created_at,
            updated_at=updated_at,
        )

        sample.additional_properties = d
        return sample

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.sample_request_metadata import SampleRequestMetadata


T = TypeVar("T", bound="SampleRequest")


@_attrs_define
class SampleRequest:
    """
    Attributes:
        name (str):
        metadata (SampleRequestMetadata):
    """

    name: str
    metadata: "SampleRequestMetadata"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        metadata = self.metadata.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "metadata": metadata,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sample_request_metadata import SampleRequestMetadata

        d = src_dict.copy()
        name = d.pop("name")

        metadata = SampleRequestMetadata.from_dict(d.pop("metadata"))

        sample_request = cls(
            name=name,
            metadata=metadata,
        )

        sample_request.additional_properties = d
        return sample_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

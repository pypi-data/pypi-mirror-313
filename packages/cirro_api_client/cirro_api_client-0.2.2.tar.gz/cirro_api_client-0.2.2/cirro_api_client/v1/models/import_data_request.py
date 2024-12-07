from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportDataRequest")


@_attrs_define
class ImportDataRequest:
    """
    Attributes:
        name (str): Name of the dataset
        public_ids (List[str]):
        description (Union[Unset, str]): Description of the dataset
    """

    name: str
    public_ids: List[str]
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        public_ids = self.public_ids

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "publicIds": public_ids,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        public_ids = cast(List[str], d.pop("publicIds"))

        description = d.pop("description", UNSET)

        import_data_request = cls(
            name=name,
            public_ids=public_ids,
            description=description,
        )

        import_data_request.additional_properties = d
        return import_data_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetViz")


@_attrs_define
class DatasetViz:
    """
    Attributes:
        name (Union[Unset, str]): Name of viz
        desc (Union[Unset, str]): Description of viz
        type (Union[Unset, str]): Type of viz Example: vitescce.
        config (Union[Unset, Any]): Config or path to config used to render viz
    """

    name: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    config: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        desc = self.desc

        type = self.type

        config = self.config

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if desc is not UNSET:
            field_dict["desc"] = desc
        if type is not UNSET:
            field_dict["type"] = type
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        desc = d.pop("desc", UNSET)

        type = d.pop("type", UNSET)

        config = d.pop("config", UNSET)

        dataset_viz = cls(
            name=name,
            desc=desc,
            type=type,
            config=config,
        )

        dataset_viz.additional_properties = d
        return dataset_viz

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

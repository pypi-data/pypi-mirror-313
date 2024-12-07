from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ColumnDefinition")


@_attrs_define
class ColumnDefinition:
    """
    Attributes:
        col (Union[Unset, str]): Column name in asset file
        name (Union[Unset, str]): User-friendly column name
        desc (Union[Unset, str]): Description of the column
    """

    col: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    desc: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        col = self.col

        name = self.name

        desc = self.desc

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if col is not UNSET:
            field_dict["col"] = col
        if name is not UNSET:
            field_dict["name"] = name
        if desc is not UNSET:
            field_dict["desc"] = desc

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        col = d.pop("col", UNSET)

        name = d.pop("name", UNSET)

        desc = d.pop("desc", UNSET)

        column_definition = cls(
            col=col,
            name=name,
            desc=desc,
        )

        column_definition.additional_properties = d
        return column_definition

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

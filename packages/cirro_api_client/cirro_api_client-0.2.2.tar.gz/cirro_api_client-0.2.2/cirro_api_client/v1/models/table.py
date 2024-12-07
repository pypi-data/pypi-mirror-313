from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.column_definition import ColumnDefinition


T = TypeVar("T", bound="Table")


@_attrs_define
class Table:
    """
    Attributes:
        desc (str):
        name (Union[Unset, str]): User-friendly name of asset
        type (Union[Unset, str]): Type of file Example: parquet.
        rows (Union[Unset, int]): Number of rows in table
        path (Union[Unset, str]): Relative path to asset
        cols (Union[List['ColumnDefinition'], None, Unset]):
    """

    desc: str
    name: Union[Unset, str] = UNSET
    type: Union[Unset, str] = UNSET
    rows: Union[Unset, int] = UNSET
    path: Union[Unset, str] = UNSET
    cols: Union[List["ColumnDefinition"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        desc = self.desc

        name = self.name

        type = self.type

        rows = self.rows

        path = self.path

        cols: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.cols, Unset):
            cols = UNSET
        elif isinstance(self.cols, list):
            cols = []
            for cols_type_0_item_data in self.cols:
                cols_type_0_item = cols_type_0_item_data.to_dict()
                cols.append(cols_type_0_item)

        else:
            cols = self.cols

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "desc": desc,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if type is not UNSET:
            field_dict["type"] = type
        if rows is not UNSET:
            field_dict["rows"] = rows
        if path is not UNSET:
            field_dict["path"] = path
        if cols is not UNSET:
            field_dict["cols"] = cols

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.column_definition import ColumnDefinition

        d = src_dict.copy()
        desc = d.pop("desc")

        name = d.pop("name", UNSET)

        type = d.pop("type", UNSET)

        rows = d.pop("rows", UNSET)

        path = d.pop("path", UNSET)

        def _parse_cols(data: object) -> Union[List["ColumnDefinition"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                cols_type_0 = []
                _cols_type_0 = data
                for cols_type_0_item_data in _cols_type_0:
                    cols_type_0_item = ColumnDefinition.from_dict(cols_type_0_item_data)

                    cols_type_0.append(cols_type_0_item)

                return cols_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["ColumnDefinition"], None, Unset], data)

        cols = _parse_cols(d.pop("cols", UNSET))

        table = cls(
            desc=desc,
            name=name,
            type=type,
            rows=rows,
            path=path,
            cols=cols,
        )

        table.additional_properties = d
        return table

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

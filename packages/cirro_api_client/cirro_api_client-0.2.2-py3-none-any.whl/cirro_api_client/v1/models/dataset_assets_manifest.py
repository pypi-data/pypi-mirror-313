from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dataset_viz import DatasetViz
    from ..models.file_entry import FileEntry
    from ..models.table import Table


T = TypeVar("T", bound="DatasetAssetsManifest")


@_attrs_define
class DatasetAssetsManifest:
    """
    Attributes:
        domain (Union[Unset, str]): Base URL for files Example: s3://project-1a1a/datasets/1a1a.
        files (Union[Unset, List['FileEntry']]): List of files in the dataset, including metadata
        total_files (Union[Unset, int]): Total number of files in the dataset, used for pagination
        viz (Union[Unset, List['DatasetViz']]): List of viz to render for the dataset
        tables (Union[Unset, List['Table']]): List of web optimized tables for the dataset
    """

    domain: Union[Unset, str] = UNSET
    files: Union[Unset, List["FileEntry"]] = UNSET
    total_files: Union[Unset, int] = UNSET
    viz: Union[Unset, List["DatasetViz"]] = UNSET
    tables: Union[Unset, List["Table"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        domain = self.domain

        files: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_dict()
                files.append(files_item)

        total_files = self.total_files

        viz: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.viz, Unset):
            viz = []
            for viz_item_data in self.viz:
                viz_item = viz_item_data.to_dict()
                viz.append(viz_item)

        tables: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tables, Unset):
            tables = []
            for tables_item_data in self.tables:
                tables_item = tables_item_data.to_dict()
                tables.append(tables_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if domain is not UNSET:
            field_dict["domain"] = domain
        if files is not UNSET:
            field_dict["files"] = files
        if total_files is not UNSET:
            field_dict["totalFiles"] = total_files
        if viz is not UNSET:
            field_dict["viz"] = viz
        if tables is not UNSET:
            field_dict["tables"] = tables

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dataset_viz import DatasetViz
        from ..models.file_entry import FileEntry
        from ..models.table import Table

        d = src_dict.copy()
        domain = d.pop("domain", UNSET)

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = FileEntry.from_dict(files_item_data)

            files.append(files_item)

        total_files = d.pop("totalFiles", UNSET)

        viz = []
        _viz = d.pop("viz", UNSET)
        for viz_item_data in _viz or []:
            viz_item = DatasetViz.from_dict(viz_item_data)

            viz.append(viz_item)

        tables = []
        _tables = d.pop("tables", UNSET)
        for tables_item_data in _tables or []:
            tables_item = Table.from_dict(tables_item_data)

            tables.append(tables_item)

        dataset_assets_manifest = cls(
            domain=domain,
            files=files,
            total_files=total_files,
            viz=viz,
            tables=tables,
        )

        dataset_assets_manifest.additional_properties = d
        return dataset_assets_manifest

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

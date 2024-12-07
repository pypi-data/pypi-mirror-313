from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.repository_type import RepositoryType

T = TypeVar("T", bound="PipelineCode")


@_attrs_define
class PipelineCode:
    """Used to describe the pipeline analysis code, not required for ingest processes

    Attributes:
        repository_path (str): GitHub repository which contains the workflow code Example: nf-core/rnaseq.
        version (str): Branch, tag, or commit hash of the pipeline code Example: main.
        repository_type (RepositoryType): Type of repository
        entry_point (str): Main script for running the pipeline Example: main.nf.
    """

    repository_path: str
    version: str
    repository_type: RepositoryType
    entry_point: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repository_path = self.repository_path

        version = self.version

        repository_type = self.repository_type.value

        entry_point = self.entry_point

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repositoryPath": repository_path,
                "version": version,
                "repositoryType": repository_type,
                "entryPoint": entry_point,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repository_path = d.pop("repositoryPath")

        version = d.pop("version")

        repository_type = RepositoryType(d.pop("repositoryType"))

        entry_point = d.pop("entryPoint")

        pipeline_code = cls(
            repository_path=repository_path,
            version=version,
            repository_type=repository_type,
            entry_point=entry_point,
        )

        pipeline_code.additional_properties = d
        return pipeline_code

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

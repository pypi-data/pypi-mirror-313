from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.executor import Executor
from ..types import UNSET, Unset

T = TypeVar("T", bound="Process")


@_attrs_define
class Process:
    """
    Attributes:
        id (str): Unique ID of the Process Example: process-hutch-magic_flute-1_0.
        name (str): Friendly name for the process Example: MAGeCK Flute.
        executor (Executor): How the workflow is executed
        category (str): Category of the process Example: Microbial Analysis.
        pipeline_type (str): Type of pipeline Example: nf-core.
        description (Union[Unset, str]):  Example: MAGeCK Flute enables accurate identification of essential genes with
            their related biological functions.
        data_type (Union[None, Unset, str]): Name of the data type this pipeline produces (if it is not defined, use the
            name)
        documentation_url (Union[Unset, str]): Link to pipeline documentation Example:
            https://docs.cirro.bio/pipelines/catalog_targeted_sequencing/#crispr-screen-analysis.
        file_requirements_message (Union[Unset, str]): Description of the files to be uploaded (optional)
        child_process_ids (Union[Unset, List[str]]): IDs of pipelines that can be run downstream
        parent_process_ids (Union[Unset, List[str]]): IDs of pipelines that can run this pipeline
        owner (Union[Unset, str]): Username of the pipeline creator (blank if Cirro curated)
        linked_project_ids (Union[Unset, List[str]]): Projects that can run this pipeline
        allow_multiple_sources (Union[Unset, bool]): Whether the pipeline is allowed to have multiple dataset sources
        is_archived (Union[Unset, bool]): Whether the pipeline is marked as archived
    """

    id: str
    name: str
    executor: Executor
    category: str
    pipeline_type: str
    description: Union[Unset, str] = UNSET
    data_type: Union[None, Unset, str] = UNSET
    documentation_url: Union[Unset, str] = UNSET
    file_requirements_message: Union[Unset, str] = UNSET
    child_process_ids: Union[Unset, List[str]] = UNSET
    parent_process_ids: Union[Unset, List[str]] = UNSET
    owner: Union[Unset, str] = UNSET
    linked_project_ids: Union[Unset, List[str]] = UNSET
    allow_multiple_sources: Union[Unset, bool] = UNSET
    is_archived: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        executor = self.executor.value

        category = self.category

        pipeline_type = self.pipeline_type

        description = self.description

        data_type: Union[None, Unset, str]
        if isinstance(self.data_type, Unset):
            data_type = UNSET
        else:
            data_type = self.data_type

        documentation_url = self.documentation_url

        file_requirements_message = self.file_requirements_message

        child_process_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.child_process_ids, Unset):
            child_process_ids = self.child_process_ids

        parent_process_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parent_process_ids, Unset):
            parent_process_ids = self.parent_process_ids

        owner = self.owner

        linked_project_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.linked_project_ids, Unset):
            linked_project_ids = self.linked_project_ids

        allow_multiple_sources = self.allow_multiple_sources

        is_archived = self.is_archived

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "executor": executor,
                "category": category,
                "pipelineType": pipeline_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if documentation_url is not UNSET:
            field_dict["documentationUrl"] = documentation_url
        if file_requirements_message is not UNSET:
            field_dict["fileRequirementsMessage"] = file_requirements_message
        if child_process_ids is not UNSET:
            field_dict["childProcessIds"] = child_process_ids
        if parent_process_ids is not UNSET:
            field_dict["parentProcessIds"] = parent_process_ids
        if owner is not UNSET:
            field_dict["owner"] = owner
        if linked_project_ids is not UNSET:
            field_dict["linkedProjectIds"] = linked_project_ids
        if allow_multiple_sources is not UNSET:
            field_dict["allowMultipleSources"] = allow_multiple_sources
        if is_archived is not UNSET:
            field_dict["isArchived"] = is_archived

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        executor = Executor(d.pop("executor"))

        category = d.pop("category")

        pipeline_type = d.pop("pipelineType")

        description = d.pop("description", UNSET)

        def _parse_data_type(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        data_type = _parse_data_type(d.pop("dataType", UNSET))

        documentation_url = d.pop("documentationUrl", UNSET)

        file_requirements_message = d.pop("fileRequirementsMessage", UNSET)

        child_process_ids = cast(List[str], d.pop("childProcessIds", UNSET))

        parent_process_ids = cast(List[str], d.pop("parentProcessIds", UNSET))

        owner = d.pop("owner", UNSET)

        linked_project_ids = cast(List[str], d.pop("linkedProjectIds", UNSET))

        allow_multiple_sources = d.pop("allowMultipleSources", UNSET)

        is_archived = d.pop("isArchived", UNSET)

        process = cls(
            id=id,
            name=name,
            executor=executor,
            category=category,
            pipeline_type=pipeline_type,
            description=description,
            data_type=data_type,
            documentation_url=documentation_url,
            file_requirements_message=file_requirements_message,
            child_process_ids=child_process_ids,
            parent_process_ids=parent_process_ids,
            owner=owner,
            linked_project_ids=linked_project_ids,
            allow_multiple_sources=allow_multiple_sources,
            is_archived=is_archived,
        )

        process.additional_properties = d
        return process

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

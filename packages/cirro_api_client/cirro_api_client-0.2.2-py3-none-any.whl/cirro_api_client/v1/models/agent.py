from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agent_status import AgentStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_tags import AgentTags


T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """Details of the agent

    Attributes:
        status (AgentStatus): The status of the agent
        id (Union[Unset, str]): The unique ID of the agent
        name (Union[Unset, str]): The display name of the agent
        tags (Union[Unset, AgentTags]): Tags associated with the agent
    """

    status: AgentStatus
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, "AgentTags"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        id = self.id

        name = self.name

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.agent_tags import AgentTags

        d = src_dict.copy()
        status = AgentStatus(d.pop("status"))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, AgentTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = AgentTags.from_dict(_tags)

        agent = cls(
            status=status,
            id=id,
            name=name,
            tags=tags,
        )

        agent.additional_properties = d
        return agent

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

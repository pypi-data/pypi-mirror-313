from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentInputTags")


@_attrs_define
class AgentInputTags:
    """The tags associated with the agent displayed to the user

    Example:
        {'Support Email': 'it@company.com'}

    """

    additional_properties: Dict[str, str] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        agent_input_tags = cls()

        agent_input_tags.additional_properties = d
        return agent_input_tags

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

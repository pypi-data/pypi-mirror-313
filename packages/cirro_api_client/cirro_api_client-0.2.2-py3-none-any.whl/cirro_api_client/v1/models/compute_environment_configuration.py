import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.environment_type import EnvironmentType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent import Agent
    from ..models.compute_environment_configuration_properties import ComputeEnvironmentConfigurationProperties


T = TypeVar("T", bound="ComputeEnvironmentConfiguration")


@_attrs_define
class ComputeEnvironmentConfiguration:
    """
    Attributes:
        environment_type (EnvironmentType): The type of compute environment
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        id (Union[Unset, str]): The unique ID of the environment
        name (Union[Unset, str]): The display name of the environment
        properties (Union[Unset, ComputeEnvironmentConfigurationProperties]): Configuration properties passed to the
            environment
        agent (Union['Agent', None, Unset]):
        created_by (Union[Unset, str]): The user who created the environment
    """

    environment_type: EnvironmentType
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    properties: Union[Unset, "ComputeEnvironmentConfigurationProperties"] = UNSET
    agent: Union["Agent", None, Unset] = UNSET
    created_by: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.agent import Agent

        environment_type = self.environment_type.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        id = self.id

        name = self.name

        properties: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        agent: Union[Dict[str, Any], None, Unset]
        if isinstance(self.agent, Unset):
            agent = UNSET
        elif isinstance(self.agent, Agent):
            agent = self.agent.to_dict()
        else:
            agent = self.agent

        created_by = self.created_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "environmentType": environment_type,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if properties is not UNSET:
            field_dict["properties"] = properties
        if agent is not UNSET:
            field_dict["agent"] = agent
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.agent import Agent
        from ..models.compute_environment_configuration_properties import ComputeEnvironmentConfigurationProperties

        d = src_dict.copy()
        environment_type = EnvironmentType(d.pop("environmentType"))

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _properties = d.pop("properties", UNSET)
        properties: Union[Unset, ComputeEnvironmentConfigurationProperties]
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = ComputeEnvironmentConfigurationProperties.from_dict(_properties)

        def _parse_agent(data: object) -> Union["Agent", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                agent_type_1 = Agent.from_dict(data)

                return agent_type_1
            except:  # noqa: E722
                pass
            return cast(Union["Agent", None, Unset], data)

        agent = _parse_agent(d.pop("agent", UNSET))

        created_by = d.pop("createdBy", UNSET)

        compute_environment_configuration = cls(
            environment_type=environment_type,
            created_at=created_at,
            updated_at=updated_at,
            id=id,
            name=name,
            properties=properties,
            agent=agent,
            created_by=created_by,
        )

        compute_environment_configuration.additional_properties = d
        return compute_environment_configuration

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

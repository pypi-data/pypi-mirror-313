from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_input_configuration_options_schema import AgentInputConfigurationOptionsSchema
    from ..models.agent_input_environment_configuration import AgentInputEnvironmentConfiguration
    from ..models.agent_input_tags import AgentInputTags


T = TypeVar("T", bound="AgentInput")


@_attrs_define
class AgentInput:
    """
    Attributes:
        name (str): The display name of the agent
        agent_role_arn (str): Arn of the AWS IAM role or user that the agent will use (JSONSchema format)
        id (Union[None, Unset, str]): The unique ID of the agent (required on create)
        configuration_options_schema (Union['AgentInputConfigurationOptionsSchema', None, Unset]): The configuration
            options available for the agent
        environment_configuration (Union['AgentInputEnvironmentConfiguration', None, Unset]): The environment
            configuration for the agent Example: {'PARTITION': 'restart'}.
        tags (Union['AgentInputTags', None, Unset]): The tags associated with the agent displayed to the user Example:
            {'Support Email': 'it@company.com'}.
    """

    name: str
    agent_role_arn: str
    id: Union[None, Unset, str] = UNSET
    configuration_options_schema: Union["AgentInputConfigurationOptionsSchema", None, Unset] = UNSET
    environment_configuration: Union["AgentInputEnvironmentConfiguration", None, Unset] = UNSET
    tags: Union["AgentInputTags", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.agent_input_configuration_options_schema import AgentInputConfigurationOptionsSchema
        from ..models.agent_input_environment_configuration import AgentInputEnvironmentConfiguration
        from ..models.agent_input_tags import AgentInputTags

        name = self.name

        agent_role_arn = self.agent_role_arn

        id: Union[None, Unset, str]
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        configuration_options_schema: Union[Dict[str, Any], None, Unset]
        if isinstance(self.configuration_options_schema, Unset):
            configuration_options_schema = UNSET
        elif isinstance(self.configuration_options_schema, AgentInputConfigurationOptionsSchema):
            configuration_options_schema = self.configuration_options_schema.to_dict()
        else:
            configuration_options_schema = self.configuration_options_schema

        environment_configuration: Union[Dict[str, Any], None, Unset]
        if isinstance(self.environment_configuration, Unset):
            environment_configuration = UNSET
        elif isinstance(self.environment_configuration, AgentInputEnvironmentConfiguration):
            environment_configuration = self.environment_configuration.to_dict()
        else:
            environment_configuration = self.environment_configuration

        tags: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, AgentInputTags):
            tags = self.tags.to_dict()
        else:
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "agentRoleArn": agent_role_arn,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if configuration_options_schema is not UNSET:
            field_dict["configurationOptionsSchema"] = configuration_options_schema
        if environment_configuration is not UNSET:
            field_dict["environmentConfiguration"] = environment_configuration
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.agent_input_configuration_options_schema import AgentInputConfigurationOptionsSchema
        from ..models.agent_input_environment_configuration import AgentInputEnvironmentConfiguration
        from ..models.agent_input_tags import AgentInputTags

        d = src_dict.copy()
        name = d.pop("name")

        agent_role_arn = d.pop("agentRoleArn")

        def _parse_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        id = _parse_id(d.pop("id", UNSET))

        def _parse_configuration_options_schema(
            data: object,
        ) -> Union["AgentInputConfigurationOptionsSchema", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                configuration_options_schema_type_0 = AgentInputConfigurationOptionsSchema.from_dict(data)

                return configuration_options_schema_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentInputConfigurationOptionsSchema", None, Unset], data)

        configuration_options_schema = _parse_configuration_options_schema(d.pop("configurationOptionsSchema", UNSET))

        def _parse_environment_configuration(data: object) -> Union["AgentInputEnvironmentConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                environment_configuration_type_0 = AgentInputEnvironmentConfiguration.from_dict(data)

                return environment_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentInputEnvironmentConfiguration", None, Unset], data)

        environment_configuration = _parse_environment_configuration(d.pop("environmentConfiguration", UNSET))

        def _parse_tags(data: object) -> Union["AgentInputTags", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tags_type_0 = AgentInputTags.from_dict(data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentInputTags", None, Unset], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        agent_input = cls(
            name=name,
            agent_role_arn=agent_role_arn,
            id=id,
            configuration_options_schema=configuration_options_schema,
            environment_configuration=environment_configuration,
            tags=tags,
        )

        agent_input.additional_properties = d
        return agent_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

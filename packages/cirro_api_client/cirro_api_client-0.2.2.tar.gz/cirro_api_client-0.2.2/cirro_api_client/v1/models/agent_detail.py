import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.agent_status import AgentStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.agent_detail_environment_configuration import AgentDetailEnvironmentConfiguration
    from ..models.agent_detail_tags import AgentDetailTags
    from ..models.agent_registration import AgentRegistration


T = TypeVar("T", bound="AgentDetail")


@_attrs_define
class AgentDetail:
    """
    Attributes:
        id (str):
        name (str):
        agent_role_arn (str):
        status (AgentStatus): The status of the agent
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        registration (Union['AgentRegistration', None, Unset]):
        tags (Union['AgentDetailTags', None, Unset]):
        environment_configuration (Union['AgentDetailEnvironmentConfiguration', None, Unset]):
    """

    id: str
    name: str
    agent_role_arn: str
    status: AgentStatus
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    registration: Union["AgentRegistration", None, Unset] = UNSET
    tags: Union["AgentDetailTags", None, Unset] = UNSET
    environment_configuration: Union["AgentDetailEnvironmentConfiguration", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.agent_detail_environment_configuration import AgentDetailEnvironmentConfiguration
        from ..models.agent_detail_tags import AgentDetailTags
        from ..models.agent_registration import AgentRegistration

        id = self.id

        name = self.name

        agent_role_arn = self.agent_role_arn

        status = self.status.value

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        registration: Union[Dict[str, Any], None, Unset]
        if isinstance(self.registration, Unset):
            registration = UNSET
        elif isinstance(self.registration, AgentRegistration):
            registration = self.registration.to_dict()
        else:
            registration = self.registration

        tags: Union[Dict[str, Any], None, Unset]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, AgentDetailTags):
            tags = self.tags.to_dict()
        else:
            tags = self.tags

        environment_configuration: Union[Dict[str, Any], None, Unset]
        if isinstance(self.environment_configuration, Unset):
            environment_configuration = UNSET
        elif isinstance(self.environment_configuration, AgentDetailEnvironmentConfiguration):
            environment_configuration = self.environment_configuration.to_dict()
        else:
            environment_configuration = self.environment_configuration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "agentRoleArn": agent_role_arn,
                "status": status,
                "createdBy": created_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if registration is not UNSET:
            field_dict["registration"] = registration
        if tags is not UNSET:
            field_dict["tags"] = tags
        if environment_configuration is not UNSET:
            field_dict["environmentConfiguration"] = environment_configuration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.agent_detail_environment_configuration import AgentDetailEnvironmentConfiguration
        from ..models.agent_detail_tags import AgentDetailTags
        from ..models.agent_registration import AgentRegistration

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        agent_role_arn = d.pop("agentRoleArn")

        status = AgentStatus(d.pop("status"))

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        def _parse_registration(data: object) -> Union["AgentRegistration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                registration_type_1 = AgentRegistration.from_dict(data)

                return registration_type_1
            except:  # noqa: E722
                pass
            return cast(Union["AgentRegistration", None, Unset], data)

        registration = _parse_registration(d.pop("registration", UNSET))

        def _parse_tags(data: object) -> Union["AgentDetailTags", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                tags_type_0 = AgentDetailTags.from_dict(data)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentDetailTags", None, Unset], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_environment_configuration(data: object) -> Union["AgentDetailEnvironmentConfiguration", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                environment_configuration_type_0 = AgentDetailEnvironmentConfiguration.from_dict(data)

                return environment_configuration_type_0
            except:  # noqa: E722
                pass
            return cast(Union["AgentDetailEnvironmentConfiguration", None, Unset], data)

        environment_configuration = _parse_environment_configuration(d.pop("environmentConfiguration", UNSET))

        agent_detail = cls(
            id=id,
            name=name,
            agent_role_arn=agent_role_arn,
            status=status,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            registration=registration,
            tags=tags,
            environment_configuration=environment_configuration,
        )

        agent_detail.additional_properties = d
        return agent_detail

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

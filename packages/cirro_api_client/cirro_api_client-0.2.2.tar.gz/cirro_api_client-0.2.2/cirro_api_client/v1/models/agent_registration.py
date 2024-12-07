from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AgentRegistration")


@_attrs_define
class AgentRegistration:
    """
    Attributes:
        local_ip (str):
        remote_ip (str):
        agent_version (str):
        hostname (str):
        os (str):
    """

    local_ip: str
    remote_ip: str
    agent_version: str
    hostname: str
    os: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        local_ip = self.local_ip

        remote_ip = self.remote_ip

        agent_version = self.agent_version

        hostname = self.hostname

        os = self.os

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "localIp": local_ip,
                "remoteIp": remote_ip,
                "agentVersion": agent_version,
                "hostname": hostname,
                "os": os,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        local_ip = d.pop("localIp")

        remote_ip = d.pop("remoteIp")

        agent_version = d.pop("agentVersion")

        hostname = d.pop("hostname")

        os = d.pop("os")

        agent_registration = cls(
            local_ip=local_ip,
            remote_ip=remote_ip,
            agent_version=agent_version,
            hostname=hostname,
            os=os,
        )

        agent_registration.additional_properties = d
        return agent_registration

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

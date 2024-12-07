from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.auth_info import AuthInfo
    from ..models.resources_info import ResourcesInfo
    from ..models.tenant_info import TenantInfo


T = TypeVar("T", bound="SystemInfoResponse")


@_attrs_define
class SystemInfoResponse:
    """
    Attributes:
        resources_bucket (str):
        references_bucket (str):
        live_endpoint (str):
        agent_endpoint (str):
        region (str):
        system_message (str):
        maintenance_mode_enabled (bool):
        commit_hash (str):
        version (str):
        resources_info (ResourcesInfo):
        tenant_info (TenantInfo):
        auth (AuthInfo):
    """

    resources_bucket: str
    references_bucket: str
    live_endpoint: str
    agent_endpoint: str
    region: str
    system_message: str
    maintenance_mode_enabled: bool
    commit_hash: str
    version: str
    resources_info: "ResourcesInfo"
    tenant_info: "TenantInfo"
    auth: "AuthInfo"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        resources_bucket = self.resources_bucket

        references_bucket = self.references_bucket

        live_endpoint = self.live_endpoint

        agent_endpoint = self.agent_endpoint

        region = self.region

        system_message = self.system_message

        maintenance_mode_enabled = self.maintenance_mode_enabled

        commit_hash = self.commit_hash

        version = self.version

        resources_info = self.resources_info.to_dict()

        tenant_info = self.tenant_info.to_dict()

        auth = self.auth.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourcesBucket": resources_bucket,
                "referencesBucket": references_bucket,
                "liveEndpoint": live_endpoint,
                "agentEndpoint": agent_endpoint,
                "region": region,
                "systemMessage": system_message,
                "maintenanceModeEnabled": maintenance_mode_enabled,
                "commitHash": commit_hash,
                "version": version,
                "resourcesInfo": resources_info,
                "tenantInfo": tenant_info,
                "auth": auth,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.auth_info import AuthInfo
        from ..models.resources_info import ResourcesInfo
        from ..models.tenant_info import TenantInfo

        d = src_dict.copy()
        resources_bucket = d.pop("resourcesBucket")

        references_bucket = d.pop("referencesBucket")

        live_endpoint = d.pop("liveEndpoint")

        agent_endpoint = d.pop("agentEndpoint")

        region = d.pop("region")

        system_message = d.pop("systemMessage")

        maintenance_mode_enabled = d.pop("maintenanceModeEnabled")

        commit_hash = d.pop("commitHash")

        version = d.pop("version")

        resources_info = ResourcesInfo.from_dict(d.pop("resourcesInfo"))

        tenant_info = TenantInfo.from_dict(d.pop("tenantInfo"))

        auth = AuthInfo.from_dict(d.pop("auth"))

        system_info_response = cls(
            resources_bucket=resources_bucket,
            references_bucket=references_bucket,
            live_endpoint=live_endpoint,
            agent_endpoint=agent_endpoint,
            region=region,
            system_message=system_message,
            maintenance_mode_enabled=maintenance_mode_enabled,
            commit_hash=commit_hash,
            version=version,
            resources_info=resources_info,
            tenant_info=tenant_info,
            auth=auth,
        )

        system_info_response.additional_properties = d
        return system_info_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

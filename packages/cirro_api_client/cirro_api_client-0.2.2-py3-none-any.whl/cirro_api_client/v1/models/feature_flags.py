from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="FeatureFlags")


@_attrs_define
class FeatureFlags:
    """
    Attributes:
        sftp_enabled (bool):
        governance_enabled (bool):
        project_requests_enabled (bool):
    """

    sftp_enabled: bool
    governance_enabled: bool
    project_requests_enabled: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        sftp_enabled = self.sftp_enabled

        governance_enabled = self.governance_enabled

        project_requests_enabled = self.project_requests_enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "sftpEnabled": sftp_enabled,
                "governanceEnabled": governance_enabled,
                "projectRequestsEnabled": project_requests_enabled,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sftp_enabled = d.pop("sftpEnabled")

        governance_enabled = d.pop("governanceEnabled")

        project_requests_enabled = d.pop("projectRequestsEnabled")

        feature_flags = cls(
            sftp_enabled=sftp_enabled,
            governance_enabled=governance_enabled,
            project_requests_enabled=project_requests_enabled,
        )

        feature_flags.additional_properties = d
        return feature_flags

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

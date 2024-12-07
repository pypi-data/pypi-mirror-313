from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateSftpCredentialsRequest")


@_attrs_define
class GenerateSftpCredentialsRequest:
    """
    Attributes:
        lifetime_days (Union[Unset, int]): Number of days the credentials are valid for Default: 1.
    """

    lifetime_days: Union[Unset, int] = 1
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        lifetime_days = self.lifetime_days

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if lifetime_days is not UNSET:
            field_dict["lifetimeDays"] = lifetime_days

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lifetime_days = d.pop("lifetimeDays", UNSET)

        generate_sftp_credentials_request = cls(
            lifetime_days=lifetime_days,
        )

        generate_sftp_credentials_request.additional_properties = d
        return generate_sftp_credentials_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

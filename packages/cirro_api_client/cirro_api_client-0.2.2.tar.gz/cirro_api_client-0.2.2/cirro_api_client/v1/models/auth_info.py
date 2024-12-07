from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthInfo")


@_attrs_define
class AuthInfo:
    """
    Attributes:
        user_pool_id (str):
        sdk_app_id (str):
        ui_app_id (str):
        endpoint (str):
    """

    user_pool_id: str
    sdk_app_id: str
    ui_app_id: str
    endpoint: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_pool_id = self.user_pool_id

        sdk_app_id = self.sdk_app_id

        ui_app_id = self.ui_app_id

        endpoint = self.endpoint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userPoolId": user_pool_id,
                "sdkAppId": sdk_app_id,
                "uiAppId": ui_app_id,
                "endpoint": endpoint,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_pool_id = d.pop("userPoolId")

        sdk_app_id = d.pop("sdkAppId")

        ui_app_id = d.pop("uiAppId")

        endpoint = d.pop("endpoint")

        auth_info = cls(
            user_pool_id=user_pool_id,
            sdk_app_id=sdk_app_id,
            ui_app_id=ui_app_id,
            endpoint=endpoint,
        )

        auth_info.additional_properties = d
        return auth_info

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

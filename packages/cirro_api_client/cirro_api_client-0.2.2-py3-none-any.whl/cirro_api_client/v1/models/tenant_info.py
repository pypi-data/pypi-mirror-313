from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.feature_flags import FeatureFlags
    from ..models.login_provider import LoginProvider


T = TypeVar("T", bound="TenantInfo")


@_attrs_define
class TenantInfo:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        location (str):
        contact_email (str):
        tenant_logo_url (str):
        terms_of_service_url (str):
        privacy_policy_url (str):
        login_providers (List['LoginProvider']):
        features (FeatureFlags):
    """

    id: str
    name: str
    description: str
    location: str
    contact_email: str
    tenant_logo_url: str
    terms_of_service_url: str
    privacy_policy_url: str
    login_providers: List["LoginProvider"]
    features: "FeatureFlags"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        location = self.location

        contact_email = self.contact_email

        tenant_logo_url = self.tenant_logo_url

        terms_of_service_url = self.terms_of_service_url

        privacy_policy_url = self.privacy_policy_url

        login_providers = []
        for login_providers_item_data in self.login_providers:
            login_providers_item = login_providers_item_data.to_dict()
            login_providers.append(login_providers_item)

        features = self.features.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "location": location,
                "contactEmail": contact_email,
                "tenantLogoUrl": tenant_logo_url,
                "termsOfServiceUrl": terms_of_service_url,
                "privacyPolicyUrl": privacy_policy_url,
                "loginProviders": login_providers,
                "features": features,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.feature_flags import FeatureFlags
        from ..models.login_provider import LoginProvider

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        location = d.pop("location")

        contact_email = d.pop("contactEmail")

        tenant_logo_url = d.pop("tenantLogoUrl")

        terms_of_service_url = d.pop("termsOfServiceUrl")

        privacy_policy_url = d.pop("privacyPolicyUrl")

        login_providers = []
        _login_providers = d.pop("loginProviders")
        for login_providers_item_data in _login_providers:
            login_providers_item = LoginProvider.from_dict(login_providers_item_data)

            login_providers.append(login_providers_item)

        features = FeatureFlags.from_dict(d.pop("features"))

        tenant_info = cls(
            id=id,
            name=name,
            description=description,
            location=location,
            contact_email=contact_email,
            tenant_logo_url=tenant_logo_url,
            terms_of_service_url=terms_of_service_url,
            privacy_policy_url=privacy_policy_url,
            login_providers=login_providers,
            features=features,
        )

        tenant_info.additional_properties = d
        return tenant_info

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

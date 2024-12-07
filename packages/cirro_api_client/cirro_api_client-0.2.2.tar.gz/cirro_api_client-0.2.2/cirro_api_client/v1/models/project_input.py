from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_account import CloudAccount
    from ..models.contact import Contact
    from ..models.project_settings import ProjectSettings
    from ..models.tag import Tag


T = TypeVar("T", bound="ProjectInput")


@_attrs_define
class ProjectInput:
    """
    Attributes:
        name (str):
        description (str):
        billing_account_id (str):
        settings (ProjectSettings):
        contacts (List['Contact']):
        account (Union['CloudAccount', None, Unset]):
        classification_ids (Union[List[str], None, Unset]):
        tags (Union[List['Tag'], None, Unset]):
    """

    name: str
    description: str
    billing_account_id: str
    settings: "ProjectSettings"
    contacts: List["Contact"]
    account: Union["CloudAccount", None, Unset] = UNSET
    classification_ids: Union[List[str], None, Unset] = UNSET
    tags: Union[List["Tag"], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.cloud_account import CloudAccount

        name = self.name

        description = self.description

        billing_account_id = self.billing_account_id

        settings = self.settings.to_dict()

        contacts = []
        for contacts_item_data in self.contacts:
            contacts_item = contacts_item_data.to_dict()
            contacts.append(contacts_item)

        account: Union[Dict[str, Any], None, Unset]
        if isinstance(self.account, Unset):
            account = UNSET
        elif isinstance(self.account, CloudAccount):
            account = self.account.to_dict()
        else:
            account = self.account

        classification_ids: Union[List[str], None, Unset]
        if isinstance(self.classification_ids, Unset):
            classification_ids = UNSET
        elif isinstance(self.classification_ids, list):
            classification_ids = self.classification_ids

        else:
            classification_ids = self.classification_ids

        tags: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = []
            for tags_type_0_item_data in self.tags:
                tags_type_0_item = tags_type_0_item_data.to_dict()
                tags.append(tags_type_0_item)

        else:
            tags = self.tags

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "billingAccountId": billing_account_id,
                "settings": settings,
                "contacts": contacts,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account
        if classification_ids is not UNSET:
            field_dict["classificationIds"] = classification_ids
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cloud_account import CloudAccount
        from ..models.contact import Contact
        from ..models.project_settings import ProjectSettings
        from ..models.tag import Tag

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        billing_account_id = d.pop("billingAccountId")

        settings = ProjectSettings.from_dict(d.pop("settings"))

        contacts = []
        _contacts = d.pop("contacts")
        for contacts_item_data in _contacts:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        def _parse_account(data: object) -> Union["CloudAccount", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                account_type_1 = CloudAccount.from_dict(data)

                return account_type_1
            except:  # noqa: E722
                pass
            return cast(Union["CloudAccount", None, Unset], data)

        account = _parse_account(d.pop("account", UNSET))

        def _parse_classification_ids(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                classification_ids_type_0 = cast(List[str], data)

                return classification_ids_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        classification_ids = _parse_classification_ids(d.pop("classificationIds", UNSET))

        def _parse_tags(data: object) -> Union[List["Tag"], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = []
                _tags_type_0 = data
                for tags_type_0_item_data in _tags_type_0:
                    tags_type_0_item = Tag.from_dict(tags_type_0_item_data)

                    tags_type_0.append(tags_type_0_item)

                return tags_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List["Tag"], None, Unset], data)

        tags = _parse_tags(d.pop("tags", UNSET))

        project_input = cls(
            name=name,
            description=description,
            billing_account_id=billing_account_id,
            settings=settings,
            contacts=contacts,
            account=account,
            classification_ids=classification_ids,
            tags=tags,
        )

        project_input.additional_properties = d
        return project_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

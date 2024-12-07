import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.status import Status
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_account import CloudAccount
    from ..models.contact import Contact
    from ..models.project_settings import ProjectSettings
    from ..models.tag import Tag


T = TypeVar("T", bound="ProjectDetail")


@_attrs_define
class ProjectDetail:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        billing_account_id (str):
        contacts (List['Contact']):
        organization (str):
        status (Status):
        settings (ProjectSettings):
        status_message (str):
        tags (List['Tag']):
        classification_ids (List[str]):
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
        account (Union['CloudAccount', None, Unset]):
    """

    id: str
    name: str
    description: str
    billing_account_id: str
    contacts: List["Contact"]
    organization: str
    status: Status
    settings: "ProjectSettings"
    status_message: str
    tags: List["Tag"]
    classification_ids: List[str]
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    account: Union["CloudAccount", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.cloud_account import CloudAccount

        id = self.id

        name = self.name

        description = self.description

        billing_account_id = self.billing_account_id

        contacts = []
        for contacts_item_data in self.contacts:
            contacts_item = contacts_item_data.to_dict()
            contacts.append(contacts_item)

        organization = self.organization

        status = self.status.value

        settings = self.settings.to_dict()

        status_message = self.status_message

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        classification_ids = self.classification_ids

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        account: Union[Dict[str, Any], None, Unset]
        if isinstance(self.account, Unset):
            account = UNSET
        elif isinstance(self.account, CloudAccount):
            account = self.account.to_dict()
        else:
            account = self.account

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "billingAccountId": billing_account_id,
                "contacts": contacts,
                "organization": organization,
                "status": status,
                "settings": settings,
                "statusMessage": status_message,
                "tags": tags,
                "classificationIds": classification_ids,
                "createdBy": created_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )
        if account is not UNSET:
            field_dict["account"] = account

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.cloud_account import CloudAccount
        from ..models.contact import Contact
        from ..models.project_settings import ProjectSettings
        from ..models.tag import Tag

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        billing_account_id = d.pop("billingAccountId")

        contacts = []
        _contacts = d.pop("contacts")
        for contacts_item_data in _contacts:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        organization = d.pop("organization")

        status = Status(d.pop("status"))

        settings = ProjectSettings.from_dict(d.pop("settings"))

        status_message = d.pop("statusMessage")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = Tag.from_dict(tags_item_data)

            tags.append(tags_item)

        classification_ids = cast(List[str], d.pop("classificationIds"))

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

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

        project_detail = cls(
            id=id,
            name=name,
            description=description,
            billing_account_id=billing_account_id,
            contacts=contacts,
            organization=organization,
            status=status,
            settings=settings,
            status_message=status_message,
            tags=tags,
            classification_ids=classification_ids,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
            account=account,
        )

        project_detail.additional_properties = d
        return project_detail

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

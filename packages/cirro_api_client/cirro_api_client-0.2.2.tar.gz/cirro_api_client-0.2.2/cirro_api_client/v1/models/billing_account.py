from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.billing_method import BillingMethod
from ..models.customer_type import CustomerType

if TYPE_CHECKING:
    from ..models.contact import Contact


T = TypeVar("T", bound="BillingAccount")


@_attrs_define
class BillingAccount:
    """
    Attributes:
        id (str):
        name (str):
        organization (str):
        contacts (List['Contact']):
        customer_type (CustomerType):
        billing_method (BillingMethod):
        primary_budget_number (str):
        owner (str):
        shared_with (List[str]):
        is_archived (bool):
    """

    id: str
    name: str
    organization: str
    contacts: List["Contact"]
    customer_type: CustomerType
    billing_method: BillingMethod
    primary_budget_number: str
    owner: str
    shared_with: List[str]
    is_archived: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        organization = self.organization

        contacts = []
        for contacts_item_data in self.contacts:
            contacts_item = contacts_item_data.to_dict()
            contacts.append(contacts_item)

        customer_type = self.customer_type.value

        billing_method = self.billing_method.value

        primary_budget_number = self.primary_budget_number

        owner = self.owner

        shared_with = self.shared_with

        is_archived = self.is_archived

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "organization": organization,
                "contacts": contacts,
                "customerType": customer_type,
                "billingMethod": billing_method,
                "primaryBudgetNumber": primary_budget_number,
                "owner": owner,
                "sharedWith": shared_with,
                "isArchived": is_archived,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.contact import Contact

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        organization = d.pop("organization")

        contacts = []
        _contacts = d.pop("contacts")
        for contacts_item_data in _contacts:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        customer_type = CustomerType(d.pop("customerType"))

        billing_method = BillingMethod(d.pop("billingMethod"))

        primary_budget_number = d.pop("primaryBudgetNumber")

        owner = d.pop("owner")

        shared_with = cast(List[str], d.pop("sharedWith"))

        is_archived = d.pop("isArchived")

        billing_account = cls(
            id=id,
            name=name,
            organization=organization,
            contacts=contacts,
            customer_type=customer_type,
            billing_method=billing_method,
            primary_budget_number=primary_budget_number,
            owner=owner,
            shared_with=shared_with,
            is_archived=is_archived,
        )

        billing_account.additional_properties = d
        return billing_account

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

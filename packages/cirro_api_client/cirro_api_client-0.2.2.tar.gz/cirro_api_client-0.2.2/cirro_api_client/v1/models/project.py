from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.status import Status

if TYPE_CHECKING:
    from ..models.tag import Tag


T = TypeVar("T", bound="Project")


@_attrs_define
class Project:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        status (Status):
        tags (List['Tag']):
        organization (str):
        classification_ids (List[str]):
        billing_account_id (str):
    """

    id: str
    name: str
    description: str
    status: Status
    tags: List["Tag"]
    organization: str
    classification_ids: List[str]
    billing_account_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        status = self.status.value

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        organization = self.organization

        classification_ids = self.classification_ids

        billing_account_id = self.billing_account_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "status": status,
                "tags": tags,
                "organization": organization,
                "classificationIds": classification_ids,
                "billingAccountId": billing_account_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tag import Tag

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        status = Status(d.pop("status"))

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = Tag.from_dict(tags_item_data)

            tags.append(tags_item)

        organization = d.pop("organization")

        classification_ids = cast(List[str], d.pop("classificationIds"))

        billing_account_id = d.pop("billingAccountId")

        project = cls(
            id=id,
            name=name,
            description=description,
            status=status,
            tags=tags,
            organization=organization,
            classification_ids=classification_ids,
            billing_account_id=billing_account_id,
        )

        project.additional_properties = d
        return project

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

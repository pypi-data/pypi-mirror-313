from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectRequest")


@_attrs_define
class ProjectRequest:
    """
    Attributes:
        name (str):
        description (str):
        classification_ids (List[str]):
        billing_info (str):
        admin_username (str):
        message (str):
    """

    name: str
    description: str
    classification_ids: List[str]
    billing_info: str
    admin_username: str
    message: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        classification_ids = self.classification_ids

        billing_info = self.billing_info

        admin_username = self.admin_username

        message = self.message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "classificationIds": classification_ids,
                "billingInfo": billing_info,
                "adminUsername": admin_username,
                "message": message,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        classification_ids = cast(List[str], d.pop("classificationIds"))

        billing_info = d.pop("billingInfo")

        admin_username = d.pop("adminUsername")

        message = d.pop("message")

        project_request = cls(
            name=name,
            description=description,
            classification_ids=classification_ids,
            billing_info=billing_info,
            admin_username=admin_username,
            message=message,
        )

        project_request.additional_properties = d
        return project_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

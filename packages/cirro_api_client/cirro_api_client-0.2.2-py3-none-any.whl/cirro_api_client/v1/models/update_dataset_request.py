from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.tag import Tag


T = TypeVar("T", bound="UpdateDatasetRequest")


@_attrs_define
class UpdateDatasetRequest:
    """
    Attributes:
        name (str):
        description (str):
        process_id (str):
        tags (List['Tag']):
    """

    name: str
    description: str
    process_id: str
    tags: List["Tag"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        process_id = self.process_id

        tags = []
        for tags_item_data in self.tags:
            tags_item = tags_item_data.to_dict()
            tags.append(tags_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "processId": process_id,
                "tags": tags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tag import Tag

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        process_id = d.pop("processId")

        tags = []
        _tags = d.pop("tags")
        for tags_item_data in _tags:
            tags_item = Tag.from_dict(tags_item_data)

            tags.append(tags_item)

        update_dataset_request = cls(
            name=name,
            description=description,
            process_id=process_id,
            tags=tags,
        )

        update_dataset_request.additional_properties = d
        return update_dataset_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

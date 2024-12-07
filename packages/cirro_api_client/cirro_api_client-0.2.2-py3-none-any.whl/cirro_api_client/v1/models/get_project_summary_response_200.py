from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.task import Task


T = TypeVar("T", bound="GetProjectSummaryResponse200")


@_attrs_define
class GetProjectSummaryResponse200:
    """ """

    additional_properties: Dict[str, List["Task"]] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = []
            for additional_property_item_data in prop:
                additional_property_item = additional_property_item_data.to_dict()
                field_dict[prop_name].append(additional_property_item)

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.task import Task

        d = src_dict.copy()
        get_project_summary_response_200 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = []
            _additional_property = prop_dict
            for additional_property_item_data in _additional_property:
                additional_property_item = Task.from_dict(additional_property_item_data)

                additional_property.append(additional_property_item)

            additional_properties[prop_name] = additional_property

        get_project_summary_response_200.additional_properties = additional_properties
        return get_project_summary_response_200

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

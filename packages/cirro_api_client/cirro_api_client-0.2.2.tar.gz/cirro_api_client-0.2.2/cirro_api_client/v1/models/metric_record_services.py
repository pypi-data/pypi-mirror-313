from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MetricRecordServices")


@_attrs_define
class MetricRecordServices:
    """Map of service names to metric value

    Example:
        {'Amazon Simple Storage Service': 24.91}

    """

    additional_properties: Dict[str, float] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metric_record_services = cls()

        metric_record_services.additional_properties = d
        return metric_record_services

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_record_services import MetricRecordServices


T = TypeVar("T", bound="MetricRecord")


@_attrs_define
class MetricRecord:
    """
    Attributes:
        unit (str):
        date (Union[Unset, datetime.date]): Date in ISO 8601 format
        services (Union[Unset, MetricRecordServices]): Map of service names to metric value Example: {'Amazon Simple
            Storage Service': 24.91}.
    """

    unit: str
    date: Union[Unset, datetime.date] = UNSET
    services: Union[Unset, "MetricRecordServices"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        unit = self.unit

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        services: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.services, Unset):
            services = self.services.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unit": unit,
            }
        )
        if date is not UNSET:
            field_dict["date"] = date
        if services is not UNSET:
            field_dict["services"] = services

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_record_services import MetricRecordServices

        d = src_dict.copy()
        unit = d.pop("unit")

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        _services = d.pop("services", UNSET)
        services: Union[Unset, MetricRecordServices]
        if isinstance(_services, Unset):
            services = UNSET
        else:
            services = MetricRecordServices.from_dict(_services)

        metric_record = cls(
            unit=unit,
            date=date,
            services=services,
        )

        metric_record.additional_properties = d
        return metric_record

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

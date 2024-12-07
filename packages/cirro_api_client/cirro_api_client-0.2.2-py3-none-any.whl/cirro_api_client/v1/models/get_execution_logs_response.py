from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_entry import LogEntry


T = TypeVar("T", bound="GetExecutionLogsResponse")


@_attrs_define
class GetExecutionLogsResponse:
    """
    Attributes:
        events (List['LogEntry']):
    """

    events: List["LogEntry"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()
            events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_entry import LogEntry

        d = src_dict.copy()
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = LogEntry.from_dict(events_item_data)

            events.append(events_item)

        get_execution_logs_response = cls(
            events=events,
        )

        get_execution_logs_response.additional_properties = d
        return get_execution_logs_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

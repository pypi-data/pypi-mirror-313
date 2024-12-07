from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.dashboard_request_dashboard_data import DashboardRequestDashboardData
    from ..models.dashboard_request_info import DashboardRequestInfo


T = TypeVar("T", bound="DashboardRequest")


@_attrs_define
class DashboardRequest:
    """
    Attributes:
        name (str):
        description (str):
        process_ids (List[str]):
        dashboard_data (DashboardRequestDashboardData):
        info (DashboardRequestInfo):
    """

    name: str
    description: str
    process_ids: List[str]
    dashboard_data: "DashboardRequestDashboardData"
    info: "DashboardRequestInfo"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        process_ids = self.process_ids

        dashboard_data = self.dashboard_data.to_dict()

        info = self.info.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "processIds": process_ids,
                "dashboardData": dashboard_data,
                "info": info,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dashboard_request_dashboard_data import DashboardRequestDashboardData
        from ..models.dashboard_request_info import DashboardRequestInfo

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        process_ids = cast(List[str], d.pop("processIds"))

        dashboard_data = DashboardRequestDashboardData.from_dict(d.pop("dashboardData"))

        info = DashboardRequestInfo.from_dict(d.pop("info"))

        dashboard_request = cls(
            name=name,
            description=description,
            process_ids=process_ids,
            dashboard_data=dashboard_data,
            info=info,
        )

        dashboard_request.additional_properties = d
        return dashboard_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

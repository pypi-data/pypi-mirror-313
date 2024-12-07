import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.dashboard_dashboard_data import DashboardDashboardData
    from ..models.dashboard_info import DashboardInfo


T = TypeVar("T", bound="Dashboard")


@_attrs_define
class Dashboard:
    """
    Attributes:
        id (str):
        name (str):
        description (str):
        process_ids (List[str]):
        dashboard_data (DashboardDashboardData):
        info (DashboardInfo):
        created_by (str):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    name: str
    description: str
    process_ids: List[str]
    dashboard_data: "DashboardDashboardData"
    info: "DashboardInfo"
    created_by: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        process_ids = self.process_ids

        dashboard_data = self.dashboard_data.to_dict()

        info = self.info.to_dict()

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "processIds": process_ids,
                "dashboardData": dashboard_data,
                "info": info,
                "createdBy": created_by,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.dashboard_dashboard_data import DashboardDashboardData
        from ..models.dashboard_info import DashboardInfo

        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        process_ids = cast(List[str], d.pop("processIds"))

        dashboard_data = DashboardDashboardData.from_dict(d.pop("dashboardData"))

        info = DashboardInfo.from_dict(d.pop("info"))

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        dashboard = cls(
            id=id,
            name=name,
            description=description,
            process_ids=process_ids,
            dashboard_data=dashboard_data,
            info=info,
            created_by=created_by,
            created_at=created_at,
            updated_at=updated_at,
        )

        dashboard.additional_properties = d
        return dashboard

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

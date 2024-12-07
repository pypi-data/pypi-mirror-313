from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_record import MetricRecord


T = TypeVar("T", bound="ProjectMetrics")


@_attrs_define
class ProjectMetrics:
    """
    Attributes:
        project_id (str):
        costs (Union[Unset, List['MetricRecord']]): Costs by service by month Example: [{
              "date": "2022-11-01",
              "unit": "$",
              "service": {
                "Other": 26.47,
                "EC2 - Other": 3.66,
                "Amazon Elastic Compute Cloud - Compute": 140.59,
                "Amazon Simple Storage Service": 24.91,
                "AmazonCloudWatch": 2.09
              }
            }]
            .
        storage_metrics (Union[Unset, List['MetricRecord']]): Storage usage by tier by day Example: [{
                "date": "2023-12-12",
                "unit": "GB",
                "service": {
                    "IntelligentTieringAIAStorage": 4198.95,
                    "IntelligentTieringFAStorage": 1516.48,
                    "StandardStorage": 1.9,
                    "IntelligentTieringIAStorage": 2154.6
                }
            }]
            .
    """

    project_id: str
    costs: Union[Unset, List["MetricRecord"]] = UNSET
    storage_metrics: Union[Unset, List["MetricRecord"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        project_id = self.project_id

        costs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.costs, Unset):
            costs = []
            for costs_item_data in self.costs:
                costs_item = costs_item_data.to_dict()
                costs.append(costs_item)

        storage_metrics: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.storage_metrics, Unset):
            storage_metrics = []
            for storage_metrics_item_data in self.storage_metrics:
                storage_metrics_item = storage_metrics_item_data.to_dict()
                storage_metrics.append(storage_metrics_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "projectId": project_id,
            }
        )
        if costs is not UNSET:
            field_dict["costs"] = costs
        if storage_metrics is not UNSET:
            field_dict["storageMetrics"] = storage_metrics

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.metric_record import MetricRecord

        d = src_dict.copy()
        project_id = d.pop("projectId")

        costs = []
        _costs = d.pop("costs", UNSET)
        for costs_item_data in _costs or []:
            costs_item = MetricRecord.from_dict(costs_item_data)

            costs.append(costs_item)

        storage_metrics = []
        _storage_metrics = d.pop("storageMetrics", UNSET)
        for storage_metrics_item_data in _storage_metrics or []:
            storage_metrics_item = MetricRecord.from_dict(storage_metrics_item_data)

            storage_metrics.append(storage_metrics_item)

        project_metrics = cls(
            project_id=project_id,
            costs=costs,
            storage_metrics=storage_metrics,
        )

        project_metrics.additional_properties = d
        return project_metrics

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

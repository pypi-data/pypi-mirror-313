from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelineCost")


@_attrs_define
class PipelineCost:
    """
    Attributes:
        total_cost (Union[None, Unset, float]): The total cost of running the pipeline
        is_estimate (Union[Unset, bool]): Is this an estimate of the cost?
        description (Union[Unset, str]): Description of the cost calculation
    """

    total_cost: Union[None, Unset, float] = UNSET
    is_estimate: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        total_cost: Union[None, Unset, float]
        if isinstance(self.total_cost, Unset):
            total_cost = UNSET
        else:
            total_cost = self.total_cost

        is_estimate = self.is_estimate

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if total_cost is not UNSET:
            field_dict["totalCost"] = total_cost
        if is_estimate is not UNSET:
            field_dict["isEstimate"] = is_estimate
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_total_cost(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        total_cost = _parse_total_cost(d.pop("totalCost", UNSET))

        is_estimate = d.pop("isEstimate", UNSET)

        description = d.pop("description", UNSET)

        pipeline_cost = cls(
            total_cost=total_cost,
            is_estimate=is_estimate,
            description=description,
        )

        pipeline_cost.additional_properties = d
        return pipeline_cost

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

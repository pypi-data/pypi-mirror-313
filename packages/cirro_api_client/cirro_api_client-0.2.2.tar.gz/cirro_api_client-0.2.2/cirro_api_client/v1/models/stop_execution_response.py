from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="StopExecutionResponse")


@_attrs_define
class StopExecutionResponse:
    """
    Attributes:
        success (Union[Unset, List[str]]): List of job IDs that were successful in termination
        failed (Union[Unset, List[str]]): List of job IDs that were not successful in termination
    """

    success: Union[Unset, List[str]] = UNSET
    failed: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success: Union[Unset, List[str]] = UNSET
        if not isinstance(self.success, Unset):
            success = self.success

        failed: Union[Unset, List[str]] = UNSET
        if not isinstance(self.failed, Unset):
            failed = self.failed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if success is not UNSET:
            field_dict["success"] = success
        if failed is not UNSET:
            field_dict["failed"] = failed

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = cast(List[str], d.pop("success", UNSET))

        failed = cast(List[str], d.pop("failed", UNSET))

        stop_execution_response = cls(
            success=success,
            failed=failed,
        )

        stop_execution_response.additional_properties = d
        return stop_execution_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

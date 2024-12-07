from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.access_type import AccessType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FileAccessRequest")


@_attrs_define
class FileAccessRequest:
    """
    Attributes:
        access_type (AccessType):
        dataset_id (Union[None, Unset, str]):
        token_lifetime_hours (Union[None, Unset, int]):
    """

    access_type: AccessType
    dataset_id: Union[None, Unset, str] = UNSET
    token_lifetime_hours: Union[None, Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access_type = self.access_type.value

        dataset_id: Union[None, Unset, str]
        if isinstance(self.dataset_id, Unset):
            dataset_id = UNSET
        else:
            dataset_id = self.dataset_id

        token_lifetime_hours: Union[None, Unset, int]
        if isinstance(self.token_lifetime_hours, Unset):
            token_lifetime_hours = UNSET
        else:
            token_lifetime_hours = self.token_lifetime_hours

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accessType": access_type,
            }
        )
        if dataset_id is not UNSET:
            field_dict["datasetId"] = dataset_id
        if token_lifetime_hours is not UNSET:
            field_dict["tokenLifetimeHours"] = token_lifetime_hours

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_type = AccessType(d.pop("accessType"))

        def _parse_dataset_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        dataset_id = _parse_dataset_id(d.pop("datasetId", UNSET))

        def _parse_token_lifetime_hours(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        token_lifetime_hours = _parse_token_lifetime_hours(d.pop("tokenLifetimeHours", UNSET))

        file_access_request = cls(
            access_type=access_type,
            dataset_id=dataset_id,
            token_lifetime_hours=token_lifetime_hours,
        )

        file_access_request.additional_properties = d
        return file_access_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

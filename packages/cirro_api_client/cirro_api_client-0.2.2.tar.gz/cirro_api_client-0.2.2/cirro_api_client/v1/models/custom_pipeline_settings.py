import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sync_status import SyncStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomPipelineSettings")


@_attrs_define
class CustomPipelineSettings:
    """Used to describe the location of the process definition dependencies

    Attributes:
        repository (str): GitHub repository that contains the process definition Example: CirroBio/my-pipeline.
        branch (Union[Unset, str]): Branch, tag, or commit hash of the repo that contains the process definition
            Default: 'main'.
        folder (Union[Unset, str]): Folder within the repo that contains the process definition Default: '.cirro'.
        last_sync (Union[None, Unset, datetime.datetime]): Time of last sync
        sync_status (Union[None, SyncStatus, Unset]):
        commit_hash (Union[None, Unset, str]): Commit hash of the last successful sync
        is_authorized (Union[Unset, bool]): Whether we are authorized to access the repository Default: False.
    """

    repository: str
    branch: Union[Unset, str] = "main"
    folder: Union[Unset, str] = ".cirro"
    last_sync: Union[None, Unset, datetime.datetime] = UNSET
    sync_status: Union[None, SyncStatus, Unset] = UNSET
    commit_hash: Union[None, Unset, str] = UNSET
    is_authorized: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        repository = self.repository

        branch = self.branch

        folder = self.folder

        last_sync: Union[None, Unset, str]
        if isinstance(self.last_sync, Unset):
            last_sync = UNSET
        elif isinstance(self.last_sync, datetime.datetime):
            last_sync = self.last_sync.isoformat()
        else:
            last_sync = self.last_sync

        sync_status: Union[None, Unset, str]
        if isinstance(self.sync_status, Unset):
            sync_status = UNSET
        elif isinstance(self.sync_status, SyncStatus):
            sync_status = self.sync_status.value
        else:
            sync_status = self.sync_status

        commit_hash: Union[None, Unset, str]
        if isinstance(self.commit_hash, Unset):
            commit_hash = UNSET
        else:
            commit_hash = self.commit_hash

        is_authorized = self.is_authorized

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repository": repository,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch
        if folder is not UNSET:
            field_dict["folder"] = folder
        if last_sync is not UNSET:
            field_dict["lastSync"] = last_sync
        if sync_status is not UNSET:
            field_dict["syncStatus"] = sync_status
        if commit_hash is not UNSET:
            field_dict["commitHash"] = commit_hash
        if is_authorized is not UNSET:
            field_dict["isAuthorized"] = is_authorized

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        repository = d.pop("repository")

        branch = d.pop("branch", UNSET)

        folder = d.pop("folder", UNSET)

        def _parse_last_sync(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sync_type_0 = isoparse(data)

                return last_sync_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        last_sync = _parse_last_sync(d.pop("lastSync", UNSET))

        def _parse_sync_status(data: object) -> Union[None, SyncStatus, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                sync_status_type_1 = SyncStatus(data)

                return sync_status_type_1
            except:  # noqa: E722
                pass
            return cast(Union[None, SyncStatus, Unset], data)

        sync_status = _parse_sync_status(d.pop("syncStatus", UNSET))

        def _parse_commit_hash(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        commit_hash = _parse_commit_hash(d.pop("commitHash", UNSET))

        is_authorized = d.pop("isAuthorized", UNSET)

        custom_pipeline_settings = cls(
            repository=repository,
            branch=branch,
            folder=folder,
            last_sync=last_sync,
            sync_status=sync_status,
            commit_hash=commit_hash,
            is_authorized=is_authorized,
        )

        custom_pipeline_settings.additional_properties = d
        return custom_pipeline_settings

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

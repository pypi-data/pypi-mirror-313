import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_http_triggers_response_200_item_http_method import ListHttpTriggersResponse200ItemHttpMethod
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_http_triggers_response_200_item_extra_perms import ListHttpTriggersResponse200ItemExtraPerms
    from ..models.list_http_triggers_response_200_item_static_asset_config import (
        ListHttpTriggersResponse200ItemStaticAssetConfig,
    )


T = TypeVar("T", bound="ListHttpTriggersResponse200Item")


@_attrs_define
class ListHttpTriggersResponse200Item:
    """
    Attributes:
        path (str):
        edited_by (str):
        edited_at (datetime.datetime):
        script_path (str):
        route_path (str):
        is_flow (bool):
        extra_perms (ListHttpTriggersResponse200ItemExtraPerms):
        email (str):
        workspace_id (str):
        http_method (ListHttpTriggersResponse200ItemHttpMethod):
        is_async (bool):
        requires_auth (bool):
        static_asset_config (Union[Unset, ListHttpTriggersResponse200ItemStaticAssetConfig]):
    """

    path: str
    edited_by: str
    edited_at: datetime.datetime
    script_path: str
    route_path: str
    is_flow: bool
    extra_perms: "ListHttpTriggersResponse200ItemExtraPerms"
    email: str
    workspace_id: str
    http_method: ListHttpTriggersResponse200ItemHttpMethod
    is_async: bool
    requires_auth: bool
    static_asset_config: Union[Unset, "ListHttpTriggersResponse200ItemStaticAssetConfig"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        script_path = self.script_path
        route_path = self.route_path
        is_flow = self.is_flow
        extra_perms = self.extra_perms.to_dict()

        email = self.email
        workspace_id = self.workspace_id
        http_method = self.http_method.value

        is_async = self.is_async
        requires_auth = self.requires_auth
        static_asset_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.static_asset_config, Unset):
            static_asset_config = self.static_asset_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "script_path": script_path,
                "route_path": route_path,
                "is_flow": is_flow,
                "extra_perms": extra_perms,
                "email": email,
                "workspace_id": workspace_id,
                "http_method": http_method,
                "is_async": is_async,
                "requires_auth": requires_auth,
            }
        )
        if static_asset_config is not UNSET:
            field_dict["static_asset_config"] = static_asset_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_http_triggers_response_200_item_extra_perms import ListHttpTriggersResponse200ItemExtraPerms
        from ..models.list_http_triggers_response_200_item_static_asset_config import (
            ListHttpTriggersResponse200ItemStaticAssetConfig,
        )

        d = src_dict.copy()
        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        script_path = d.pop("script_path")

        route_path = d.pop("route_path")

        is_flow = d.pop("is_flow")

        extra_perms = ListHttpTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        email = d.pop("email")

        workspace_id = d.pop("workspace_id")

        http_method = ListHttpTriggersResponse200ItemHttpMethod(d.pop("http_method"))

        is_async = d.pop("is_async")

        requires_auth = d.pop("requires_auth")

        _static_asset_config = d.pop("static_asset_config", UNSET)
        static_asset_config: Union[Unset, ListHttpTriggersResponse200ItemStaticAssetConfig]
        if isinstance(_static_asset_config, Unset):
            static_asset_config = UNSET
        else:
            static_asset_config = ListHttpTriggersResponse200ItemStaticAssetConfig.from_dict(_static_asset_config)

        list_http_triggers_response_200_item = cls(
            path=path,
            edited_by=edited_by,
            edited_at=edited_at,
            script_path=script_path,
            route_path=route_path,
            is_flow=is_flow,
            extra_perms=extra_perms,
            email=email,
            workspace_id=workspace_id,
            http_method=http_method,
            is_async=is_async,
            requires_auth=requires_auth,
            static_asset_config=static_asset_config,
        )

        list_http_triggers_response_200_item.additional_properties = d
        return list_http_triggers_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

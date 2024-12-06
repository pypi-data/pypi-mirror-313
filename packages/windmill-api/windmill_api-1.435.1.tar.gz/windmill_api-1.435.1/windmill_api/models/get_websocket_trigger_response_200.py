import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_websocket_trigger_response_200_extra_perms import GetWebsocketTriggerResponse200ExtraPerms
    from ..models.get_websocket_trigger_response_200_filters_item import GetWebsocketTriggerResponse200FiltersItem
    from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
        GetWebsocketTriggerResponse200InitialMessagesItemType0,
    )
    from ..models.get_websocket_trigger_response_200_initial_messages_item_type_1 import (
        GetWebsocketTriggerResponse200InitialMessagesItemType1,
    )
    from ..models.get_websocket_trigger_response_200_url_runnable_args import (
        GetWebsocketTriggerResponse200UrlRunnableArgs,
    )


T = TypeVar("T", bound="GetWebsocketTriggerResponse200")


@_attrs_define
class GetWebsocketTriggerResponse200:
    """
    Attributes:
        path (str):
        edited_by (str):
        edited_at (datetime.datetime):
        script_path (str):
        url (str):
        is_flow (bool):
        extra_perms (GetWebsocketTriggerResponse200ExtraPerms):
        email (str):
        workspace_id (str):
        enabled (bool):
        filters (List['GetWebsocketTriggerResponse200FiltersItem']):
        initial_messages (List[Union['GetWebsocketTriggerResponse200InitialMessagesItemType0',
            'GetWebsocketTriggerResponse200InitialMessagesItemType1']]):
        url_runnable_args (GetWebsocketTriggerResponse200UrlRunnableArgs):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
    """

    path: str
    edited_by: str
    edited_at: datetime.datetime
    script_path: str
    url: str
    is_flow: bool
    extra_perms: "GetWebsocketTriggerResponse200ExtraPerms"
    email: str
    workspace_id: str
    enabled: bool
    filters: List["GetWebsocketTriggerResponse200FiltersItem"]
    initial_messages: List[
        Union[
            "GetWebsocketTriggerResponse200InitialMessagesItemType0",
            "GetWebsocketTriggerResponse200InitialMessagesItemType1",
        ]
    ]
    url_runnable_args: "GetWebsocketTriggerResponse200UrlRunnableArgs"
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType0,
        )

        path = self.path
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        script_path = self.script_path
        url = self.url
        is_flow = self.is_flow
        extra_perms = self.extra_perms.to_dict()

        email = self.email
        workspace_id = self.workspace_id
        enabled = self.enabled
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        initial_messages = []
        for initial_messages_item_data in self.initial_messages:
            initial_messages_item: Dict[str, Any]

            if isinstance(initial_messages_item_data, GetWebsocketTriggerResponse200InitialMessagesItemType0):
                initial_messages_item = initial_messages_item_data.to_dict()

            else:
                initial_messages_item = initial_messages_item_data.to_dict()

            initial_messages.append(initial_messages_item)

        url_runnable_args = self.url_runnable_args.to_dict()

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "script_path": script_path,
                "url": url,
                "is_flow": is_flow,
                "extra_perms": extra_perms,
                "email": email,
                "workspace_id": workspace_id,
                "enabled": enabled,
                "filters": filters,
                "initial_messages": initial_messages,
                "url_runnable_args": url_runnable_args,
            }
        )
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_websocket_trigger_response_200_extra_perms import GetWebsocketTriggerResponse200ExtraPerms
        from ..models.get_websocket_trigger_response_200_filters_item import GetWebsocketTriggerResponse200FiltersItem
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_0 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType0,
        )
        from ..models.get_websocket_trigger_response_200_initial_messages_item_type_1 import (
            GetWebsocketTriggerResponse200InitialMessagesItemType1,
        )
        from ..models.get_websocket_trigger_response_200_url_runnable_args import (
            GetWebsocketTriggerResponse200UrlRunnableArgs,
        )

        d = src_dict.copy()
        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        script_path = d.pop("script_path")

        url = d.pop("url")

        is_flow = d.pop("is_flow")

        extra_perms = GetWebsocketTriggerResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        email = d.pop("email")

        workspace_id = d.pop("workspace_id")

        enabled = d.pop("enabled")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = GetWebsocketTriggerResponse200FiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        initial_messages = []
        _initial_messages = d.pop("initial_messages")
        for initial_messages_item_data in _initial_messages:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "GetWebsocketTriggerResponse200InitialMessagesItemType0",
                "GetWebsocketTriggerResponse200InitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = GetWebsocketTriggerResponse200InitialMessagesItemType0.from_dict(
                        data
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = GetWebsocketTriggerResponse200InitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        url_runnable_args = GetWebsocketTriggerResponse200UrlRunnableArgs.from_dict(d.pop("url_runnable_args"))

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        get_websocket_trigger_response_200 = cls(
            path=path,
            edited_by=edited_by,
            edited_at=edited_at,
            script_path=script_path,
            url=url,
            is_flow=is_flow,
            extra_perms=extra_perms,
            email=email,
            workspace_id=workspace_id,
            enabled=enabled,
            filters=filters,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
        )

        get_websocket_trigger_response_200.additional_properties = d
        return get_websocket_trigger_response_200

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

from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_websocket_trigger_json_body_filters_item import CreateWebsocketTriggerJsonBodyFiltersItem
    from ..models.create_websocket_trigger_json_body_initial_messages_item_type_0 import (
        CreateWebsocketTriggerJsonBodyInitialMessagesItemType0,
    )
    from ..models.create_websocket_trigger_json_body_initial_messages_item_type_1 import (
        CreateWebsocketTriggerJsonBodyInitialMessagesItemType1,
    )
    from ..models.create_websocket_trigger_json_body_url_runnable_args import (
        CreateWebsocketTriggerJsonBodyUrlRunnableArgs,
    )


T = TypeVar("T", bound="CreateWebsocketTriggerJsonBody")


@_attrs_define
class CreateWebsocketTriggerJsonBody:
    """
    Attributes:
        path (str):
        script_path (str):
        is_flow (bool):
        url (str):
        filters (List['CreateWebsocketTriggerJsonBodyFiltersItem']):
        initial_messages (List[Union['CreateWebsocketTriggerJsonBodyInitialMessagesItemType0',
            'CreateWebsocketTriggerJsonBodyInitialMessagesItemType1']]):
        url_runnable_args (CreateWebsocketTriggerJsonBodyUrlRunnableArgs):
        enabled (Union[Unset, bool]):
    """

    path: str
    script_path: str
    is_flow: bool
    url: str
    filters: List["CreateWebsocketTriggerJsonBodyFiltersItem"]
    initial_messages: List[
        Union[
            "CreateWebsocketTriggerJsonBodyInitialMessagesItemType0",
            "CreateWebsocketTriggerJsonBodyInitialMessagesItemType1",
        ]
    ]
    url_runnable_args: "CreateWebsocketTriggerJsonBodyUrlRunnableArgs"
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_websocket_trigger_json_body_initial_messages_item_type_0 import (
            CreateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        url = self.url
        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        initial_messages = []
        for initial_messages_item_data in self.initial_messages:
            initial_messages_item: Dict[str, Any]

            if isinstance(initial_messages_item_data, CreateWebsocketTriggerJsonBodyInitialMessagesItemType0):
                initial_messages_item = initial_messages_item_data.to_dict()

            else:
                initial_messages_item = initial_messages_item_data.to_dict()

            initial_messages.append(initial_messages_item)

        url_runnable_args = self.url_runnable_args.to_dict()

        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "url": url,
                "filters": filters,
                "initial_messages": initial_messages,
                "url_runnable_args": url_runnable_args,
            }
        )
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_websocket_trigger_json_body_filters_item import CreateWebsocketTriggerJsonBodyFiltersItem
        from ..models.create_websocket_trigger_json_body_initial_messages_item_type_0 import (
            CreateWebsocketTriggerJsonBodyInitialMessagesItemType0,
        )
        from ..models.create_websocket_trigger_json_body_initial_messages_item_type_1 import (
            CreateWebsocketTriggerJsonBodyInitialMessagesItemType1,
        )
        from ..models.create_websocket_trigger_json_body_url_runnable_args import (
            CreateWebsocketTriggerJsonBodyUrlRunnableArgs,
        )

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        url = d.pop("url")

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = CreateWebsocketTriggerJsonBodyFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        initial_messages = []
        _initial_messages = d.pop("initial_messages")
        for initial_messages_item_data in _initial_messages:

            def _parse_initial_messages_item(
                data: object,
            ) -> Union[
                "CreateWebsocketTriggerJsonBodyInitialMessagesItemType0",
                "CreateWebsocketTriggerJsonBodyInitialMessagesItemType1",
            ]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    initial_messages_item_type_0 = CreateWebsocketTriggerJsonBodyInitialMessagesItemType0.from_dict(
                        data
                    )

                    return initial_messages_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                initial_messages_item_type_1 = CreateWebsocketTriggerJsonBodyInitialMessagesItemType1.from_dict(data)

                return initial_messages_item_type_1

            initial_messages_item = _parse_initial_messages_item(initial_messages_item_data)

            initial_messages.append(initial_messages_item)

        url_runnable_args = CreateWebsocketTriggerJsonBodyUrlRunnableArgs.from_dict(d.pop("url_runnable_args"))

        enabled = d.pop("enabled", UNSET)

        create_websocket_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            url=url,
            filters=filters,
            initial_messages=initial_messages,
            url_runnable_args=url_runnable_args,
            enabled=enabled,
        )

        create_websocket_trigger_json_body.additional_properties = d
        return create_websocket_trigger_json_body

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

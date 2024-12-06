from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.edit_copilot_config_json_body_ai_resource import EditCopilotConfigJsonBodyAiResource


T = TypeVar("T", bound="EditCopilotConfigJsonBody")


@_attrs_define
class EditCopilotConfigJsonBody:
    """
    Attributes:
        code_completion_enabled (bool):
        ai_resource (Union[Unset, EditCopilotConfigJsonBodyAiResource]):
    """

    code_completion_enabled: bool
    ai_resource: Union[Unset, "EditCopilotConfigJsonBodyAiResource"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code_completion_enabled = self.code_completion_enabled
        ai_resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ai_resource, Unset):
            ai_resource = self.ai_resource.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code_completion_enabled": code_completion_enabled,
            }
        )
        if ai_resource is not UNSET:
            field_dict["ai_resource"] = ai_resource

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.edit_copilot_config_json_body_ai_resource import EditCopilotConfigJsonBodyAiResource

        d = src_dict.copy()
        code_completion_enabled = d.pop("code_completion_enabled")

        _ai_resource = d.pop("ai_resource", UNSET)
        ai_resource: Union[Unset, EditCopilotConfigJsonBodyAiResource]
        if isinstance(_ai_resource, Unset):
            ai_resource = UNSET
        else:
            ai_resource = EditCopilotConfigJsonBodyAiResource.from_dict(_ai_resource)

        edit_copilot_config_json_body = cls(
            code_completion_enabled=code_completion_enabled,
            ai_resource=ai_resource,
        )

        edit_copilot_config_json_body.additional_properties = d
        return edit_copilot_config_json_body

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

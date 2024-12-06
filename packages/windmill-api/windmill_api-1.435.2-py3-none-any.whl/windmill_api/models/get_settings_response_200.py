from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_settings_response_200_ai_resource import GetSettingsResponse200AiResource
    from ..models.get_settings_response_200_default_scripts import GetSettingsResponse200DefaultScripts
    from ..models.get_settings_response_200_deploy_ui import GetSettingsResponse200DeployUi
    from ..models.get_settings_response_200_error_handler_extra_args import GetSettingsResponse200ErrorHandlerExtraArgs
    from ..models.get_settings_response_200_git_sync import GetSettingsResponse200GitSync
    from ..models.get_settings_response_200_large_file_storage import GetSettingsResponse200LargeFileStorage


T = TypeVar("T", bound="GetSettingsResponse200")


@_attrs_define
class GetSettingsResponse200:
    """
    Attributes:
        automatic_billing (bool):
        code_completion_enabled (bool):
        error_handler_muted_on_cancel (bool):
        workspace_id (Union[Unset, str]):
        slack_name (Union[Unset, str]):
        slack_team_id (Union[Unset, str]):
        slack_command_script (Union[Unset, str]):
        auto_invite_domain (Union[Unset, str]):
        auto_invite_operator (Union[Unset, bool]):
        auto_add (Union[Unset, bool]):
        plan (Union[Unset, str]):
        customer_id (Union[Unset, str]):
        webhook (Union[Unset, str]):
        deploy_to (Union[Unset, str]):
        ai_resource (Union[Unset, GetSettingsResponse200AiResource]):
        error_handler (Union[Unset, str]):
        error_handler_extra_args (Union[Unset, GetSettingsResponse200ErrorHandlerExtraArgs]):
        large_file_storage (Union[Unset, GetSettingsResponse200LargeFileStorage]):
        git_sync (Union[Unset, GetSettingsResponse200GitSync]):
        deploy_ui (Union[Unset, GetSettingsResponse200DeployUi]):
        default_app (Union[Unset, str]):
        default_scripts (Union[Unset, GetSettingsResponse200DefaultScripts]):
        mute_critical_alerts (Union[Unset, bool]):
    """

    automatic_billing: bool
    code_completion_enabled: bool
    error_handler_muted_on_cancel: bool
    workspace_id: Union[Unset, str] = UNSET
    slack_name: Union[Unset, str] = UNSET
    slack_team_id: Union[Unset, str] = UNSET
    slack_command_script: Union[Unset, str] = UNSET
    auto_invite_domain: Union[Unset, str] = UNSET
    auto_invite_operator: Union[Unset, bool] = UNSET
    auto_add: Union[Unset, bool] = UNSET
    plan: Union[Unset, str] = UNSET
    customer_id: Union[Unset, str] = UNSET
    webhook: Union[Unset, str] = UNSET
    deploy_to: Union[Unset, str] = UNSET
    ai_resource: Union[Unset, "GetSettingsResponse200AiResource"] = UNSET
    error_handler: Union[Unset, str] = UNSET
    error_handler_extra_args: Union[Unset, "GetSettingsResponse200ErrorHandlerExtraArgs"] = UNSET
    large_file_storage: Union[Unset, "GetSettingsResponse200LargeFileStorage"] = UNSET
    git_sync: Union[Unset, "GetSettingsResponse200GitSync"] = UNSET
    deploy_ui: Union[Unset, "GetSettingsResponse200DeployUi"] = UNSET
    default_app: Union[Unset, str] = UNSET
    default_scripts: Union[Unset, "GetSettingsResponse200DefaultScripts"] = UNSET
    mute_critical_alerts: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        automatic_billing = self.automatic_billing
        code_completion_enabled = self.code_completion_enabled
        error_handler_muted_on_cancel = self.error_handler_muted_on_cancel
        workspace_id = self.workspace_id
        slack_name = self.slack_name
        slack_team_id = self.slack_team_id
        slack_command_script = self.slack_command_script
        auto_invite_domain = self.auto_invite_domain
        auto_invite_operator = self.auto_invite_operator
        auto_add = self.auto_add
        plan = self.plan
        customer_id = self.customer_id
        webhook = self.webhook
        deploy_to = self.deploy_to
        ai_resource: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.ai_resource, Unset):
            ai_resource = self.ai_resource.to_dict()

        error_handler = self.error_handler
        error_handler_extra_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_extra_args, Unset):
            error_handler_extra_args = self.error_handler_extra_args.to_dict()

        large_file_storage: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.large_file_storage, Unset):
            large_file_storage = self.large_file_storage.to_dict()

        git_sync: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.git_sync, Unset):
            git_sync = self.git_sync.to_dict()

        deploy_ui: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.deploy_ui, Unset):
            deploy_ui = self.deploy_ui.to_dict()

        default_app = self.default_app
        default_scripts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.default_scripts, Unset):
            default_scripts = self.default_scripts.to_dict()

        mute_critical_alerts = self.mute_critical_alerts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "automatic_billing": automatic_billing,
                "code_completion_enabled": code_completion_enabled,
                "error_handler_muted_on_cancel": error_handler_muted_on_cancel,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if slack_name is not UNSET:
            field_dict["slack_name"] = slack_name
        if slack_team_id is not UNSET:
            field_dict["slack_team_id"] = slack_team_id
        if slack_command_script is not UNSET:
            field_dict["slack_command_script"] = slack_command_script
        if auto_invite_domain is not UNSET:
            field_dict["auto_invite_domain"] = auto_invite_domain
        if auto_invite_operator is not UNSET:
            field_dict["auto_invite_operator"] = auto_invite_operator
        if auto_add is not UNSET:
            field_dict["auto_add"] = auto_add
        if plan is not UNSET:
            field_dict["plan"] = plan
        if customer_id is not UNSET:
            field_dict["customer_id"] = customer_id
        if webhook is not UNSET:
            field_dict["webhook"] = webhook
        if deploy_to is not UNSET:
            field_dict["deploy_to"] = deploy_to
        if ai_resource is not UNSET:
            field_dict["ai_resource"] = ai_resource
        if error_handler is not UNSET:
            field_dict["error_handler"] = error_handler
        if error_handler_extra_args is not UNSET:
            field_dict["error_handler_extra_args"] = error_handler_extra_args
        if large_file_storage is not UNSET:
            field_dict["large_file_storage"] = large_file_storage
        if git_sync is not UNSET:
            field_dict["git_sync"] = git_sync
        if deploy_ui is not UNSET:
            field_dict["deploy_ui"] = deploy_ui
        if default_app is not UNSET:
            field_dict["default_app"] = default_app
        if default_scripts is not UNSET:
            field_dict["default_scripts"] = default_scripts
        if mute_critical_alerts is not UNSET:
            field_dict["mute_critical_alerts"] = mute_critical_alerts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_settings_response_200_ai_resource import GetSettingsResponse200AiResource
        from ..models.get_settings_response_200_default_scripts import GetSettingsResponse200DefaultScripts
        from ..models.get_settings_response_200_deploy_ui import GetSettingsResponse200DeployUi
        from ..models.get_settings_response_200_error_handler_extra_args import (
            GetSettingsResponse200ErrorHandlerExtraArgs,
        )
        from ..models.get_settings_response_200_git_sync import GetSettingsResponse200GitSync
        from ..models.get_settings_response_200_large_file_storage import GetSettingsResponse200LargeFileStorage

        d = src_dict.copy()
        automatic_billing = d.pop("automatic_billing")

        code_completion_enabled = d.pop("code_completion_enabled")

        error_handler_muted_on_cancel = d.pop("error_handler_muted_on_cancel")

        workspace_id = d.pop("workspace_id", UNSET)

        slack_name = d.pop("slack_name", UNSET)

        slack_team_id = d.pop("slack_team_id", UNSET)

        slack_command_script = d.pop("slack_command_script", UNSET)

        auto_invite_domain = d.pop("auto_invite_domain", UNSET)

        auto_invite_operator = d.pop("auto_invite_operator", UNSET)

        auto_add = d.pop("auto_add", UNSET)

        plan = d.pop("plan", UNSET)

        customer_id = d.pop("customer_id", UNSET)

        webhook = d.pop("webhook", UNSET)

        deploy_to = d.pop("deploy_to", UNSET)

        _ai_resource = d.pop("ai_resource", UNSET)
        ai_resource: Union[Unset, GetSettingsResponse200AiResource]
        if isinstance(_ai_resource, Unset):
            ai_resource = UNSET
        else:
            ai_resource = GetSettingsResponse200AiResource.from_dict(_ai_resource)

        error_handler = d.pop("error_handler", UNSET)

        _error_handler_extra_args = d.pop("error_handler_extra_args", UNSET)
        error_handler_extra_args: Union[Unset, GetSettingsResponse200ErrorHandlerExtraArgs]
        if isinstance(_error_handler_extra_args, Unset):
            error_handler_extra_args = UNSET
        else:
            error_handler_extra_args = GetSettingsResponse200ErrorHandlerExtraArgs.from_dict(_error_handler_extra_args)

        _large_file_storage = d.pop("large_file_storage", UNSET)
        large_file_storage: Union[Unset, GetSettingsResponse200LargeFileStorage]
        if isinstance(_large_file_storage, Unset):
            large_file_storage = UNSET
        else:
            large_file_storage = GetSettingsResponse200LargeFileStorage.from_dict(_large_file_storage)

        _git_sync = d.pop("git_sync", UNSET)
        git_sync: Union[Unset, GetSettingsResponse200GitSync]
        if isinstance(_git_sync, Unset):
            git_sync = UNSET
        else:
            git_sync = GetSettingsResponse200GitSync.from_dict(_git_sync)

        _deploy_ui = d.pop("deploy_ui", UNSET)
        deploy_ui: Union[Unset, GetSettingsResponse200DeployUi]
        if isinstance(_deploy_ui, Unset):
            deploy_ui = UNSET
        else:
            deploy_ui = GetSettingsResponse200DeployUi.from_dict(_deploy_ui)

        default_app = d.pop("default_app", UNSET)

        _default_scripts = d.pop("default_scripts", UNSET)
        default_scripts: Union[Unset, GetSettingsResponse200DefaultScripts]
        if isinstance(_default_scripts, Unset):
            default_scripts = UNSET
        else:
            default_scripts = GetSettingsResponse200DefaultScripts.from_dict(_default_scripts)

        mute_critical_alerts = d.pop("mute_critical_alerts", UNSET)

        get_settings_response_200 = cls(
            automatic_billing=automatic_billing,
            code_completion_enabled=code_completion_enabled,
            error_handler_muted_on_cancel=error_handler_muted_on_cancel,
            workspace_id=workspace_id,
            slack_name=slack_name,
            slack_team_id=slack_team_id,
            slack_command_script=slack_command_script,
            auto_invite_domain=auto_invite_domain,
            auto_invite_operator=auto_invite_operator,
            auto_add=auto_add,
            plan=plan,
            customer_id=customer_id,
            webhook=webhook,
            deploy_to=deploy_to,
            ai_resource=ai_resource,
            error_handler=error_handler,
            error_handler_extra_args=error_handler_extra_args,
            large_file_storage=large_file_storage,
            git_sync=git_sync,
            deploy_ui=deploy_ui,
            default_app=default_app,
            default_scripts=default_scripts,
            mute_critical_alerts=mute_critical_alerts,
        )

        get_settings_response_200.additional_properties = d
        return get_settings_response_200

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

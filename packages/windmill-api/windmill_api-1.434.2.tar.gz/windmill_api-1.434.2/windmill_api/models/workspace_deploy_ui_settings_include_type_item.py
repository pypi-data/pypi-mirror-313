from enum import Enum


class WorkspaceDeployUISettingsIncludeTypeItem(str, Enum):
    APP = "app"
    FLOW = "flow"
    RESOURCE = "resource"
    SCRIPT = "script"
    SECRET = "secret"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)

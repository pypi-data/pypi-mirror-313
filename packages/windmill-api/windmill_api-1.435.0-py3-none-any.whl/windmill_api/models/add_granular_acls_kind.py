from enum import Enum


class AddGranularAclsKind(str, Enum):
    APP = "app"
    FLOW = "flow"
    FOLDER = "folder"
    GROUP = "group_"
    HTTP_TRIGGER = "http_trigger"
    KAFKA_TRIGGER = "kafka_trigger"
    RAW_APP = "raw_app"
    RESOURCE = "resource"
    SCHEDULE = "schedule"
    SCRIPT = "script"
    VARIABLE = "variable"
    WEBSOCKET_TRIGGER = "websocket_trigger"

    def __str__(self) -> str:
        return str(self.value)

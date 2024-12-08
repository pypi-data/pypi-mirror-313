from langroid.agent.tool_message import ToolMessage


class StructuredMessage(ToolMessage):
    request: str = ""
    purpose: str = "Wrapper for a structured message"

    # allow subclasses to inhert this "extras allowed" config
    # model_config = ConfigDict(extra=Extra.allow)

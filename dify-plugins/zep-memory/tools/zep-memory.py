from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class ZepMemoryTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Auth
        api_key = self.runtime.credentials.get("api_key")
        # Params
        user_id = tool_parameters.get("user_id", "")
        session_id = tool_parameters.get("session_id", "")
        ref = tool_parameters.get("ref", "")

        yield self.create_json_message({"result": "Hello, world!"})

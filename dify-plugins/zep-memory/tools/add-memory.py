from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.common import ZepMemoryData, ZepMemoryRetrievalFailure
from zep_cloud.client import Zep
from zep_cloud.errors import NotFoundError
from zep_cloud.types import Message


class AddMemoryTool(Tool):
    """Zep cloud add-memory tool"""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Auth
        api_key = self.runtime.credentials.get("api_key")
        # settings

        # Params
        user_id = tool_parameters.get("user_id", "")
        session_id = tool_parameters.get("session_id", "")
        role_type = tool_parameters.get("role_type", "")
        content = tool_parameters.get("content", "")

        if role_type not in ("user", "assistant", "system", "function", "tool"):
            raise ValueError(f"Invalid role type: {role_type}")

        zep = Zep(api_key=api_key)
        try:
            message = Message(role_type=role_type, content=content)

            try:
                zep.memory.get_session(session_id)
            except NotFoundError:
                zep.memory.add_session(session_id=session_id, user_id=user_id)

            zep.memory.add(session_id=session_id, messages=[message])
            memory_data = ZepMemoryData(
                session_id=session_id,
                message=f"Successfully added message to memory session {session_id}",
            )
            # TODO: logging
            yield self.create_text_message(memory_data.to_text())

        except Exception as err:
            raise ZepMemoryRetrievalFailure(f"Error Adding memory: {str(err)}")

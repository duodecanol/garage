from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from tools.common import ZepMemoryData, ZepMemoryRetrievalFailure
from zep_cloud.client import Zep
from zep_cloud.errors import NotFoundError


class GetMemoryTool(Tool):
    """Zep cloud get-memory tool"""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Auth
        api_key = self.runtime.credentials.get("api_key")
        # settings

        # Params
        user_id = tool_parameters.get("user_id", "")
        session_id = tool_parameters.get("session_id", "")

        zep = Zep(api_key=api_key)
        try:
            memory = zep.memory.get(session_id)
            memory_data = ZepMemoryData(
                session_id=session_id,
                context=memory.context,
            )
            # TODO: logging
            yield self.create_text_message(memory_data.to_text())

        except NotFoundError:
            yield self.create_text_message("")
        except Exception as err:
            raise ZepMemoryRetrievalFailure(f"Error retrieving memory: {str(err)}")

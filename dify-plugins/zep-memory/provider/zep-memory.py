from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from zep_cloud.client import Zep
from zep_cloud.errors import NotFoundError


class ZepMemoryProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        if "api_key" not in credentials:
            raise ToolProviderCredentialValidationError("api_key is required")
        try:
            api_key: str = credentials["api_key"]
            if not api_key:
                raise ToolProviderCredentialValidationError("api_key is required")
            zep = Zep(api_key=api_key)
            user_id = "auth-check-dify-plugin"
            try:
                user = zep.user.get(user_id)
            except NotFoundError:
                ...
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

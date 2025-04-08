from dataclasses import dataclass
from typing import Optional


class ZepMemoryRetrievalFailure(Exception): ...


@dataclass
class ZepMemoryData:
    session_id: str
    context: Optional[str] = None
    message: Optional[str] = None

    def to_text(self) -> str:
        if self.message:
            return self.message
        return f"""
Memory Context for Session {self.session_id}:
{self.context}
        """

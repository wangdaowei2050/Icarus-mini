from dataclasses import dataclass, field
from typing import Any
from app.schemas.chat import ChatMessage

@dataclass
class AgentState:
    user_id: int = 1
    conversation_id: int
    model: str
    messages: list[ChatMessage]

    short_memory: list[str] = field(default_factory=list)

    long_memory: list[str] = field(default_factory=list)

    intent: str | None = None
    tool_name: str | None = None
    tool_arguments: dict[str, Any] = field(default_factory=dict)
    tool_result: str | None = None

    final_answer: str = ""
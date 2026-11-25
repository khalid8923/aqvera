"""Memory layer: conversation and learning memory storage.

Stores conversation history and short-term context used by the tutor. Long-term
learning evidence lives in the backend adaptive-learning domain; this module
holds AI-facing conversation memory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import Message


@dataclass
class ConversationMemory:
    conversation_id: str
    messages: list[Message] = field(default_factory=list)
    max_turns: int = 50

    def add(self, message: Message) -> None:
        self.messages.append(message)
        if len(self.messages) > self.max_turns:
            self.messages = self.messages[-self.max_turns:]

    def get_context(self, last_n: int = 10) -> list[Message]:
        return self.messages[-last_n:]

    def clear(self) -> None:
        self.messages = []


class MemoryStore:
    """In-memory store for conversation memories (backend may persist to DB)."""

    def __init__(self) -> None:
        self._memories: dict[str, ConversationMemory] = {}

    def get_or_create(self, conversation_id: str) -> ConversationMemory:
        if conversation_id not in self._memories:
            self._memories[conversation_id] = ConversationMemory(
                conversation_id=conversation_id
            )
        return self._memories[conversation_id]

    def get(self, conversation_id: str) -> Optional[ConversationMemory]:
        return self._memories.get(conversation_id)

    def delete(self, conversation_id: str) -> None:
        self._memories.pop(conversation_id, None)

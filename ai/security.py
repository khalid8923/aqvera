"""Prompt-injection defenses for untrusted uploaded document content.

Uploaded documents are untrusted data. Instructions inside them must never
override AQVERA system policies or application instructions. This module
sanitizes user-provided content before it reaches provider prompts.
"""

from __future__ import annotations

from typing import Any

from ai import Message


class PromptInjectionGuard:
    """Detects and neutralizes prompt-injection attempts in untrusted content."""

    # Common injection marker phrases. Not exhaustive; defense-in-depth.
    _INJECTION_MARKERS = [
        "ignore previous instructions",
        "ignore all previous",
        "disregard the above",
        "system:",
        "you are now",
        "new instructions:",
        "override system",
        "jailbreak",
        "forget your",
    ]

    def sanitize(self, messages: list[Message]) -> list[Message]:
        """Return a copy of messages with injection markers neutralized in user content."""
        sanitized: list[Message] = []
        for msg in messages:
            content = msg.content
            if msg.role == "user":
                content = self._neutralize(content)
            sanitized.append(Message(role=msg.role, content=content))
        return sanitized

    def _neutralize(self, content: str) -> str:
        import re

        for marker in self._INJECTION_MARKERS:
            # Case-insensitive replacement of injection markers.
            content = re.sub(re.escape(marker), "[injection marker removed]", content, flags=re.IGNORECASE)
        return content

    def contains_injection(self, content: str) -> bool:
        import re

        lower = content.lower()
        return any(re.search(re.escape(marker), lower) for marker in self._INJECTION_MARKERS)

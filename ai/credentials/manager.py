"""Credential management for AI providers.

Centralized, secure credential handling. Provider API keys are never exposed
in frontend responses, logs, or error messages. Credentials are sourced from
environment variables (or an existing secure config mechanism). This module
tracks which providers have credentials configured, their validation status,
and last connection test, without ever storing or returning secret values.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from ai import ProviderCredential


@dataclass
class CredentialEntry:
    """Internal credential record (secret value held in memory only)."""

    provider_id: str
    api_key: Optional[str] = None  # The actual secret (never serialized out)
    key_source: str = "env"  # env | config | vault
    configured: bool = False
    provider_status: str = "unknown"  # healthy | degraded | down | unknown
    usage_status: str = "idle"  # idle | active | rate_limited | disabled


class CredentialManager:
    """Manages AI provider credentials.

    Keys are read from environment variables at initialization. The manager
    never returns the full key; it only reports whether a key is configured,
    its last-four mask, validation status, and last connection test.
    """

    # Mapping of provider_id -> env variable name(s). Multiple env vars can be
    # listed; the first non-empty one wins.
    ENV_VAR_MAP: dict[str, list[str]] = {
        "openai_compatible": ["AQVERA_OPENAI_COMPATIBLE_API_KEY"],
        "anthropic": ["AQVERA_ANTHROPIC_API_KEY"],
        "google_gemini": ["AQVERA_GOOGLE_GEMINI_API_KEY", "GEMINI_API_KEY"],
        "groq": ["AQVERA_GROQ_API_KEY", "GROQ_API_KEY"],
        "nvidia_nim": ["AQVERA_NVIDIA_API_KEY", "NVIDIA_API_KEY"],
        "deepseek": ["AQVERA_DEEPSEEK_API_KEY", "DEEPSEEK_API_KEY"],
        "mistral": ["AQVERA_MISTRAL_API_KEY", "MISTRAL_API_KEY"],
        "together": ["AQVERA_TOGETHER_API_KEY", "TOGETHER_API_KEY"],
        "huggingface": ["AQVERA_HUGGINGFACE_API_KEY", "HF_TOKEN"],
        "cohere": ["AQVERA_COHERE_API_KEY", "COHERE_API_KEY"],
        "elevenlabs": ["AQVERA_ELEVENLABS_API_KEY", "ELEVENLABS_API_KEY"],
        "local": [],
    }

    def __init__(self) -> None:
        self._entries: dict[str, CredentialEntry] = {}
        self._validation: dict[str, str] = {}  # provider_id -> valid | invalid | untested | expired
        self._last_test: dict[str, Optional[str]] = {}
        self._load_from_env()

    def _load_from_env(self) -> None:
        for provider_id, env_names in self.ENV_VAR_MAP.items():
            api_key = None
            for name in env_names:
                value = os.getenv(name)
                if value:
                    api_key = value
                    break
            self._entries[provider_id] = CredentialEntry(
                provider_id=provider_id,
                api_key=api_key,
                configured=bool(api_key),
            )
            if not api_key:
                self._validation[provider_id] = "untested"
                self._last_test[provider_id] = None

    def is_configured(self, provider_id: str) -> bool:
        entry = self._entries.get(provider_id)
        return bool(entry and entry.configured and entry.api_key)

    def get_credential(self, provider_id: str) -> Optional[str]:
        """Return the actual API key for internal provider adapter use only.

        This method is for use by provider adapters within the backend process.
        It must never be called from frontend-facing code or logged.
        """
        entry = self._entries.get(provider_id)
        if not entry or not entry.configured:
            return None
        return entry.api_key

    def key_last_four(self, provider_id: str) -> Optional[str]:
        entry = self._entries.get(provider_id)
        if not entry or not entry.api_key:
            return None
        key = entry.api_key
        return key[-4:] if len(key) >= 4 else key

    def provider_credential(self, provider_id: str) -> ProviderCredential:
        """Return a safe credential summary (no secret value)."""
        entry = self._entries.get(provider_id)
        configured = bool(entry and entry.configured)
        return ProviderCredential(
            provider_id=provider_id,
            configured=configured,
            key_last_four=self.key_last_four(provider_id) if configured else None,
            validation_status=self._validation.get(provider_id, "untested"),
            last_connection_test=self._last_test.get(provider_id),
            usage_status=entry.usage_status if entry else "disabled",
            provider_status=entry.provider_status if entry else "unknown",
            multiple_keys=False,
            key_count=1 if configured else 0,
        )

    def list_credentials(self) -> list[ProviderCredential]:
        return [self.provider_credential(pid) for pid in self._entries]

    def set_validation(self, provider_id: str, status: str) -> None:
        """Record validation status (valid | invalid | untested | expired)."""
        self._validation[provider_id] = status
        self._last_test[provider_id] = _now()

    def set_provider_status(self, provider_id: str, status: str) -> None:
        entry = self._entries.get(provider_id)
        if entry is None:
            return
        entry.provider_status = status

    def add_key(self, provider_id: str, api_key: str, source: str = "env") -> None:
        """Add or update a credential (programmatic, e.g. after operator config)."""
        self._entries[provider_id] = CredentialEntry(
            provider_id=provider_id,
            api_key=api_key,
            key_source=source,
            configured=True,
        )
        self._validation[provider_id] = "untested"
        self._last_test[provider_id] = None

    def remove_key(self, provider_id: str) -> bool:
        """Remove a credential. Returns True if removed."""
        if provider_id in self._entries:
            del self._entries[provider_id]
            self._validation.pop(provider_id, None)
            self._last_test.pop(provider_id, None)
            return True
        return False


def _now() -> Optional[str]:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
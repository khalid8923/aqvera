"""Contract tests for the new AI platform components.

All tests use mocks and no live provider API calls. Providers that require
credentials are tested for correct "NOT CONFIGURED" behavior.
"""

from __future__ import annotations

import asyncio
import sys

sys.path.insert(0, ".")

from ai import (
    AIError,
    AIErrorCategory,
    AIRequest,
    AIResponse,
    AIUsage,
    AvailabilityStatus,
    FreeTierStatus,
    Message,
    ModelCapability,
    ModelSpec,
    PricingClass,
    ProviderUnavailableError,
    TaskCapability,
    TaskType,
)
from ai.credentials.manager import CredentialManager
from ai.orchestration.execution.engine import ExecutionEngine
from ai.orchestration.tasks.types import TaskInput, TaskOutput, get_task, register_task
from ai.providers.adapters.gemini import GeminiProvider
from ai.providers.base import AIProvider, ProviderConfig, ProviderRegistry
from ai.providers.mock import MockProvider
from ai.registry.capability import CapabilityIndex
from ai.registry.model_registry import ModelRegistry
from ai.resilience import (
    CircuitBreaker,
    CircuitConfig,
    CircuitState,
    RetryConfig,
    RetryScheduler,
    execute_with_resilience,
    is_retryable,
)
from ai.routing import FallbackManager, ModelRouter, RoutingPolicy, TaskPolicyRegistry
from ai.routing.selection import estimate_max_cost_usd, has_capability, score_model


def _run(coro):
    return asyncio.run(coro)


# --------------------------------------------------------------------------- #
# Credential manager tests
# --------------------------------------------------------------------------- #


def test_credential_manager_no_keys_configured():
    cm = CredentialManager()
    creds = cm.list_credentials()
    assert len(creds) > 0
    # None should be configured in this repo.
    assert all(not c.configured for c in creds)
    assert cm.is_configured("google_gemini") is False


def test_credential_manager_key_last_four_redacted():
    cm = CredentialManager()
    cm.add_key("test_provider", "sk-abcd1234efgh5678")
    assert cm.is_configured("test_provider") is True
    assert cm.key_last_four("test_provider") == "5678"
    cred = cm.provider_credential("test_provider")
    assert cred.key_last_four == "5678"
    # Full key never returned by provider_credential (only via get_credential internally).
    assert "sk-abcd1234efgh5678" not in str(cred)


def test_credential_manager_validation_status():
    cm = CredentialManager()
    cm.set_validation("google_gemini", "valid")
    cred = cm.provider_credential("google_gemini")
    assert cred.validation_status == "valid"


# --------------------------------------------------------------------------- #
# Model registry tests
# --------------------------------------------------------------------------- #


def test_model_registry_register_and_find():
    reg = ModelRegistry()
    spec = ModelSpec(
        model_id="gemini-3.5-flash-lite",
        provider_id="google_gemini",
        display_name="Gemini 3.5 Flash-Lite",
        task_capabilities=[TaskCapability.TEXT, TaskCapability.VISION],
        task_types=[TaskType.CHAT, TaskType.TUTOR_EXPLANATION],
        context_window=1_000_000,
        max_output_tokens=8192,
        streaming=True,
        pricing_class=PricingClass.FREE,
        free_tier_status=FreeTierStatus.PERMANENT,
        availability=AvailabilityStatus.ACTIVE,
        documentation_url="https://aistudio.google.com/docs/",
        last_verification_date="2026-11-25",
        cost_per_input_token=0.0,
        cost_per_output_token=0.0,
    )
    reg.register(spec)
    assert reg.get("gemini-3.5-flash-lite") is spec
    assert reg.count() == 1
    assert reg.count_active() == 1
    found = reg.find_for_task(TaskType.TUTOR_EXPLANATION)
    assert any(m.model_id == "gemini-3.5-flash-lite" for m in found)


def test_model_registry_disabled_model_not_active():
    reg = ModelRegistry()
    spec = ModelSpec(
        model_id="old-model",
        provider_id="prov",
        display_name="Old",
        availability=AvailabilityStatus.DEPRECATED,
    )
    reg.register(spec)
    active = reg.list_models(active_only=True)
    assert len(active) == 0
    all_models = reg.list_models(active_only=False)
    assert len(all_models) == 1


def test_model_registry_unregister():
    reg = ModelRegistry()
    spec = ModelSpec(model_id="m1", provider_id="p", display_name="M1")
    reg.register(spec)
    assert reg.unregister("m1") is True
    assert reg.get("m1") is None
    assert reg.unregister("m1") is False


# --------------------------------------------------------------------------- #
# Capability index tests
# --------------------------------------------------------------------------- #


def test_capability_index_find_for_task():
    reg = ModelRegistry()
    spec = ModelSpec(
        model_id="embed-model",
        provider_id="p",
        display_name="Embed",
        task_capabilities=[TaskCapability.EMBEDDING],
        task_types=[TaskType.EMBEDDING],
    )
    reg.register(spec)
    results = reg.find_for_task(TaskType.EMBEDDING)
    assert any(m.model_id == "embed-model" for m in results)
    results_chat = reg.find_for_task(TaskType.CHAT)
    assert not any(m.model_id == "embed-model" for m in results_chat)


# --------------------------------------------------------------------------- #
# Router tests
# --------------------------------------------------------------------------- #


def test_router_selects_free_model():
    reg = ModelRegistry()
    reg.register(ModelSpec(
        model_id="free-model",
        provider_id="p",
        display_name="Free",
        task_capabilities=[TaskCapability.TEXT],
        task_types=[TaskType.CHAT],
        pricing_class=PricingClass.FREE,
        free_tier_status=FreeTierStatus.PERMANENT,
        availability=AvailabilityStatus.ACTIVE,
    ))
    reg.register(ModelSpec(
        model_id="paid-model",
        provider_id="p",
        display_name="Paid",
        task_capabilities=[TaskCapability.TEXT],
        task_types=[TaskType.CHAT],
        pricing_class=PricingClass.PAID,
        free_tier_status=FreeTierStatus.NONE,
        availability=AvailabilityStatus.ACTIVE,
    ))
    policies = TaskPolicyRegistry()
    router = ModelRouter(reg, policies)
    decision = router.select(TaskType.CHAT, diagnostic=True)
    assert decision.model_id == "free-model"
    assert len(decision.diagnostics) > 0


def test_router_no_eligible_model_raises():
    reg = ModelRegistry()
    reg.register(ModelSpec(
        model_id="paid-only",
        provider_id="p",
        display_name="Paid",
        task_capabilities=[TaskCapability.TEXT],
        task_types=[TaskType.CHAT],
        pricing_class=PricingClass.PAID,
        availability=AvailabilityStatus.ACTIVE,
    ))
    policies = TaskPolicyRegistry()
    router = ModelRouter(reg, policies)
    try:
        router.select(TaskType.CHAT, require_free_tier=True)
        assert False, "Expected error"
    except ProviderUnavailableError as exc:
        assert exc.error is not None
        assert exc.error.category == AIErrorCategory.PROVIDER_UNAVAILABLE


# --------------------------------------------------------------------------- #
# Selection helper tests
# --------------------------------------------------------------------------- #


def test_score_model_prefers_free():
    free_spec = ModelSpec(
        model_id="f", provider_id="p", display_name="F",
        free_tier_status=FreeTierStatus.PERMANENT,
        pricing_class=PricingClass.FREE,
    )
    paid_spec = ModelSpec(
        model_id="g", provider_id="p", display_name="G",
        free_tier_status=FreeTierStatus.NONE,
        pricing_class=PricingClass.PAID,
    )
    assert score_model(free_spec) > score_model(paid_spec)


def test_has_capability():
    spec = ModelSpec(model_id="m", provider_id="p", display_name="M",
                     task_capabilities=[TaskCapability.VISION])
    assert has_capability(spec, TaskCapability.VISION) is True
    assert has_capability(spec, TaskCapability.EMBEDDING) is False


def test_estimate_max_cost_usd():
    spec = ModelSpec(model_id="m", provider_id="p", display_name="M",
                     cost_per_output_token=1.0)  # $1 per 1M tokens
    cost = estimate_max_cost_usd(spec, 1_000_000)
    assert cost == 1.0
    spec2 = ModelSpec(model_id="m2", provider_id="p", display_name="M2")
    assert estimate_max_cost_usd(spec2, 1000) is None


# --------------------------------------------------------------------------- #
# Resilience tests
# --------------------------------------------------------------------------- #


def test_is_retryable_classification():
    assert is_retryable(AIError(AIErrorCategory.RATE_LIMIT, "x", retryable=True)) is True
    assert is_retryable(AIError(AIErrorCategory.TIMEOUT, "x", retryable=True)) is True
    assert is_retryable(AIError(AIErrorCategory.INVALID_REQUEST, "x", retryable=False)) is False
    assert is_retryable(AIError(AIErrorCategory.UNSUPPORTED_CAPABILITY, "x", retryable=False)) is False
    assert is_retryable(AIError(AIErrorCategory.MALFORMED_OUTPUT, "x", retryable=False)) is False


def test_retry_scheduler_backoff():
    sched = RetryScheduler(RetryConfig(base_delay_ms=100, max_delay_ms=1000, jitter=False))
    d0 = sched.delay_for(0)
    d1 = sched.delay_for(1)
    d2 = sched.delay_for(2)
    assert d0 <= d1 <= d2
    assert d2 <= 1000


def test_circuit_breaker_opens_after_failures():
    cb = CircuitBreaker(CircuitConfig(failure_threshold=2, recovery_timeout_ms=5000))
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.allow_request() is False


async def _fail_once():
    raise RuntimeError("boom")


def test_execute_with_resilience_returns_error():
    result = _run(execute_with_resilience(_fail_once, retry_config=RetryConfig(max_retries=1)))
    assert result.error is not None
    assert result.content is None


# --------------------------------------------------------------------------- #
# Execution engine tests (mock provider)
# --------------------------------------------------------------------------- #


def test_execution_engine_mock_success():
    reg = ModelRegistry()
    reg.register(ModelSpec(
        model_id="mock-model",
        provider_id="mock",
        display_name="Mock",
        task_capabilities=[TaskCapability.TEXT],
        task_types=[TaskType.CHAT],
        free_tier_status=FreeTierStatus.PERMANENT,
        pricing_class=PricingClass.FREE,
        availability=AvailabilityStatus.ACTIVE,
    ))
    policies = TaskPolicyRegistry()
    router = ModelRouter(reg, policies)
    fallback_mgr = FallbackManager(reg, router)
    cm = CredentialManager()
    cm.add_key("mock", "sk-mock")
    engine = ExecutionEngine(reg, router, fallback_mgr, cm, {"mock": MockProvider()})
    messages = [Message(role="user", content="Hello")]
    response = _run(engine.execute(TaskType.CHAT, messages, user_id="u1"))
    assert response.error is None
    assert response.content is not None


def test_execution_engine_no_provider_configured():
    reg = ModelRegistry()
    reg.register(ModelSpec(
        model_id="mock-model",
        provider_id="mock",
        display_name="Mock",
        task_capabilities=[TaskCapability.TEXT],
        task_types=[TaskType.CHAT],
        free_tier_status=FreeTierStatus.PERMANENT,
        pricing_class=PricingClass.FREE,
        availability=AvailabilityStatus.ACTIVE,
    ))
    policies = TaskPolicyRegistry()
    router = ModelRouter(reg, policies)
    fallback_mgr = FallbackManager(reg, router)
    cm = CredentialManager()  # no keys
    engine = ExecutionEngine(reg, router, fallback_mgr, cm, {})
    messages = [Message(role="user", content="Hello")]
    response = _run(engine.execute(TaskType.CHAT, messages, user_id="u1"))
    assert response.error is not None
    assert response.content is None


# --------------------------------------------------------------------------- #
# Task definition tests
# --------------------------------------------------------------------------- #


def test_task_definitions_registered():
    assert get_task(TaskType.TUTOR_EXPLANATION) is not None
    assert get_task(TaskType.EMBEDDING) is not None
    assert get_task(TaskType.WEB_RESEARCH) is not None
    td = get_task(TaskType.EMBEDDING)
    assert td.required_capability == TaskCapability.EMBEDDING


def test_task_input_require_text():
    ti = TaskInput(task_type=TaskType.CHAT)
    try:
        ti.require_text()
        assert False
    except ValueError:
        pass
    ti2 = TaskInput(task_type=TaskType.CHAT, text="hello")
    assert ti2.require_text() == "hello"


def test_gemini_provider_not_configured():
    from ai import ProviderType
    provider = GeminiProvider(ProviderConfig(
        id="google_gemini", name="Gemini", type=ProviderType.OPENAI_COMPATIBLE
    ))
    assert provider._configured is False

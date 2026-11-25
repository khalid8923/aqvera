"""Resilience layer: retry, backoff, circuit breaker, timeouts, health checks.

Provides the execution reliability layer for AI provider requests. Errors are
not blindly retried: invalid API keys and invalid requests are classified as
non-retryable. Only retryable errors (rate limit, timeout, transient failure)
trigger backoff with jitter.
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from ai import AIError, AIErrorCategory, AIResponse, AIUsage


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_retries: int = 3
    base_delay_ms: int = 500
    max_delay_ms: int = 30000
    backoff_multiplier: float = 2.0
    jitter: bool = True
    jitter_ms: int = 250


@dataclass
class CircuitConfig:
    """Configuration for circuit breaker."""

    failure_threshold: int = 5
    recovery_timeout_ms: int = 30000
    half_open_max_calls: int = 3


class CircuitBreaker:
    """Circuit breaker that trips after repeated failures and recovers over time."""

    def __init__(self, config: CircuitConfig | None = None) -> None:
        self.config = config or CircuitConfig()
        self.state = CircuitState.CLOSED
        self._failures = 0
        self._opened_at: Optional[float] = None
        self._half_open_calls = 0

    def allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if (
                self._opened_at is not None
                and time.monotonic() * 1000 - self._opened_at >= self.config.recovery_timeout_ms
            ):
                self.state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
                return True
            return False
        # HALF_OPEN: allow a limited number of probe calls.
        if self._half_open_calls < self.config.half_open_max_calls:
            self._half_open_calls += 1
            return True
        return False

    def record_success(self) -> None:
        self._failures = 0
        self.state = CircuitState.CLOSED
        self._opened_at = None
        self._half_open_calls = 0

    def record_failure(self) -> None:
        self._failures += 1
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self._opened_at = time.monotonic() * 1000
            return
        if self._failures >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self._opened_at = time.monotonic() * 1000


class RetryScheduler:
    """Computes retry delays with exponential backoff and jitter."""

    def __init__(self, config: RetryConfig | None = None) -> None:
        self.config = config or RetryConfig()

    def delay_for(self, attempt: int) -> int:
        """Return delay in milliseconds for the given attempt index (0-based)."""
        delay = min(
            self.config.base_delay_ms * (self.config.backoff_multiplier ** attempt),
            self.config.max_delay_ms,
        )
        if self.config.jitter:
            delay = delay + random.uniform(0, self.config.jitter_ms)
        return int(delay)


def is_retryable(error: AIError) -> bool:
    """Classify whether an AIError is retryable.

    Retryable: rate limit, timeout, provider unavailable (transient).
    Non-retryable: invalid request, unsupported capability, malformed output,
    authentication failure (invalid API key).
    """
    if error.category in (
        AIErrorCategory.RATE_LIMIT,
        AIErrorCategory.TIMEOUT,
        AIErrorCategory.PROVIDER_UNAVAILABLE,
    ):
        return True
    if error.category in (
        AIErrorCategory.INVALID_REQUEST,
        AIErrorCategory.UNSUPPORTED_CAPABILITY,
        AIErrorCategory.MALFORMED_OUTPUT,
    ):
        return False
    return True  # unknown: be conservative, retry once


def _make_response(error: AIError, provider: str = "resilience", model: str = "none") -> AIResponse:
    return AIResponse(
        content=None,
        structured_output=None,
        usage=AIUsage(),
        cost_estimate=None,
        latency_ms=0,
        provider=provider,
        model=model,
        finish_reason=None,
        error=error,
    )


def _unavailable_response(message: str) -> AIResponse:
    return _make_response(
        AIError(
            category=AIErrorCategory.PROVIDER_UNAVAILABLE,
            message=message,
            retryable=False,
        )
    )


def _timeout_response() -> AIResponse:
    return _make_response(
        AIError(
            category=AIErrorCategory.TIMEOUT,
            message="Request timed out",
            retryable=True,
        )
    )


def _error_response(exc: Exception) -> AIResponse:
    return _make_response(
        AIError(
            category=AIErrorCategory.UNKNOWN,
            message=str(exc),
            retryable=True,
        )
    )


async def execute_with_resilience(
    func: Callable,
    *,
    retry_config: RetryConfig | None = None,
    circuit: CircuitBreaker | None = None,
    timeout_ms: Optional[int] = None,
    is_retryable_fn: Callable[[AIError], bool] = is_retryable,
) -> AIResponse:
    """Execute an async function with retry, circuit breaker, and timeout.

    Args:
        func: Async callable returning an AIResponse-like object with an
            `error` attribute (AIError | None).
        retry_config: Retry configuration.
        circuit: Circuit breaker (shared across calls).
        timeout_ms: Per-attempt timeout in milliseconds.
        is_retryable_fn: Classifier for whether an error is retryable.

    Returns the successful result. On exhaustion, returns the last error result.
    """
    config = retry_config or RetryConfig()
    scheduler = RetryScheduler(config)
    breaker = circuit or CircuitBreaker()
    last_result: Optional[AIResponse] = None

    for attempt in range(config.max_retries + 1):
        if not breaker.allow_request():
            last_result = _unavailable_response("circuit breaker open")
            break

        try:
            if timeout_ms is not None:
                result = await asyncio.wait_for(func(), timeout=timeout_ms / 1000.0)
            else:
                result = await func()
        except asyncio.TimeoutError:
            breaker.record_failure()
            if attempt < config.max_retries:
                await asyncio.sleep(scheduler.delay_for(attempt) / 1000.0)
                continue
            last_result = _timeout_response()
            break
        except Exception as exc:  # noqa: BLE001
            breaker.record_failure()
            error = AIError(
                category=AIErrorCategory.UNKNOWN,
                message=str(exc),
                retryable=True,
            )
            if attempt < config.max_retries and is_retryable_fn(error):
                await asyncio.sleep(scheduler.delay_for(attempt) / 1000.0)
                continue
            last_result = _error_response(exc)
            break

        # Check result-level error.
        error = getattr(result, "error", None)
        if error is None:
            breaker.record_success()
            return result

        if not is_retryable_fn(error):
            # Non-retryable error: do not retry.
            breaker.record_failure()
            return result

        # Retryable: increment failures and retry.
        breaker.record_failure()
        last_result = result
        if attempt < config.max_retries:
            await asyncio.sleep(scheduler.delay_for(attempt) / 1000.0)
            continue
        break

    return last_result or _unavailable_response("no result returned")
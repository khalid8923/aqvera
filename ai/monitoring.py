"""Latency tracking for AI provider requests."""

from __future__ import annotations

from collections import deque


class LatencyTracker:
    """Tracks request latency per provider/model."""

    def __init__(self, window_size: int = 100) -> None:
        self._latencies: deque[int] = deque(maxlen=window_size)

    def record(self, latency_ms: int) -> None:
        self._latencies.append(latency_ms)

    def average_ms(self) -> float:
        if not self._latencies:
            return 0.0
        return sum(self._latencies) / len(self._latencies)

    def p95_ms(self) -> float:
        if not self._latencies:
            return 0.0
        sorted_lat = sorted(self._latencies)
        idx = int(0.95 * (len(sorted_lat) - 1))
        return float(sorted_lat[idx])

    def count(self) -> int:
        return len(self._latencies)

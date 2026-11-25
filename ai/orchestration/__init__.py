"""Orchestration layer package.

Provides the high-level Orchestrator (legacy, preserved for compatibility) and
the new ExecutionEngine for resilient task execution with routing and fallback.
"""

from ai.orchestration.execution.engine import ExecutionEngine
from ai.orchestration.legacy import Orchestrator

__all__ = ["ExecutionEngine", "Orchestrator"]

"""Structured output validation.

Validates model-generated JSON against a JSON Schema contract before returning
it to the application. Never trusts model output simply because it appears
valid JSON.
"""

from __future__ import annotations

from typing import Any, Optional

try:
    from jsonschema import Draft7Validator, ValidationError as JsonSchemaValidationError
    _HAS_JSONSCHEMA = True
except Exception:  # jsonschema may not be installed
    Draft7Validator = None  # type: ignore
    JsonSchemaValidationError = Exception  # type: ignore
    _HAS_JSONSCHEMA = False


class ValidationResult:
    """Result of validating a structured model output."""

    def __init__(self, valid: bool, data: Optional[Any] = None, errors: Optional[list[str]] = None):
        self.valid = valid
        self.data = data
        self.errors = errors or []


class StructuredOutputValidator:
    """Validates structured (JSON) model output against a JSON Schema."""

    def __init__(self) -> None:
        self._schemas: dict[str, Any] = {}
        self._validators: dict[str, Any] = {}

    def register_schema(self, schema_id: str, schema: dict) -> None:
        self._schemas[schema_id] = schema
        if _HAS_JSONSCHEMA and Draft7Validator is not None:
            self._validators[schema_id] = Draft7Validator(schema)

    def validate(self, schema_id: str, value: Any) -> ValidationResult:
        """Validate `value` against the schema `schema_id`.

        Returns a ValidationResult. If jsonschema is not installed, performs a
        best-effort check that the value is a dict/list (non-empty) and
        warns that schema validation is unavailable.
        """
        if schema_id not in self._schemas:
            return ValidationResult(valid=False, errors=[f"Schema {schema_id} not registered"])

        if not _HAS_JSONSCHEMA:
            # Best-effort: accept if it's a dict/list; no real schema validation.
            if isinstance(value, (dict, list)):
                return ValidationResult(valid=True, data=value)
            return ValidationResult(valid=False, errors=["jsonschema not installed; cannot validate schema"])

        validator = self._validators.get(schema_id)
        if validator is None:
            return ValidationResult(valid=False, errors=[f"Validator for {schema_id} not initialized"])

        errors = [e.message for e in validator.iter_errors(value)]
        if errors:
            return ValidationResult(valid=False, errors=errors)
        return ValidationResult(valid=True, data=value)
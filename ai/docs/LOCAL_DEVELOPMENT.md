# Local Development

## Testing Without Paid API Requests

All AI adapters and orchestration logic are tested using the `MockProvider`
and contract tests. No live provider request is made in the test suite.

Run backend tests:
```
cd backend
python -m pytest tests/
```

Run AI-specific contract tests (to be added in `ai/tests/`):
```
cd backend
python -m pytest ai/tests/  # when present
```

## Mock Provider

`ai/providers/mock.py` — `MockProvider` returns deterministic canned responses
based on task type. Never makes live requests. Used for:
- Testing routing, fallback, circuit breaker, cost control.
- Testing orchestrator, tutor, RAG, assessment without a provider.
- Verifying provider-independent architecture.

## Adding a Provider Credential

1. Copy `.env.example` to `.env` (do not commit `.env`).
2. Add your API key:
   ```
   AQVERA_OPENAI_COMPATIBLE_API_KEY=sk-...
   AQVERA_ANTHROPIC_API_KEY=sk-...
   ```
3. Restart the backend.

## Provider Status

No live provider API key is configured in this repository. All AI features
honestly report "not configured" until a key is added.

## Project Structure

```
ai/
  providers/     provider adapters
  orchestration/ high-level task orchestration
  routing.py     task→model routing, fallback, circuit breaker
  agents.py      domain AI agents
  tutoring.py    course-aware tutoring
  rag.py         RAG pipeline
  retrieval.py   embeddings, vector/keyword retrieval
  memory.py      conversation memory
  adaptive_learning.py  deterministic mastery, recommendations
  assessment.py  questions, deterministic + subjective grading
  multimodal.py  image/audio/video interfaces
  prompts.py     versioned prompt templates
  evaluation.py  model/output evaluation
  cost_control.py budgets, spending ceilings
  monitoring.py  latency tracking
  security.py    prompt-injection defense, credentials
  tests/         contract and mock tests
  docs/          architecture and subsystem documentation
```

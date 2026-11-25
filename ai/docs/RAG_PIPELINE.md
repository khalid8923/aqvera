# RAG Pipeline

## Overview

Retrieval-augmented generation (RAG) grounds answers in the student's uploaded
materials. Retrieval is separate from generation: the LLM is never the source of
truth for document references — source references come from the retrieval index.

## Pipeline Stages

```
Question → RetrievalService.retrieve() → Chunks → Context Construction →
Orchestrator.generate() → Answer with Source Attribution
```

1. **Retrieve**: `RetrievalService` embeds the query and searches the vector store
   (pgvector) plus keyword search; merges and optionally reranks results.
2. **Context Build**: Chunks are formatted with document title + location
   (page/section/slide).
3. **Generate**: `Orchestrator.generate()` produces an answer using only the
   source context, with citation requirements in the system prompt.
4. **Attribute**: Every claim cites source title and location. No fabricated
   citations.

## Components

- `RAGPipeline.retrieve_and_answer()` — full retrieve → answer flow.
- `RetrievalService` — abstract retrieval interface; concrete backend impl queries pgvector.
- `Chunk` — a retrieved text chunk with metadata (document, section, page, slide, score).
- `EmbeddingModel` — abstraction over embedding providers.
- `VectorStore` — abstraction over vector search (pgvector).
- `Reranker` — optional reranking.

## Source Attribution Rules

- Every chunk carries `document_id`, `document_title`, `section`, `page`, `slide`.
- The system prompt requires citations: `[Document Title (page X, section Y)]`.
- The LLM never invents page citations; it can only cite what retrieval returned.
- If no chunks are found, the answer states the sources don't contain the answer
  and offers external knowledge with a caveat.

## Prompt-Injection Defense

Uploaded document content is treated as untrusted. `PromptInjectionGuard`
sanitizes user-facing content before it reaches provider prompts. System
instructions are in a separate channel; document text is never concatenated
into the system prompt.

## Retrieval Quality Tests

Tests verify:
- Relevant chunks are returned for known queries (mock index).
- Metadata filtering by course works.
- Empty results handled gracefully (no hallucinated sources).
- Arabic queries return relevant Arabic chunks.

## Arabic Retrieval

Arabic and mixed Arabic/English documents are supported at the chunking/
extraction stage (backend). Retrieval is language-agnostic (vector similarity).
Evaluation includes Arabic test cases in `ai/tests/`.

## Provider Status

No embedding provider is configured. Vector search uses a local/mock index in
tests. Production requires pgvector (PostgreSQL) or another vector store.

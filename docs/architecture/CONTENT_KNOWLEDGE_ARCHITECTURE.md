# CONTENT_KNOWLEDGE_ARCHITECTURE.md

# AQVERA — Content and Knowledge Architecture

## Content Pipeline (DECIDED)

Upload → Validation → Storage → Processing Job → Extraction → OCR (if needed) → Sectioning → Chunking → Embedding → Vector Index → Source References → Course Generation.

### Stages

1. **Upload Validation** — file type, size, malicious content scan, SHA-256 integrity.
2. **Storage** — S3-compatible object storage; metadata in `UploadedMaterials`.
3. **Processing Job** — created with status `pending`; idempotency key; progress tracking.
4. **Extraction** — text extraction from PDF/docx/etc.; creates `DocumentVersions` and `ExtractedSections`.
5. **OCR** — for image-based PDFs; optional stage; timeout with retry.
6. **Sectioning** — identify headings, paragraphs, tables, figures, equations; page references.
7. **Chunking** — split sections into chunks with token counts; `ContentChunks`.
8. **Embedding** — generate vectors via AI provider (or local embedding model); `Embeddings` + pgvector.
9. **Source References** — link chunks/sections back to source material with page/location.
10. **Course Generation** — AI generates course structure linked to learning objectives; validated against contract.

### Job Lifecycle (DECIDED)

- Statuses: pending → in_progress → completed/failed/cancelled.
- Progress: 0–100 reported per stage.
- Retry policy: max 3 retries with exponential backoff.
- Failure reasons stored; user notified.
- Idempotency key prevents duplicate processing on retry.
- Completed stages are not lost when a later stage fails (stage-based transactions).

### Failure Handling

| Failure | Behavior |
|---------|----------|
| Extraction failure | Job failed with reason; retry up to 3 times; user notified |
| OCR timeout | OCR stage skipped or retried; text-only fallback |
| Vector indexing failure | Degraded retrieval (keyword fallback); course generation continues |
| Course generation failure | Job failed; course not created; user can retry |

## Knowledge Architecture

### Source Traceability (DECIDED)

Every piece of generated academic content must be traceable to source material:

- Questions store `source_reference_id` linking to `SourceReferences`.
- Lessons store references to sections/objectives they cover.
- Explanations include source attribution (document, section, page).
- Embeddings store `chunk_id` → `section_id` → `document_version_id` → `material_id`.

### Content Integrity

- `UploadedMaterials.sha256` ensures file integrity.
- `DocumentVersions.version_number` tracks extraction versions.
- Content chunks are immutable once embedded; reprocessing creates new versions.

### Vector Search

- pgvector index on `Embeddings.vector` (1536 dimensions, configurable).
- Similarity search for retrieval; hybrid search (vector + keyword) as fallback.
- Retrieval quality indicators logged (top-k results, similarity scores, relevance feedback).

### Content Ownership

- Content Processing domain owns `UploadedMaterials`, `DocumentVersions`, `ProcessingJobs`, `ExtractedSections`, `ContentChunks`, `Embeddings`, `SourceReferences`.
- Academic Structure domain owns `Courses`, `Modules`, `Lessons`, `Topics`, `LearningObjectives`, `Prerequisites`.
- Teaching domain owns `LessonContent`, `LearningActivities`.

### Derived vs. Authoritative Content

| Authoritative | Derived |
|---------------|---------|
| Uploaded file bytes | Extracted text, chunks |
| Extracted sections | Embeddings, vector index |
| Source references | Course structure (AI-generated, validated) |
| Learning objectives | Lesson content (derived from objectives + methodology) |

### Reprocessing Rules

- Re-uploading a file with the same SHA-256 reuses existing processing (idempotent).
- Reprocessing creates a new `DocumentVersion`; old versions preserved for traceability.
- Embeddings regenerated only when chunks change or embedding model changes.

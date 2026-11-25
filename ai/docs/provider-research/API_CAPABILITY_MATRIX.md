# AQVERA — AI Capability Matrix

**Date checked:** 2026-11-25
**Purpose:** Matrix of provider capabilities by modality/task. A checkmark (✓) means the provider officially supports the capability; (~) means partial or trial-limited; (—) means not supported.

## Capability definitions

| Capability | Description |
|------------|-------------|
| Text generation | Chat/completion text generation |
| Vision | Image understanding (image-to-text) |
| Embeddings | Text/document embedding vectors |
| Image generation | Text-to-image generation |
| Speech-to-text | Audio transcription (STT) |
| Text-to-speech | Text-to-speech audio generation |
| Reranking | Search result reranking |
| OCR/Document | Document extraction and OCR |
| Web search | Web search and information retrieval |
| Audio (live) | Real-time audio-to-audio / live transcription |
| OpenAI-compatible | Provider API is OpenAI-compatible (drop-in) |

## Capability matrix

| Provider | Text | Vision | Embeddings | Image gen | STT | TTS | Rerank | OCR/Doc | Web search | Audio live | OpenAI-compatible | Free tier |
|----------|------|--------|------------|-----------|-----|-----|--------|---------|------------|------------|-------------------|-----------|
| Google Gemini | ✓ | ✓ | ✓ | ✓ (Nano Banana) | ✓ | ✓ | ✓ (via grounding) | ✓ | ✓ (grounding) | ✓ (Live) | No | Permanent |
| OpenRouter | ✓ | ✓ | ✓ | ✓ | ✓ (via providers) | ✓ (via providers) | ✓ | ✓ | ✓ | ~ | Yes | Permanent |
| Groq | ✓ | ✓ (Qwen3.8) | — | — | ✓ (Whisper) | ✓ (Orpheus) | — | — | — | — | Yes | Permanent |
| NVIDIA NIM | ✓ | ✓ | ✓ | ✓ | ✓ (Whisper) | ✓ | ✓ | ✓ | — | ~ | Yes | Trial (credits) |
| Cerebras | ✓ | — | — | — | — | — | — | — | — | — | Yes | Trial ($5) |
| Together AI | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | — | — | Yes | Paid (min $15) |
| DeepSeek | ✓ | ✓ (Flash) | — | — | ✓ (ASR) | ✓ (TTS) | — | ✓ | ✓ (search) | — | Yes | Trial (5M tokens) |
| Mistral AI | ✓ | ✓ | ✓ | — | ✓ (Voxtral) | ✓ (Voxtral TTS) | — | ✓ (OCR) | — | — | Partial | Paid (API) |
| Hugging Face | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | — | — | — | Yes | None (free acct) |
| Cohere | ✓ | — | ✓ | — | — | — | ✓ | — | — | — | No | Trial |
| SambaNova | ✓ | — | ✓ | — | — | — | — | — | — | — | Yes | Trial |
| Fireworks AI | ✓ | ✓ | — | ✓ | — | — | — | — | — | — | Yes | Trial |
| xAI | ✓ | ✓ | — | — | — | — | — | — | — | — | Yes | Trial |
| ElevenLabs | — | — | — | — | — | ✓ | — | — | — | — | No | Permanent |
| Deepgram | — | — | — | — | ✓ | — | — | — | — | — | No | Trial/Credit |
| AssemblyAI | — | — | — | — | ✓ | — | — | — | — | — | No | Trial/Credit |
| Tavily | — | — | — | — | — | — | — | — | ✓ | — | No | Permanent |
| Brave Search | — | — | — | — | — | — | — | — | ✓ | — | No | Permanent |
| Exa | — | — | — | — | — | — | — | — | ✓ | — | No | Permanent |
| Firecrawl | — | — | — | — | — | — | — | — | ✓ (extract) | — | No | Permanent |
| Jina AI | — | — | ✓ | — | — | — | ✓ | — | ✓ (reader) | — | No | Permanent |
| Azure AI Speech | — | — | — | — | ✓ | ✓ | — | — | — | — | No | Trial/Credit |
| AWS Textract | — | — | — | — | — | — | — | ✓ | — | — | No | Trial (12mo) |
| Azure Doc Intel | — | — | — | — | — | — | — | ✓ | — | — | No | Trial/Credit |
| Stability AI | — | — | — | ✓ | — | — | — | — | — | — | No | Trial/Credit |
| Ollama (local) | ✓ | ~ | ✓ | ~ | — | — | — | — | — | — | Yes | Permanent (local) |

## Notes

- OpenRouter is a router; capabilities depend on the underlying model/provider selected.
- Hugging Face Inference Providers is a router; capabilities depend on the selected provider (Groq, Cerebras, Together, Fireworks, etc.).
- Local (Ollama) capabilities depend on the model downloaded and the hardware available; no API cost.
- "Free tier" column indicates whether a standing permanent free allowance exists (see FREE_TIER_CATALOG.md for details).
- Providers marked TRIAL/CREDIT are not configured for live use in AQVERA by default.

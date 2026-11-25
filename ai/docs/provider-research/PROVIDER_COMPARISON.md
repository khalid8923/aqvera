# AQVERA — Provider Comparison

**Date checked:** 2026-11-25
**Purpose:** Side-by-side comparison of AI providers relevant to AQVERA, to support integration decisions.

## Comparison criteria

| Criterion | Description |
|-----------|-------------|
| Cost | Free vs paid vs trial |
| Free tier | Whether a standing permanent free allowance exists |
| Permanence | Whether free access is permanent or time/credit bounded |
| Ease of integration | OpenAI-compatible vs custom SDK |
| Modalities | What input/output modalities supported |
| Best AQVERA use | Recommended academic use case |
| Blocker | Why it may not be integrated live |

## Provider comparison

| Provider | Cost | Free tier | Permanent | Integration | Modalities | Best AQVERA use | Blocker |
|----------|------|-----------|-----------|-------------|------------|-----------------|---------|
| Google Gemini | Free + paid | Yes | Yes | Native SDK | text, image, audio, video | General tutor, RAG, STT/TTS | None (free tier) |
| OpenRouter | Free + paid | Yes | Yes | OpenAI-compatible | text, image | Multi-model fallback, free models | None (free tier) |
| Groq | Free + paid | Yes | Yes | OpenAI-compatible | text, image, audio | Fast text, STT (Whisper) | None (free tier) |
| NVIDIA NIM | Trial | Credits | No | OpenAI-compatible | text, image, audio, video | Prototyping, vision, embeddings | Trial credits expire |
| Cerebras | Trial | $5 credit | No | OpenAI-compatible | text | Ultra-fast text | Trial requires payment method |
| Together AI | Paid | No | No | OpenAI-compatible | text, image, audio, video | Broad model catalog | Paid only (min $15) |
| DeepSeek | Trial + paid | 5M tokens grant | No | OpenAI-compatible | text, image, audio | Cheap text (off-peak) | Trial grant expires |
| Mistral AI | Paid | No (API) | No | SDK | text, image, audio, doc | OCR, speech (Voxtral) | API paid only |
| Hugging Face | Paid/custom | None (free acct) | No | SDK / OpenAI router | text, image, audio | Multi-provider router, failover | No free credits (free acct) |
| Cohere | Paid | Trial | No | SDK | text | Embeddings, reranking | Trial only |
| SambaNova | Trial | Credits | No | OpenAI-compatible | text | Fast text | Trial only |
| Fireworks AI | Trial | Credits | No | OpenAI-compatible | text, image, audio | Broad model catalog | Trial only |
| xAI | Trial | Credits | No | OpenAI-compatible | text, image | Reasoning (Grok) | Trial only |
| ElevenLabs | Free + paid | Yes | Yes | SDK | audio | TTS (accessibility) | None |
| Deepgram | Trial/Credit | Credits | No | SDK | audio | STT | Credit-based |
| AssemblyAI | Trial/Credit | Credits | No | SDK | audio | STT + intelligence | Credit-based |
| Tavily | Free + paid | Yes | Yes | REST | text | Web research | None |
| Brave Search | Free + paid | Yes | Yes | REST | text | Web search | None |
| Exa | Free + paid | Yes | Yes | REST | text | Web research | None |
| Firecrawl | Free + paid | Yes | Yes | REST | text | Web content extraction | None |
| Jina AI | Free + paid | Yes | Yes | REST | text | Reader, embeddings, rerank | None |
| Azure AI Speech | Trial/Credit | Credits | No | SDK | audio | STT/TTS (enterprise) | Requires Azure account |
| AWS Textract | Free Tier (12mo) | Credits | No | SDK | document | OCR/document extraction | Requires AWS account |
| Azure Doc Intel | Trial/Credit | Credits | No | SDK | document | OCR/document extraction | Requires Azure account |
| Stability AI | Trial/Credit | Credits | No | REST | image | Image generation | Trial only |
| Ollama (local) | Free (local) | Yes (local) | Yes | REST / OpenAI-compat | text | Local offline inference | Hardware-dependent |

## Recommendations for AQVERA initial integration

| Priority | Provider | Rationale |
|----------|----------|-----------|
| 1 | Google Gemini | Permanent free tier, strong multimodal (text/vision/audio), official SDK, good for tutor and RAG |
| 2 | OpenRouter | Single key for 600+ models, free models available, OpenAI-compatible, good fallback |
| 3 | Groq | Very fast inference, free tier, OpenAI-compatible, Whisper STT |
| 4 | NVIDIA NIM | OpenAI-compatible, 40+ models, good for prototyping (trial credits) |
| 5 | ElevenLabs | TTS for accessibility (permanent free tier) |
| 6 | Ollama (local) | Zero API cost, works offline, optional |

## Providers NOT integrated live (default)

All providers requiring a payment method or credit purchase (Together AI, Mistral AI API, Cohere, Cerebras after trial, DeepSeek after grant, etc.) are implemented as adapters but labeled NOT CONFIGURED. No credentials are present in this repository.

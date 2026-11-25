# AQVERA — AI Provider Research Catalog

**Date checked:** 2026-11-25
**Source:** Official provider documentation and pricing pages
**Purpose:** Inventory of AI providers, APIs, models, and services relevant to AQVERA.

## How to read this catalog

- Each entry lists the provider/service name, official website, official API docs, supported tasks/modalities, available models, authentication, free-tier status, limits, and suitability for AQVERA.
- "Free tier" means a standing no-cost allowance (not a one-time trial). Time-limited or credit-bounded trials are marked as TRIAL, not free.
- Pricing claims include the official source URL and the date verified.
- Model families are listed per provider; individual models are NOT counted as separate provider integrations.

---

## 1. Google Gemini (Google AI Studio / Gemini API)

| Field | Value |
|-------|-------|
| Provider | Google |
| Service | Gemini Developer API |
| Official website | https://ai.google.dev/ |
| Official API docs | https://aistudio.google.com/docs/ |
| Supported tasks | Text generation, chat, vision, audio (STT/TTS/Live), embeddings, image understanding, image generation (Nano Banana), grounding/web search |
| Modalities | text, image, audio, video |
| Available models | gemini-3.5-flash-lite, gemini-3.6-flash, gemini-3.8-flash, gemini-4-hydrogen, gemini-4-neon, gemini-4-carbon, gemini-3.5-transcribe, gemini-3.8-flash-tts, gemini-3.1-flash-image |
| Officially supported API | Yes |
| Authentication | API key (Google AI Studio / Google Cloud) |
| Free tier | Yes — free input & output tokens for certain models (e.g. gemini-3.5-flash-lite, gemini-3.6-flash, gemini-3.8-flash) with rate limits |
| Free tier type | Permanent free tier with rate limits (some models not available on free tier) |
| Documented request limits | Rate limits per model (RPM/RPD/TPM); see https://ai.google.dev/gemini-api/docs/rate-limits |
| Token limits | Up to 1M context on several models |
| Payment method required | No for free tier; required for paid tiers |
| Billing can be disabled | Yes |
| Geographic restrictions | Available in most countries; some regions restricted |
| Data retention | Free tier content may be used to improve products; paid tier opts out |
| Integration SDK | Google AI SDK, OpenAI-compatible not required (native REST) |
| OpenAI-compatible | No (native API) |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — strong free tier, multimodal, academic tasks |
| Source (pricing/quota) | https://aistudio.google.com/docs/pricing (checked 2026-11-25) |

---

## 2. OpenRouter

| Field | Value |
|-------|-------|
| Provider | OpenRouter |
| Service | Unified model router API |
| Official website | https://openrouter.ai/ |
| Official API docs | https://openrouter.ai/docs/ |
| Supported tasks | Text generation, chat, vision, structured output, tool calling |
| Modalities | text, image |
| Available models | 600+ models across 80+ providers (paid plans); 25+ free models (free plan) |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Yes — 25+ free models, 4 free providers |
| Free tier type | Permanent free tier (rate-limited: 20 req/min, 50 req/day; rises to 1000/day after $10 credit purchase) |
| Documented request limits | 50 requests/day (free), 20 req/min; paid plans passthrough provider limits |
| Token limits | Model-dependent (up to 1M+ context) |
| Payment method required | No for free tier; required to buy credits |
| Billing can be disabled | Yes |
| Geographic restrictions | Not available in EU for in-region routing (some models) |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI SDK (drop-in, base URL swap) |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — single key for many models, free models available |
| Source (pricing/quota) | https://openrouter.ai/pricing (checked 2026-11-25); https://openrouter.ai/docs/faq |

---

## 3. Groq

| Field | Value |
|-------|-------|
| Provider | Groq |
| Service | GroqCloud inference API |
| Official website | https://groq.com/ |
| Official API docs | https://console.groq.com/docs/ |
| Supported tasks | Text generation, chat, vision (Qwen3.8), speech-to-text (Whisper), text-to-speech (Orpheus), prompt guard |
| Modalities | text, image, audio |
| Available models | gpt-oss-120b, gpt-oss-20b, qwen/qwen3.8-27b, whisper-large-v3, whisper-large-v3-turbo, canopylabs/orpheus-*, meta-llama/llama-prompt-guard-2-* |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Yes — free tier with rate limits (no credit card required to start) |
| Free tier type | Permanent free tier with rate limits |
| Documented request limits | Free: e.g. gpt-oss-120b 30 RPM, 1K RPD, 8K TPM; whisper-large-v3 20 RPM, 7.2K audio-sec/hour; see https://console.groq.com/docs/rate-limits |
| Token limits | Up to 131K context (gpt-oss), 196K (MiniMax M2.7) |
| Payment method required | No for free tier; required for Developer tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI SDK (drop-in) |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — very fast inference, free tier, STT via Whisper |
| Source (pricing/quota) | https://console.groq.com/docs/models and https://console.groq.com/docs/rate-limits (checked 2026-11-25) |

---

## 4. NVIDIA NIM (API Catalog)

| Field | Value |
|-------|-------|
| Provider | NVIDIA |
| Service | NVIDIA NIM hosted inference endpoints |
| Official website | https://build.nvidia.com/ |
| Official API docs | https://docs.api.nvidia.com/nim/ |
| Supported tasks | Text generation, chat, vision, embeddings, reranking, image generation, speech, video, document parsing, OCR, content safety |
| Modalities | text, image, audio, video |
| Available models | 40+ models: nemotron-3.5-*, llama-3.1-*, deepseek-ai/deepseek-v4-flash, google/gemma-*, moonshotai/kimi-*, z-ai/glm-*, whisper-large-v3, Qwen image, FLUX, etc. |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Trial credits — 1,000 free trial credits on signup (no credit card), 90-day evaluation window |
| Free tier type | TRIAL (time- and credit-bounded, NOT permanently free) |
| Documented request limits | ~40 RPM, model-dependent TPM; trial credits consumed per request |
| Token limits | Model-dependent (up to 1M context) |
| Payment method required | No for trial; required for production (NVIDIA AI Enterprise) |
| Billing can be disabled | Yes |
| Geographic restrictions | Corporate email required for extended credits; not all countries |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI SDK (drop-in) |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Yes for prototyping; trial credits expire, so not a permanent free source |
| Source (pricing/quota) | https://build.nvidia.com/llms.txt and https://docs.api.nvidia.com/nim/docs/run-anywhere (checked 2026-11-25) |

---

## 5. Cerebras

| Field | Value |
|-------|-------|
| Provider | Cerebras |
| Service | Cerebras Inference API |
| Official website | https://www.cerebras.ai/ |
| Official API docs | https://inference-docs.cerebras.ai/ |
| Supported tasks | Text generation, chat |
| Modalities | text |
| Available models | gpt-oss-120b, qwen-3.8-27b |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | No — $5 one-time Free Trial credit after adding a verified payment method, expires 30 days |
| Free tier type | TRIAL (time- and credit-bounded, NOT permanently free) |
| Documented request limits | Free Trial: gpt-oss-120b 5 RPM, 30K uncached TPM, 1M TPD; qwen-3.8-27b 300 RPM, 150K uncached TPM |
| Token limits | gpt-oss-120b 131K context; qwen-3.8-27b 128K context |
| Payment method required | Yes (to activate trial) |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only, not permanently free; useful for short-term prototyping |
| Source (pricing/quota) | https://www.cerebras.ai/pricing and https://inference-docs.cerebras.ai/support/rate-limits (checked 2026-11-25) |

---

## 6. Together AI

| Field | Value |
|-------|-------|
| Provider | Together AI |
| Service | Together Serverless Inference |
| Official website | https://together.ai/ |
| Official API docs | https://docs.together.ai/ |
| Supported tasks | Text generation, chat, vision, image generation, audio, embeddings, reranking, moderation |
| Modalities | text, image, audio, video |
| Available models | 200+ models: DeepSeek, Qwen, Kimi, Llama, GLM, FLUX, SDXL, etc. |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | No — requires minimum $15 credit purchase; no free trial |
| Free tier type | N/A (paid only; some free model endpoints with reduced rate limits exist but require account) |
| Documented request limits | Model-dependent |
| Token limits | Model-dependent |
| Payment method required | Yes |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible, Together SDK |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — paid only, no permanent free tier; not ideal for zero-budget competition project |
| Source (pricing/quota) | https://www.together.ai/pricing and https://docs.together.ai/docs/billing-credits (checked 2026-11-25) |

---

## 7. DeepSeek

| Field | Value |
|-------|-------|
| Provider | DeepSeek |
| Service | DeepSeek API Platform |
| Official website | https://www.deepseek.com/ |
| Official API docs | https://api-docs.deepseek.com/ |
| Supported tasks | Text generation, chat, vision, search, file parsing/OCR, TTS, ASR |
| Modalities | text, image, audio |
| Available models | deepseek-flash (V4.1-Flash-1017), deepseek-v4-pro |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | One-time grant — 5M free tokens on signup (no credit card), ~30-day validity; NOT permanently free |
| Free tier type | TRIAL (one-time grant, NOT permanently free) |
| Documented request limits | Concurrency limits (2500 for flash, 500 for pro); no per-minute caps published |
| Token limits | 1M context |
| Payment method required | No for trial grant; required after grant exhausted |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible, Anthropic-compatible |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — one-time grant only; cheap off-peak pricing but not permanently free |
| Source (pricing/quota) | https://api-docs.deepseek.com/quick_start/pricing/ (checked 2026-11-25) |

---

## 8. Mistral AI

| Field | Value |
|-------|-------|
| Provider | Mistral AI |
| Service | Mistral Inference API |
| Official website | https://mistral.ai/ |
| Official API docs | https://docs.mistral.ai/ |
| Supported tasks | Text generation, chat, vision, OCR, speech (Voxtral), embeddings, code, moderation |
| Modalities | text, image, audio, document |
| Available models | Mistral Large 4, Mistral Small 4, Ministral 3 (3B/8B/14B), Codestral, Voxtral, Mistral Embed, OCR models |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | No — Free plan does NOT include API access; API requires billing activation and pay-as-you-go |
| Free tier type | N/A for API (paid only) |
| Documented request limits | Organization monthly spending limit; model-dependent rate limits |
| Token limits | Model-dependent (up to 1M context) |
| Payment method required | Yes for API |
| Billing can be disabled | Yes |
| Geographic restrictions | Global and EU endpoints |
| Data retention | Provider-dependent |
| Integration SDK | Mistral SDK, OpenAI-compatible |
| OpenAI-compatible | Partially |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — API is paid only; not suitable for zero-budget free-tier objective |
| Source (pricing/quota) | https://docs.mistral.ai/inference/pricing and https://docs.mistral.ai/admin/billing-usage/usage-limits (checked 2026-11-25) |

---

## 9. Hugging Face Inference Providers

| Field | Value |
|-------|-------|
| Provider | Hugging Face |
| Service | Inference Providers (router) |
| Official website | https://huggingface.co/ |
| Official API docs | https://huggingface.co/docs/inference-providers/ |
| Supported tasks | Text generation, chat, vision, embeddings, feature extraction, text-to-image, speech-to-text |
| Modalities | text, image, audio |
| Available models | 133+ chat models via providers: Cerebras, Cohere, DeepInfra, Fireworks, Groq, Together, SambaNova, HF Inference, etc. |
| Officially supported API | Yes |
| Authentication | HF User Access Token |
| Free tier | None for free accounts (no monthly credits); PRO $9/mo includes $2 credits; can use custom provider keys (provider bills directly, HF charges nothing) |
| Free tier type | N/A for default routing; custom provider keys inherit provider's own free tier |
| Documented request limits | HF rate limits per account tier; provider-dependent limits when using custom keys |
| Token limits | Model-dependent |
| Payment method required | No for custom provider keys; yes for HF-billed usage beyond credits |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | HF Inference SDK (JS/Python) |
| OpenAI-compatible | Yes (router.huggingface.co/v1) |
| Integration complexity | Low |
| Suitable for AQVERA | Yes as a multi-provider router with automatic failover; custom keys avoid HF charges |
| Source (pricing/quota) | https://huggingface.co/docs/inference-providers/pricing (checked 2026-11-25) |

---

## 10. Cohere

| Field | Value |
|-------|-------|
| Provider | Cohere |
| Service | Cohere API |
| Official website | https://cohere.com/ |
| Official API docs | https://docs.cohere.com/ |
| Supported tasks | Text generation, chat, embeddings (Embed), reranking (Rerank), classification |
| Modalities | text |
| Available models | Command R/R+, Embed, Rerank models |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Limited free trial credits; not permanently free |
| Free tier type | TRIAL |
| Documented request limits | Trial-based |
| Token limits | Model-dependent |
| Payment method required | Yes after trial |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | Cohere SDK |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only; good for embeddings/reranking but paid |
| Source (pricing/quota) | https://docs.cohere.com/ (checked 2026-11-25) |

---

## 11. SambaNova

| Field | Value |
|-------|-------|
| Provider | SambaNova |
| Service | SambaNova Cloud / API |
| Official website | https://sambanova.ai/ |
| Official API docs | https://docs.sambanova.ai/ |
| Supported tasks | Text generation, chat, embeddings |
| Modalities | text |
| Available models | Llama-*, Qwen-*, DeepSeek-* (via SambaNova Cloud) |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free credits; not permanently free |
| Free tier type | TRIAL |
| Documented request limits | Trial-based |
| Token limits | Model-dependent |
| Payment method required | Yes after trial |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only |
| Source (pricing/quota) | https://docs.sambanova.ai/ (checked 2026-11-25) |

---

## 12. Fireworks AI

| Field | Value |
|-------|-------|
| Provider | Fireworks AI |
| Service | Fireworks inference API |
| Official website | https://fireworks.ai/ |
| Official API docs | https://docs.fireworks.ai/ |
| Supported tasks | Text generation, chat, vision, image generation, audio |
| Modalities | text, image, audio |
| Available models | DeepSeek, Qwen, Llama, FLUX, etc. |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Limited free credits; not permanently free |
| Free tier type | TRIAL |
| Documented request limits | Trial-based |
| Token limits | Model-dependent |
| Payment method required | Yes after trial |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only |
| Source (pricing/quota) | https://docs.fireworks.ai/ (checked 2026-11-25) |

---

## 13. xAI (Grok)

| Field | Value |
|-------|-------|
| Provider | xAI |
| Service | xAI API |
| Official website | https://x.ai/ |
| Official API docs | https://docs.x.ai/ |
| Supported tasks | Text generation, chat, vision |
| Modalities | text, image |
| Available models | grok-*, grok-vision-* |
| Officially supported API | Yes |
| Authentication | API key (Bearer) |
| Free tier | Limited trial credits; not permanently free |
| Free tier type | TRIAL |
| Documented request limits | Trial-based |
| Token limits | Model-dependent |
| Payment method required | Yes after trial |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | OpenAI-compatible |
| OpenAI-compatible | Yes |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only |
| Source (pricing/quota) | https://docs.x.ai/ (checked 2026-11-25) |

---

## 14. ElevenLabs

| Field | Value |
|-------|-------|
| Provider | ElevenLabs |
| Service | Text-to-speech API |
| Official website | https://elevenlabs.io/ |
| Official API docs | https://elevenlabs.io/docs/ |
| Supported tasks | Text-to-speech, speech-to-speech, voice cloning |
| Modalities | audio |
| Available models | ElevenLabs TTS models |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier (character quota per month) |
| Free tier type | Permanent free tier with monthly character quota |
| Documented request limits | Monthly character quota |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | ElevenLabs SDK |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — TTS for accessibility/spoken explanations |
| Source (pricing/quota) | https://elevenlabs.io/pricing (checked 2026-11-25) |

---

## 15. Deepgram

| Field | Value |
|-------|-------|
| Provider | Deepgram |
| Service | Speech-to-text API |
| Official website | https://deepgram.com/ |
| Official API docs | https://developers.deepgram.com/ |
| Supported tasks | Speech-to-text, audio transcription |
| Modalities | audio |
| Available models | Nova-2, etc. |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier (credit-based) |
| Free tier type | TRIAL/CREDIT |
| Documented request limits | Credit-based |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | Deepgram SDK |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — STT for lecture transcription |
| Source (pricing/quota) | https://developers.deepgram.com/ (checked 2026-11-25) |

---

## 16. AssemblyAI

| Field | Value |
|-------|-------|
| Provider | AssemblyAI |
| Service | Speech-to-text / audio intelligence API |
| Official website | https://www.assemblyai.com/ |
| Official API docs | https://www.assemblyai.com/docs/ |
| Supported tasks | Speech-to-text, transcription, summarization, sentiment |
| Modalities | audio |
| Available models | Conformer, etc. |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier (credit-based) |
| Free tier type | TRIAL/CREDIT |
| Documented request limits | Credit-based |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | AssemblyAI SDK |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — STT with audio intelligence |
| Source (pricing/quota) | https://www.assemblyai.com/pricing (checked 2026-11-25) |

---

## 17. Tavily (Web Search)

| Field | Value |
|-------|-------|
| Provider | Tavily |
| Service | Search API |
| Official website | https://tavily.com/ |
| Official API docs | https://docs.tavily.com/ |
| Supported tasks | Web search, information retrieval |
| Modalities | text |
| Available models | tavily-search |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier (search requests/month) |
| Free tier type | Permanent free tier with monthly quota |
| Documented request limits | Monthly search quota |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | Tavily SDK, REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — web research task |
| Source (pricing/quota) | https://docs.tavily.com/ (checked 2026-11-25) |

---

## 18. Brave Search API

| Field | Value |
|-------|-------|
| Provider | Brave |
| Service | Brave Search API |
| Official website | https://brave.com/ |
| Official API docs | https://search.brave.com/ |
| Supported tasks | Web search |
| Modalities | text |
| Available models | Brave Search |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier (queries/month) |
| Free tier type | Permanent free tier with monthly quota |
| Documented request limits | Monthly query quota |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — web research task |
| Source (pricing/quota) | https://search.brave.com/ (checked 2026-11-25) |

---

## 19. Exa

| Field | Value |
|-------|-------|
| Provider | Exa |
| Service | Web search API |
| Official website | https://exa.ai/ |
| Official API docs | https://docs.exa.ai/ |
| Supported tasks | Web search, information retrieval |
| Modalities | text |
| Available models | exa-search |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier |
| Free tier type | Permanent free tier with monthly quota |
| Documented request limits | Monthly search quota |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — web research task |
| Source (pricing/quota) | https://docs.exa.ai/ (checked 2026-11-25) |

---

## 20. Firecrawl

| Field | Value |
|-------|-------|
| Provider | Firecrawl |
| Service | Web scraping/crawling API |
| Official website | https://www.firecrawl.dev/ |
| Official API docs | https://firecrawl.dev/ |
| Supported tasks | Web crawling, content extraction |
| Modalities | text |
| Available models | firecrawl-scrape |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier |
| Free tier type | Permanent free tier with monthly quota |
| Documented request limits | Monthly crawl quota |
| Token limits | N/A |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — web content extraction for research |
| Source (pricing/quota) | https://firecrawl.dev/ (checked 2026-11-25) |

---

## 21. Jina AI

| Field | Value |
|-------|-------|
| Provider | Jina AI |
| Service | Jina Reader / Search API |
| Official website | https://jina.ai/ |
| Official API docs | https://docs.jina.ai/ |
| Supported tasks | Web page reading, search, embeddings, reranking |
| Modalities | text |
| Available models | jina-reader, jina-embeddings, jina-reranker |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free tier |
| Free tier type | Permanent free tier with rate limits |
| Documented request limits | Rate-limited |
| Token limits | Model-dependent |
| Payment method required | No for free tier |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Yes — reader/search for research |
| Source (pricing/quota) | https://docs.jina.ai/ (checked 2026-11-25) |

---

## 22. Azure AI Speech

| Field | Value |
|-------|-------|
| Provider | Microsoft Azure |
| Service | Azure AI Speech |
| Official website | https://azure.microsoft.com/ |
| Official API docs | https://learn.microsoft.com/azure/ai-services/speech-service/ |
| Supported tasks | Speech-to-text, text-to-speech, speech translation |
| Modalities | audio |
| Available models | Azure Speech models |
| Officially supported API | Yes |
| Authentication | API key / Azure AD |
| Free tier | Limited free tier (credit-based, requires Azure account) |
| Free tier type | TRIAL/CREDIT |
| Documented request limits | Credit-based |
| Token limits | N/A |
| Payment method required | No for free tier (Azure account required) |
| Billing can be disabled | Yes |
| Geographic restrictions | Azure regions |
| Data retention | Provider-dependent |
| Integration SDK | Azure Speech SDK |
| OpenAI-compatible | No |
| Integration complexity | Medium |
| Suitable for AQVERA | Yes — STT/TTS (enterprise-grade) |
| Source (pricing/quota) | https://azure.microsoft.com/ (checked 2026-11-25) |

---

## 23. AWS Textract

| Field | Value |
|-------|-------|
| Provider | AWS |
| Service | Amazon Textract |
| Official website | https://aws.amazon.com/ |
| Official API docs | https://docs.aws.amazon.com/textract/ |
| Supported tasks | OCR, document intelligence, form/table extraction |
| Modalities | document (image/PDF) |
| Available models | Textract |
| Officially supported API | Yes |
| Authentication | AWS IAM / API key |
| Free tier | Limited free tier (AWS Free Tier) |
| Free tier type | TRIAL (12 months) |
| Documented request limits | AWS Free Tier limits |
| Token limits | N/A |
| Payment method required | No for free tier (AWS account required) |
| Billing can be disabled | Yes |
| Geographic restrictions | AWS regions |
| Data retention | Provider-dependent |
| Integration SDK | AWS SDK (boto3) |
| OpenAI-compatible | No |
| Integration complexity | Medium |
| Suitable for AQVERA | Yes — document OCR/extraction (requires AWS account) |
| Source (pricing/quota) | https://aws.amazon.com/textract/pricing/ (checked 2026-11-25) |

---

## 24. Azure Document Intelligence

| Field | Value |
|-------|-------|
| Provider | Microsoft Azure |
| Service | Azure Document Intelligence (formerly Form Recognizer) |
| Official website | https://azure.microsoft.com/ |
| Official API docs | https://learn.microsoft.com/azure/ai-services/document-intelligence/ |
| Supported tasks | OCR, document extraction, layout analysis |
| Modalities | document (image/PDF) |
| Available models | Document Intelligence models |
| Officially supported API | Yes |
| Authentication | API key / Azure AD |
| Free tier | Limited free tier (credit-based, requires Azure account) |
| Free tier type | TRIAL/CREDIT |
| Documented request limits | Credit-based |
| Token limits | N/A |
| Payment method required | No for free tier (Azure account required) |
| Billing can be disabled | Yes |
| Geographic restrictions | Azure regions |
| Data retention | Provider-dependent |
| Integration SDK | Azure SDK |
| OpenAI-compatible | No |
| Integration complexity | Medium |
| Suitable for AQVERA | Yes — document intelligence (requires Azure account) |
| Source (pricing/quota) | https://azure.microsoft.com/ (checked 2026-11-25) |

---

## 25. Stability AI

| Field | Value |
|-------|-------|
| Provider | Stability AI |
| Service | Stability API |
| Official website | https://stability.ai/ |
| Official API docs | https://platform.stability.ai/ |
| Supported tasks | Image generation |
| Modalities | image |
| Available models | SD XL, SD 3.5, etc. |
| Officially supported API | Yes |
| Authentication | API key |
| Free tier | Limited free credits; not permanently free |
| Free tier type | TRIAL/CREDIT |
| Documented request limits | Credit-based |
| Token limits | N/A |
| Payment method required | Yes after trial |
| Billing can be disabled | Yes |
| Geographic restrictions | Generally available |
| Data retention | Provider-dependent |
| Integration SDK | REST |
| OpenAI-compatible | No |
| Integration complexity | Low |
| Suitable for AQVERA | Limited — trial only; image generation |
| Source (pricing/quota) | https://platform.stability.ai/ (checked 2026-11-25) |

---

## 26. Local inference (Ollama / LM Studio)

| Field | Value |
|-------|-------|
| Provider | Local runtime |
| Service | Ollama / LM Studio local inference |
| Official website | https://ollama.com/ |
| Official API docs | https://github.com/ollama/ollama/blob/main/docs/api.md |
| Supported tasks | Text generation, chat, embeddings (local models) |
| Modalities | text |
| Available models | Any model downloaded locally (Llama, Qwen, Mistral, etc.) |
| Officially supported API | Yes (Ollama REST API) |
| Authentication | None (local) |
| Free tier | Free (self-hosted, hardware-dependent) |
| Free tier type | Permanent free (no API cost; hardware cost only) |
| Documented request limits | Hardware-dependent (RAM, GPU) |
| Token limits | Model context window |
| Payment method required | No |
| Billing can be disabled | N/A |
| Geographic restrictions | None |
| Data retention | Local only (no external provider) |
| Integration SDK | Ollama REST API, OpenAI-compatible |
| OpenAI-compatible | Yes (via Ollama OpenAI-compatible endpoint) |
| Integration complexity | Medium (requires local install) |
| Suitable for AQVERA | Yes — optional local inference, zero API cost, works offline |
| Source (pricing/quota) | https://ollama.com/ (checked 2026-11-25) |

---

## Classification summary

| Category | Providers |
|----------|-----------|
| Verified and usable (free tier available) | Google Gemini, OpenRouter, Groq, Hugging Face (via custom keys), ElevenLabs, Tavily, Brave Search, Exa, Firecrawl, Jina AI, Local (Ollama) |
| Verified but requires user credentials (trial) | NVIDIA NIM, Cerebras, DeepSeek, Mistral AI, Together AI, SambaNova, Fireworks AI, xAI, Azure AI Speech, AWS Textract, Azure Document Intelligence, Stability AI, Deepgram, AssemblyAI |
| Verified but paid | Cohere (primarily paid) |
| Not suitable (no permanent free, paid only) | Together AI (API), Mistral AI (API) |
| Could not verify | None (all checked against official docs) |

**Note:** No provider API key is configured in this repository. All adapters are implemented and contract-tested with mocks. Providers are labeled NOT CONFIGURED until a valid API key is added via environment variables.

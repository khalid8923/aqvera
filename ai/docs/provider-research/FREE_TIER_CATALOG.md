# AQVERA — Free Tier Catalog

**Date checked:** 2026-11-25
**Purpose:** Catalog of AI providers with verified free access, distinguishing permanent free tiers from trials and paid plans.

## Classification rules

- **PERMANENT FREE**: Standing no-cost allowance that renews or does not expire. May be rate-limited.
- **TRIAL**: Time-limited or credit-bounded; expires. Not a permanent free service.
- **PAID**: Requires payment method / credit purchase to use. No standing free allowance.
- **NOT CONFIGURED**: Provider adapter implemented but no API key present in this repository.

---

## Permanent free tiers (verified)

| Provider | Free allowance | Rate limits | Payment method required | Expiry | Source | Verified |
|----------|---------------|-------------|------------------------|--------|--------|----------|
| Google Gemini | Free input & output tokens for certain models (e.g. gemini-3.5-flash-lite, gemini-3.6-flash, gemini-3.8-flash) | Per-model RPM/RPD/TPM | No | None (standing tier) | https://aistudio.google.com/docs/pricing | 2026-11-25 |
| OpenRouter | 25+ free models, 4 free providers | 20 req/min, 50 req/day (rises to 1000/day after $10 credit purchase) | No | None | https://openrouter.ai/pricing | 2026-11-25 |
| Groq | Free tier on gpt-oss, whisper, orpheus models | e.g. gpt-oss-120b: 30 RPM, 1K RPD, 8K TPM; whisper-large-v3: 20 RPM, 7.2K audio-sec/hour | No | None | https://console.groq.com/docs/rate-limits | 2026-11-25 |
| ElevenLabs | Monthly character quota (TTS) | Monthly character quota | No | None | https://elevenlabs.io/pricing | 2026-11-25 |
| Tavily | Monthly search quota | Monthly quota | No | None | https://docs.tavily.com/ | 2026-11-25 |
| Brave Search | Monthly query quota | Monthly quota | No | None | https://search.brave.com/ | 2026-11-25 |
| Exa | Monthly search quota | Monthly quota | No | None | https://docs.exa.ai/ | 2026-11-25 |
| Firecrawl | Monthly crawl quota | Monthly quota | No | None | https://firecrawl.dev/ | 2026-11-25 |
| Jina AI | Rate-limited free tier | Rate-limited | No | None | https://docs.jina.ai/ | 2026-11-25 |
| Ollama (local) | Free (self-hosted, hardware-dependent) | Hardware-dependent | No | None | https://ollama.com/ | 2026-11-25 |

## Trials / credit-bounded (NOT permanent free)

| Provider | Trial allowance | Expiry | Payment method required | Source | Verified |
|----------|----------------|--------|------------------------|--------|----------|
| NVIDIA NIM | 1,000 free trial credits (no credit card), 90-day evaluation window | 90 days | No | https://build.nvidia.com/llms.txt | 2026-11-25 |
| Cerebras | $5 one-time credit after adding verified payment method | 30 days | Yes | https://www.cerebras.ai/pricing | 2026-11-25 |
| DeepSeek | 5M free tokens on signup (~30 days) | ~30 days | No (until grant used) | https://api-docs.deepseek.com/ | 2026-11-25 |
| Mistral AI | Free plan does NOT include API access | N/A | Yes for API | https://docs.mistral.ai/ | 2026-11-25 |
| Together AI | No free trial; min $15 purchase | N/A | Yes | https://docs.together.ai/docs/billing-credits | 2026-11-25 |
| Hugging Face Inference Providers | No monthly credits for free accounts; use custom provider keys | N/A | No (custom keys) | https://huggingface.co/docs/inference-providers/pricing | 2026-11-25 |
| Cohere | Limited free trial credits | Trial-based | Yes after trial | https://docs.cohere.com/ | 2026-11-25 |
| SambaNova | Limited free credits | Trial-based | Yes after trial | https://docs.sambanova.ai/ | 2026-11-25 |
| Fireworks AI | Limited free credits | Trial-based | Yes after trial | https://docs.fireworks.ai/ | 2026-11-25 |
| xAI | Limited trial credits | Trial-based | Yes after trial | https://docs.x.ai/ | 2026-11-25 |
| Azure AI Speech | Limited free tier (Azure account) | Credit-based | No (Azure account) | https://azure.microsoft.com/ | 2026-11-25 |
| AWS Textract | AWS Free Tier (12 months) | 12 months | No (AWS account) | https://aws.amazon.com/textract/pricing/ | 2026-11-25 |
| Azure Document Intelligence | Limited free tier (Azure account) | Credit-based | No (Azure account) | https://azure.microsoft.com/ | 2026-11-25 |
| Stability AI | Limited free credits | Trial-based | Yes after trial | https://platform.stability.ai/ | 2026-11-25 |
| Deepgram | Limited free tier (credit-based) | Credit-based | No | https://developers.deepgram.com/ | 2026-11-25 |
| AssemblyAI | Limited free tier (credit-based) | Credit-based | No | https://www.assemblyai.com/pricing | 2026-11-25 |

## Paid only (no standing free tier)

| Provider | Notes | Source | Verified |
|----------|-------|--------|----------|
| Together AI | API requires $15 minimum credit purchase; no free trial | https://docs.together.ai/docs/billing-credits | 2026-11-25 |
| Mistral AI | API requires billing activation and pay-as-you-go | https://docs.mistral.ai/admin/billing-usage/usage-limits | 2026-11-25 |

## AQVERA default policy

- Paid provider usage is **disabled by default**.
- Paid budget set to zero by default.
- No automatic credit purchase, no automatic account upgrade.
- Prefer verified permanent free-tier options when appropriate.
- Providers marked TRIAL or PAID are NOT integrated for live use unless the operator explicitly enables them and supplies credentials.

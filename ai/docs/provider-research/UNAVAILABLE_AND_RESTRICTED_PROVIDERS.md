# AQVERA — Unavailable and Restricted Providers

**Date checked:** 2026-11-25
**Purpose:** Honest classification of providers that could not be verified, are unavailable, restricted, or unsuitable for AQVERA.

## Could not verify

None. All providers listed in PROVIDER_CATALOG.md were checked against official documentation and pricing pages on 2026-11-25.

## Trial / credit-bounded (not permanent free)

These providers offer trials but no standing permanent free tier. They are implemented as adapters but labeled NOT CONFIGURED and are not used for live AQVERA features unless the operator explicitly supplies credentials and enables paid usage.

| Provider | Trial type | Expiry | Payment required | Reason not live |
|----------|-----------|--------|------------------|-----------------|
| NVIDIA NIM | 1,000 free trial credits | 90 days | No | Trial credits expire; not permanent free |
| Cerebras | $5 credit after payment method | 30 days | Yes | Requires payment method; trial expires |
| DeepSeek | 5M tokens signup grant | ~30 days | No (until grant used) | One-time grant; not permanent |
| Cohere | Limited free trial credits | Trial-based | Yes after trial | Trial only |
| SambaNova | Limited free credits | Trial-based | Yes after trial | Trial only |
| Fireworks AI | Limited free credits | Trial-based | Yes after trial | Trial only |
| xAI | Limited trial credits | Trial-based | Yes after trial | Trial only |
| Stability AI | Limited free credits | Trial-based | Yes after trial | Trial only |
| Deepgram | Limited free tier (credit-based) | Credit-based | No | Credit-based |
| AssemblyAI | Limited free tier (credit-based) | Credit-based | No | Credit-based |
| Azure AI Speech | Limited free tier (Azure account) | Credit-based | No (Azure account) | Requires Azure account |
| AWS Textract | AWS Free Tier | 12 months | No (AWS account) | Time-bounded free tier |
| Azure Document Intelligence | Limited free tier (Azure account) | Credit-based | No (Azure account) | Requires Azure account |

## Paid only (no standing free tier)

| Provider | Reason not live |
|----------|-----------------|
| Together AI | API requires minimum $15 credit purchase; no free trial |
| Mistral AI | API requires billing activation and pay-as-you-go; free plan excludes API |

## Not suitable for AQVERA (default)

| Provider | Reason |
|----------|--------|
| Together AI | Paid only; conflicts with zero-budget default |
| Mistral AI (API) | Paid only; conflicts with zero-budget default |

## AQVERA default stance

All providers in this document are **NOT CONFIGURED** in this repository. No API keys are present. Adapters exist where integration complexity is low (OpenAI-compatible providers), but live use requires explicit operator action: obtain credentials, add to environment, enable paid budget (default zero), and test. Until then, providers report `NOT CONFIGURED` and AQVERA degrades gracefully.

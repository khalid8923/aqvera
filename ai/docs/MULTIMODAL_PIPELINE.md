# Multimodal Pipeline

## Overview

AQVERA supports modular multimodal capabilities. AQVERA does not assume every
provider supports every task — capability-based provider interfaces let the
system route each modality to a capable provider or degrade gracefully.

## Interfaces

| Interface | Responsibility |
|-----------|----------------|
| `ImageProcessor` | Image understanding, OCR, diagram interpretation. |
| `AudioProcessor` | Speech-to-text, text-to-speech. |
| `VideoProcessor` | Video metadata, transcription, summarization. |

## Image Intelligence

- Image understanding and academic diagram interpretation.
- OCR (Arabic + English where the engine supports it).
- Image question answering.
- Text and equation extraction where supported.
- Image descriptions for accessibility.
- **Not** presented as accurate scientific diagrams without validation.

## Audio

- Speech-to-text (Arabic + English where provider allows).
- Text-to-speech.
- Audio lesson generation, lecture transcription, transcript correction.
- Playback controls, captions, transcript synchronization.

## Video

- Video metadata and validation.
- Audio extraction where technically and legally appropriate.
- Speech transcription, timestamped segments.
- Key-point extraction, chapter generation, summarization.
- Video Q&A only when a compatible provider supports it.
- **Policy:** Complete user videos are not uploaded to arbitrary providers
  without a clearly configured processing policy. Only necessary content is
  extracted; data flow is documented.

## Provider Status

No multimodal provider is configured. All interfaces are defined; adapters are
not yet implemented. Marked **NOT CONFIGURED**.

## Accessibility

Image descriptions, captions, and transcripts support accessibility. All
multimodal output includes text alternatives.

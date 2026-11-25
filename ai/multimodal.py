"""Multimodal capabilities: image, audio, video processing.

Capability-based interfaces — AQVERA does not assume every provider supports
every task. Each modality has a provider-agnostic interface and adapters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ImageAnalysis:
    description: str
    text_extracted: Optional[str] = None  # OCR result
    equations: Optional[str] = None
    academic_diagram: Optional[str] = None  # interpretation, not asserted as accurate
    confidence: float = 0.0


@dataclass
class AudioTranscription:
    text: str
    language: Optional[str] = None
    duration_seconds: Optional[float] = None
    segments: list[dict] = None  # timestamped segments

    def __post_init__(self):
        if self.segments is None:
            self.segments = []


@dataclass
class VideoMetadata:
    duration_seconds: float
    width: int
    height: int
    fps: float
    has_audio: bool


@dataclass
class VideoTranscript:
    segments: list[dict]  # {start, end, text}
    summary: Optional[str] = None
    key_points: list[str] = None

    def __post_init__(self):
        if self.key_points is None:
            self.key_points = []


class ImageProcessor:
    """Image understanding, OCR, diagram interpretation."""

    async def analyze(self, image_path: str) -> ImageAnalysis:
        raise NotImplementedError

    async def ocr(self, image_path: str, language: str = "eng+ara") -> str:
        raise NotImplementedError


class AudioProcessor:
    """Speech-to-text and text-to-speech."""

    async def transcribe(self, audio_path: str, language: Optional[str] = None) -> AudioTranscription:
        raise NotImplementedError

    async def synthesize(self, text: str, language: str = "en") -> str:
        """Returns path to generated audio file."""
        raise NotImplementedError


class VideoProcessor:
    """Video metadata, transcription, summarization."""

    async def extract_metadata(self, video_path: str) -> VideoMetadata:
        raise NotImplementedError

    async def transcribe(self, video_path: str, language: Optional[str] = None) -> VideoTranscript:
        raise NotImplementedError

    async def summarize(self, transcript: VideoTranscript) -> str:
        raise NotImplementedError

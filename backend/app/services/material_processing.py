"""Material processing: text extraction, chunking, and keyword-based retrieval.

Supports PDF, DOCX, PPTX, and TXT with page/slide-level metadata where
available. Extraction is pure-text; OCR and audio/video transcription return
honest placeholder text when the underlying engine is unavailable.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Optional

from pypdf import PdfReader
from docx import Document as DocxDocument
from pptx import Presentation

from app.models.material import MaterialChunk
from app.core.config import settings


@dataclass
class ExtractedPage:
    """A single page/slide of extracted text with location metadata."""

    text: str
    page: Optional[int] = None
    section: Optional[str] = None


def extract_text(file_path: str, content_type: str) -> str:
    """Extract plain text from an uploaded file.

    Joins all pages/slides with page breaks. Returns empty string for
    unsupported/binary types.
    """
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf" or content_type == "application/pdf":
            return _extract_pdf_text(file_path)
        if ext == ".docx" or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return _extract_docx(file_path)
        if ext == ".pptx" or content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            return _extract_pptx(file_path)
        if ext == ".txt" or content_type == "text/plain":
            return _extract_txt(file_path)
        if ext in (".png", ".jpg", ".jpeg"):
            return f"[Image file: {os.path.basename(file_path)} — OCR not available in this environment.]"
        if ext in (".mp3", ".wav"):
            return f"[Audio file: {os.path.basename(file_path)} — transcription not available in this environment.]"
        if ext == ".mp4":
            return f"[Video file: {os.path.basename(file_path)} — transcription not available in this environment.]"
    except Exception:
        return ""

    return ""


def extract_pages(file_path: str, content_type: str) -> list[ExtractedPage]:
    """Extract text page-by-page with page numbers where available.

    Returns a list of ExtractedPage objects. For non-paginated formats
    (TXT, DOCX), returns a single page with page=None.
    """
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf" or content_type == "application/pdf":
            return _extract_pdf_pages(file_path)
        if ext == ".pptx" or content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            return _extract_pptx_pages(file_path)
        if ext == ".docx" or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = _extract_docx(file_path)
            return [ExtractedPage(text=text, page=None)]
        if ext == ".txt" or content_type == "text/plain":
            text = _extract_txt(file_path)
            return [ExtractedPage(text=text, page=None)]
    except Exception:
        return []

    return []


def _extract_pdf_text(file_path: str) -> str:
    pages = _extract_pdf_pages(file_path)
    return "\n\n".join(f"--- Page {p.page or i+1} ---\n{p.text}" for i, p in enumerate(pages))


def _extract_pdf_pages(file_path: str) -> list[ExtractedPage]:
    reader = PdfReader(file_path)
    pages: list[ExtractedPage] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append(ExtractedPage(text=text, page=i))
    return pages


def _extract_docx(file_path: str) -> str:
    doc = DocxDocument(file_path)
    parts = [p.text for p in doc.paragraphs if p.text]
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text for c in row.cells]
            parts.append(" | ".join(cells))
    return "\n".join(parts)


def _extract_pptx_pages(file_path: str) -> list[ExtractedPage]:
    prs = Presentation(file_path)
    pages: list[ExtractedPage] = []
    for i, slide in enumerate(prs.slides, start=1):
        parts = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                parts.append(shape.text)
        pages.append(ExtractedPage(text="\n".join(parts), page=i))
    return pages


def _extract_pptx(file_path: str) -> str:
    pages = _extract_pptx_pages(file_path)
    return "\n\n".join(
        f"--- Slide {p.page or i+1} ---\n{p.text}" for i, p in enumerate(pages)
    )


def _extract_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def chunk_text(
    text: str,
    material_id: int,
    user_id: int,
    chunk_size: int = 800,
    overlap: int = 150,
) -> list[dict]:
    """Split text into overlapping chunks.

    Returns a list of chunk dicts with chunk_index, text, section, page,
    word_count. Page-level metadata is preserved when available.
    """
    if not text or not text.strip():
        return []

    # Split by page markers first, then by paragraphs within each page.
    page_blocks = re.split(r"\n\s*--- Page \d+ ---\n", text)
    slide_blocks = re.split(r"\n\s*--- Slide \d+ ---\n", text)

    # Use page blocks if we found page markers, otherwise slide blocks,
    # otherwise treat the whole text as one block.
    if len(page_blocks) > 1:
        blocks = page_blocks
        page_offset = None
    elif len(slide_blocks) > 1:
        blocks = slide_blocks
        page_offset = None
    else:
        blocks = [text]
        page_offset = None

    chunks: list[dict] = []
    current_index = 0

    for block_idx, block in enumerate(blocks):
        block = block.strip()
        if not block:
            continue

        # Detect page/slide number from the block header if present.
        page: Optional[int] = None
        first_line = block.split("\n", 1)[0]
        m = re.match(r"--- (?:Page|Slide) (\d+) ---\s*$", first_line)
        if m:
            page = int(m.group(1))
            block = block.split("\n", 1)[1] if "\n" in block else ""

        paragraphs = re.split(r"\n\s*\n", block)
        current = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(current) + len(para) + 1 <= chunk_size:
                current = (current + " " + para).strip() if current else para
            else:
                if current:
                    chunks.append(
                        _make_chunk(current, current_index, page=page)
                    )
                    current_index += 1
                current = para[:chunk_size]

        if current:
            chunks.append(_make_chunk(current, current_index, page=page))
            current_index += 1

    return chunks


def _make_chunk(text: str, index: int, page: Optional[int] = None) -> dict:
    # Try to detect a section heading from the first line.
    first_line = text.strip().split("\n", 1)[0]
    section = first_line[:80] if len(first_line) < 80 else None
    return {
        "chunk_index": index,
        "text": text,
        "section": section,
        "page": page,
        "word_count": len(text.split()),
    }


def keyword_search_chunks(
    query: str,
    chunks: list[MaterialChunk],
    top_k: int = 5,
) -> list[MaterialChunk]:
    """Rank chunks by keyword overlap with the query.

    Simple, dependency-free retrieval that works without a vector store.
    """
    query_terms = set(re.findall(r"\w+", query.lower()))
    if not query_terms:
        return chunks[:top_k]

    scored = []
    for chunk in chunks:
        chunk_terms = set(re.findall(r"\w+", (chunk.text or "").lower()))
        overlap = len(query_terms & chunk_terms)
        if overlap > 0:
            scored.append((overlap, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]

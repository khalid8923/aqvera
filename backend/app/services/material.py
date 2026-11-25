"""Content processing service: upload validation, storage, extraction, chunking, indexing."""

from __future__ import annotations

import hashlib
import os
import shutil
import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.models.material import UploadedMaterial, ProcessingJob
from app.schemas.material import MaterialUploadResponse, MaterialRead, ProcessingJobRead, MaterialStatus
from app.core.config import settings

# Supported content types and extensions
SUPPORTED_EXTENSIONS = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".mp4": "video/mp4",
}

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB

UPLOAD_DIR = "data/uploads"


def ensure_upload_dir() -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    return UPLOAD_DIR


def compute_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def validate_file(filename: str, content_type: str, file_size: int) -> Optional[str]:
    """Return error message if invalid, None if valid."""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return f"Unsupported file type: {ext}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
    if file_size > MAX_FILE_SIZE_BYTES:
        return f"File too large: {file_size} bytes. Max: {MAX_FILE_SIZE_BYTES} bytes."
    return None


def store_file(file_content: bytes, original_filename: str) -> tuple[str, str]:
    """Store uploaded file to disk. Returns (stored_filename, storage_path)."""
    ensure_upload_dir()
    stored_filename = f"{uuid.uuid4().hex}_{original_filename}"
    storage_path = os.path.join(UPLOAD_DIR, stored_filename)
    with open(storage_path, "wb") as f:
        f.write(file_content)
    return stored_filename, storage_path


def create_material(
    db: Session,
    user_id: int,
    original_filename: str,
    content_type: str,
    file_size: int,
    file_path: str,
) -> UploadedMaterial:
    sha256 = compute_sha256(file_path)
    stored_filename = os.path.basename(file_path)
    material = UploadedMaterial(
        user_id=user_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        storage_path=file_path,
        content_type=content_type,
        file_size_bytes=file_size,
        sha256=sha256,
        status="uploaded",
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def create_processing_job(
    db: Session,
    material_id: int,
    job_type: str,
    idempotency_key: Optional[str] = None,
) -> ProcessingJob:
    # Idempotency: return existing pending/in-progress job if same key
    if idempotency_key:
        existing = (
            db.query(ProcessingJob)
            .filter(ProcessingJob.idempotency_key == idempotency_key)
            .first()
        )
        if existing:
            return existing
    job = ProcessingJob(
        material_id=material_id,
        job_type=job_type,
        status="pending",
        progress=0,
        idempotency_key=idempotency_key,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_material(db: Session, material_id: int, user_id: int) -> Optional[UploadedMaterial]:
    return (
        db.query(UploadedMaterial)
        .filter(UploadedMaterial.id == material_id, UploadedMaterial.user_id == user_id)
        .first()
    )


def list_materials(db: Session, user_id: int) -> list[UploadedMaterial]:
    return db.query(UploadedMaterial).filter(UploadedMaterial.user_id == user_id).all()


def get_job(db: Session, job_id: int) -> Optional[ProcessingJob]:
    return db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()


def list_jobs_for_material(db: Session, material_id: int) -> list[ProcessingJob]:
    return (
        db.query(ProcessingJob)
        .filter(ProcessingJob.material_id == material_id)
        .order_by(ProcessingJob.created_at.desc())
        .all()
    )

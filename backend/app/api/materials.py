"""Content processing API routes: material upload, processing status."""

from __future__ import annotations

import os
import shutil
import threading
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from app.core.deps import get_db_session, get_current_user
from app.models.course import User
from app.models.material import UploadedMaterial, ProcessingJob, MaterialChunk
from app.schemas.material import (
    MaterialUploadResponse,
    MaterialRead,
    ProcessingJobRead,
    MaterialStatus,
    MaterialChunkRead,
    MaterialChunkCreate,
    MaterialSearchRequest,
    MaterialSearchResult,
)
from app.services import material as material_service
from app.services import material_processing

router = APIRouter(prefix="/materials", tags=["materials"])

# Background processing thread registry: material_id -> Thread
_processing_threads: dict[int, threading.Thread] = {}


def _run_background_processing(
    material_id: int,
    user_id: int,
    storage_path: str,
    content_type: str,
) -> None:
    """Run material extraction and chunking in a background thread.

    Creates its own database session since the request session is closed
    after the API returns.
    """
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        material = material_service.get_material(db, material_id, user_id)
        if not material:
            return

        job = material_service.create_processing_job(
            db,
            material_id,
            "extraction",
            idempotency_key=f"mat-{material_id}-extraction-run",
        )
        job.status = "in_progress"
        job.started_at = datetime.now(timezone.utc)
        db.add(job)
        db.commit()

        try:
            text = material_processing.extract_text(storage_path, content_type)
            if not text.strip():
                material.status = "failed"
                material.failure_reason = "No text could be extracted from this file."
                db.add(material)
                job.status = "failed"
                job.failure_reason = "No text extracted"
                job.completed_at = datetime.now(timezone.utc)
                db.add(job)
                db.commit()
                return

            chunks = material_processing.chunk_text(
                text, material.id, user_id
            )

            # Delete any existing chunks for this material (re-processing).
            db.query(MaterialChunk).filter(MaterialChunk.material_id == material.id).delete()

            for chunk_data in chunks:
                chunk = MaterialChunk(
                    material_id=material.id,
                    user_id=user_id,
                    chunk_index=chunk_data["chunk_index"],
                    text=chunk_data["text"],
                    section=chunk_data.get("section"),
                    page=chunk_data.get("page"),
                    word_count=chunk_data["word_count"],
                )
                db.add(chunk)

            material.status = "completed"
            job.status = "completed"
            job.progress = 100
            job.completed_at = datetime.now(timezone.utc)
            db.add(material)
            db.add(job)
            db.commit()
        except Exception as exc:  # noqa: BLE001
            material.status = "failed"
            material.failure_reason = str(exc)
            job.status = "failed"
            job.failure_reason = str(exc)
            job.completed_at = datetime.now(timezone.utc)
            db.add(material)
            db.add(job)
            db.commit()
    finally:
        db.close()
        _processing_threads.pop(material_id, None)


@router.post("/upload", response_model=MaterialUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_material(
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Upload an academic material file.

    Validates file type/size, stores securely, computes SHA-256, creates
    a processing job. Processing runs asynchronously (status = uploaded).
    """
    content_type = file.content_type or "application/octet-stream"
    contents = await file.read()
    file_size = len(contents)

    error = material_service.validate_file(file.filename or "unknown", content_type, file_size)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Check for duplicate by sha256
    temp_path = os.path.join(material_service.UPLOAD_DIR, f"tmp_{current_user.id}_{file.filename}")
    os.makedirs(material_service.UPLOAD_DIR, exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(contents)
    sha256 = material_service.compute_sha256(temp_path)

    existing = (
        db.query(UploadedMaterial)
        .filter(UploadedMaterial.user_id == current_user.id, UploadedMaterial.sha256 == sha256)
        .first()
    )
    if existing:
        os.remove(temp_path)
        return MaterialUploadResponse(
            id=existing.id,
            original_filename=existing.original_filename,
            content_type=existing.content_type,
            file_size_bytes=existing.file_size_bytes,
            status=existing.status,
            created_at=existing.created_at,
        )

    # Store permanently
    stored_filename, storage_path = material_service.store_file(contents, file.filename or "unknown")
    os.remove(temp_path)

    material = material_service.create_material(
        db,
        current_user.id,
        file.filename or "unknown",
        content_type,
        file_size,
        storage_path,
    )

    # Create extraction processing job
    job = material_service.create_processing_job(
        db, material.id, "extraction", idempotency_key=f"mat-{material.id}-extraction"
    )

    return MaterialUploadResponse(
        id=material.id,
        original_filename=material.original_filename,
        content_type=material.content_type,
        file_size_bytes=material.file_size_bytes,
        status=material.status,
        created_at=material.created_at,
    )


@router.get("", response_model=List[MaterialRead])
def list_materials(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    materials = material_service.list_materials(db, current_user.id)
    return materials


@router.get("/{material_id}", response_model=MaterialRead)
def get_material(
    material_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    material = material_service.get_material(db, material_id, current_user.id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@router.get("/{material_id}/status", response_model=MaterialStatus)
def get_material_status(
    material_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    material = material_service.get_material(db, material_id, current_user.id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    jobs = material_service.list_jobs_for_material(db, material_id)
    progress = 0
    if jobs:
        progress = sum(j.progress for j in jobs) // len(jobs)
    return MaterialStatus(
        material_id=material.id,
        status=material.status,
        progress=progress,
        failure_reason=material.failure_reason,
        jobs=jobs,
    )


@router.get("/{material_id}/jobs", response_model=List[ProcessingJobRead])
def list_jobs(
    material_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    material = material_service.get_material(db, material_id, current_user.id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material_service.list_jobs_for_material(db, material_id)


@router.post("/{material_id}/process", response_model=MaterialUploadResponse, status_code=status.HTTP_200_OK)
def process_material(
    material_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Extract text from an uploaded material and create searchable chunks.

    Processing runs in a background thread. The API returns immediately with
    the current material status; clients poll /materials/{id}/status for
    progress updates.
    """
    material = material_service.get_material(db, material_id, current_user.id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")

    # Avoid starting duplicate processing for the same material.
    if material_id in _processing_threads:
        existing = _processing_threads[material_id]
        if existing.is_alive():
            return MaterialUploadResponse(
                id=material.id,
                original_filename=material.original_filename,
                content_type=material.content_type,
                file_size_bytes=material.file_size_bytes,
                status=material.status,
                created_at=material.created_at,
            )

    # Start background processing.
    thread = threading.Thread(
        target=_run_background_processing,
        args=(material_id, current_user.id, material.storage_path, material.content_type),
        daemon=True,
    )
    _processing_threads[material_id] = thread
    thread.start()

    return MaterialUploadResponse(
        id=material.id,
        original_filename=material.original_filename,
        content_type=material.content_type,
        file_size_bytes=material.file_size_bytes,
        status=material.status,
        created_at=material.created_at,
    )


@router.get("/{material_id}/chunks", response_model=List[MaterialChunkRead])
def list_chunks(
    material_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    material = material_service.get_material(db, material_id, current_user.id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    chunks = (
        db.query(MaterialChunk)
        .filter(MaterialChunk.material_id == material_id)
        .order_by(MaterialChunk.chunk_index)
        .all()
    )
    return chunks


@router.post("/search", response_model=List[MaterialSearchResult])
def search_materials(
    search: MaterialSearchRequest,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Keyword search across the current user's material chunks."""
    query = search.query.strip()
    if not query:
        return []

    materials = material_service.list_materials(db, current_user.id)
    results: list[MaterialSearchResult] = []

    for material in materials:
        chunks = (
            db.query(MaterialChunk)
            .filter(MaterialChunk.material_id == material.id)
            .all()
        )
        matched = material_processing.keyword_search_chunks(query, chunks, top_k=search.top_k or 5)
        if matched:
            results.append(
                MaterialSearchResult(
                    material_id=material.id,
                    material_title=material.original_filename,
                    chunks=[MaterialChunkRead.model_validate(c) for c in matched],
                )
            )

    results.sort(
        key=lambda r: sum(len(c.text) for c in r.chunks),
        reverse=True,
    )
    return results[: search.limit or 10]

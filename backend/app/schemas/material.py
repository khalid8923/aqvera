"""Content processing schemas."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MaterialUploadResponse(BaseModel):
    id: int
    original_filename: str
    content_type: str
    file_size_bytes: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialRead(BaseModel):
    id: int
    user_id: int
    original_filename: str
    stored_filename: str
    content_type: str
    file_size_bytes: int
    sha256: str
    status: str
    failure_reason: Optional[str] = None
    primary_language: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProcessingJobRead(BaseModel):
    id: int
    material_id: int
    job_type: str
    status: str
    progress: int
    failure_reason: Optional[str] = None
    retry_count: int
    max_retries: int
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialStatus(BaseModel):
    material_id: int
    status: str
    progress: int
    failure_reason: Optional[str] = None
    jobs: list[ProcessingJobRead] = []

    class Config:
        from_attributes = True


class MaterialChunkRead(BaseModel):
    id: int
    material_id: int
    user_id: int
    chunk_index: int
    text: str
    section: Optional[str] = None
    page: Optional[int] = None
    word_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class MaterialChunkCreate(BaseModel):
    material_id: int
    chunk_index: int
    text: str
    section: Optional[str] = None
    page: Optional[int] = None
    word_count: Optional[int] = None


class MaterialSearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    limit: Optional[int] = 10


class MaterialSearchResult(BaseModel):
    material_id: int
    material_title: str
    chunks: List[MaterialChunkRead] = []

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str

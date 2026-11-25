"""Retrieval layer: embeddings abstraction, vector/keyword retrieval, reranking.

Provides the interface between the RAG pipeline and the underlying vector store.
The concrete vector-store implementation lives in the backend content-processing
domain (pgvector) or here when a local embedding model is available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ai import TaskType


@dataclass
class Embedding:
    vector: list[float]
    model: str
    dimensions: int


@dataclass
class RetrievalChunk:
    id: str
    text: str
    document_id: str
    document_title: str
    section: Optional[str] = None
    page: Optional[int] = None
    slide: Optional[int] = None
    score: float = 0.0


class EmbeddingModel:
    """Abstraction over embedding models. Concrete providers implement encode()."""

    async def encode(self, text: str) -> Embedding:
        raise NotImplementedError

    async def encode_batch(self, texts: list[str]) -> list[Embedding]:
        return [await self.encode(t) for t in texts]


class VectorStore:
    """Abstraction over a vector store (pgvector, local index, etc.)."""

    async def add(self, chunks: list[RetrievalChunk], embeddings: list[Embedding]) -> None:
        raise NotImplementedError

    async def search(
        self,
        query_embedding: list[float],
        course_id: Optional[str] = None,
        top_k: int = 5,
    ) -> list[RetrievalChunk]:
        raise NotImplementedError

    async def keyword_search(
        self,
        query: str,
        course_id: Optional[str] = None,
        top_k: int = 5,
    ) -> list[RetrievalChunk]:
        raise NotImplementedError


class Reranker:
    """Optional reranking abstraction. Returns re-ranked chunks."""

    async def rerank(
        self,
        query: str,
        chunks: list[RetrievalChunk],
        top_k: int = 5,
    ) -> list[RetrievalChunk]:
        return chunks[:top_k]


class RetrievalService:
    """Combines embedding + vector + keyword + rerank into retrieval."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        reranker: Reranker | None = None,
    ) -> None:
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.reranker = reranker

    async def retrieve(
        self,
        query: str,
        course_id: Optional[str] = None,
        top_k: int = 5,
    ) -> list[RetrievalChunk]:
        embedding = await self.embedding_model.encode(query)
        chunks = await self.vector_store.search(
            embedding.vector, course_id=course_id, top_k=top_k
        )
        # Hybrid: also try keyword search and merge.
        keyword_chunks = await self.vector_store.keyword_search(
            query, course_id=course_id, top_k=top_k
        )
        merged = self._merge(chunks, keyword_chunks)
        if self.reranker:
            merged = await self.reranker.rerank(query, merged, top_k=top_k)
        return merged[:top_k]

    @staticmethod
    def _merge(
        vector_chunks: list[RetrievalChunk],
        keyword_chunks: list[RetrievalChunk],
    ) -> list[RetrievalChunk]:
        seen: dict[str, RetrievalChunk] = {}
        for c in vector_chunks + keyword_chunks:
            if c.id not in seen:
                seen[c.id] = c
        return list(seen.values())

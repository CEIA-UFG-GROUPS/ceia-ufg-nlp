from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from sentence_transformers import SentenceTransformer

APP_NAME = "rag-demo"

DATA_PATH = os.getenv("DOCS_PATH", "app/data/basketball.txt")
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "basketball_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

app = FastAPI(title=APP_NAME)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(3, ge=1, le=10)


class QueryResponse(BaseModel):
    answer: str
    context: List[str]


@dataclass
class RagResources:
    client: QdrantClient
    model: SentenceTransformer
    collection: str


RESOURCES: RagResources | None = None


def _load_docs(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [line for line in lines if line]


def _embed_texts(model: SentenceTransformer, texts: List[str]) -> List[List[float]]:
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]


def _ensure_collection(client: QdrantClient, collection: str, vector_size: int) -> None:
    exists = client.collection_exists(collection)
    if exists:
        return
    client.create_collection(
        collection_name=collection,
        vectors_config=qdrant_models.VectorParams(
            size=vector_size, distance=qdrant_models.Distance.COSINE
        ),
    )


def _upsert_docs(
    client: QdrantClient, collection: str, docs: List[str], vectors: List[List[float]]
) -> None:
    points = []
    for idx, (doc, vector) in enumerate(zip(docs, vectors)):
        payload = {"text": doc, "source": "basketball.txt"}
        points.append(qdrant_models.PointStruct(id=idx, vector=vector, payload=payload))
    client.upsert(collection_name=collection, points=points)


def _simple_generator(question: str, contexts: List[str]) -> str:
    if not contexts:
        return "Nao encontrei informacoes relevantes na base."
    joined = " ".join(contexts)
    return f"Com base nos textos, a resposta e: {joined}"


@app.on_event("startup")
def startup() -> None:
    global RESOURCES

    model = SentenceTransformer(EMBEDDING_MODEL)
    docs = _load_docs(DATA_PATH)
    vectors = _embed_texts(model, docs)

    client = QdrantClient(url=QDRANT_URL)
    _ensure_collection(client, QDRANT_COLLECTION, vector_size=len(vectors[0]))
    _upsert_docs(client, QDRANT_COLLECTION, docs, vectors)

    RESOURCES = RagResources(client=client, model=model, collection=QDRANT_COLLECTION)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest) -> QueryResponse:
    if RESOURCES is None:
        return QueryResponse(answer="Servidor nao inicializado.", context=[])

    query_vector = _embed_texts(RESOURCES.model, [payload.question])[0]
    search_result = RESOURCES.client.search(
        collection_name=RESOURCES.collection,
        query_vector=query_vector,
        limit=payload.top_k,
        with_payload=True,
    )

    contexts = [
        point.payload.get("text", "") for point in search_result if point.payload
    ]
    answer = _simple_generator(payload.question, contexts)
    return QueryResponse(answer=answer, context=contexts)

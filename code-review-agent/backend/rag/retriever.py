"""
RAG Retrieval Layer — searches all knowledge bases for relevant context.
Fixes: empty collection guard, telemetry suppression, local embeddings.
"""
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dataclasses import dataclass
from typing import Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

@dataclass
class RetrievedChunk:
    source: str
    collection: str
    content: str
    distance: float

class RAGRetriever:
    COLLECTIONS = {
        "cwe_database": "CWE/CVE Database",
        "owasp_rules": "OWASP Security Rules",
        "fix_examples": "Fix Examples",
        "team_standards": "Team Coding Standards",
        "past_reviews": "Past Review History",
    }

    def __init__(self, vector_store_path: str = "vector_store"):
        self.embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=vector_store_path)
        self.collections: dict = {}
        self._load_collections()

    def _load_collections(self):
        try:
            existing = {c.name for c in self.client.list_collections()}
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            return

        for name in self.COLLECTIONS:
            if name not in existing:
                logger.warning(f"Collection '{name}' not found — run ingest script first.")
                continue
            try:
                coll = self.client.get_collection(name=name, embedding_function=self.embedding_fn)
                count = coll.count()
                if count == 0:
                    logger.warning(f"Collection '{name}' has 0 documents — skipping.")
                    continue
                self.collections[name] = coll
                logger.info(f"Loaded '{name}' ({count} chunks).")
            except Exception as e:
                logger.error(f"Failed to load '{name}': {e}")

        logger.info(f"RAGRetriever ready — {len(self.collections)} collection(s) loaded.")

    def retrieve(self, query: str, top_k: int = 4,
                 collections: Optional[list[str]] = None) -> list[RetrievedChunk]:
        if not query or not query.strip():
            return []

        results = []
        for name in (collections or list(self.collections.keys())):
            coll = self.collections.get(name)
            if not coll:
                continue
            try:
                count = coll.count()
                if count == 0:
                    continue
                n = min(top_k, count)   # Never request more than available
                res = coll.query(query_texts=[query], n_results=n)
                for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
                    results.append(RetrievedChunk(
                        source=meta.get("kb", name),
                        collection=name, content=doc, distance=dist
                    ))
            except Exception as e:
                logger.error(f"RAG query failed for '{name}': {e}")

        results.sort(key=lambda x: x.distance)
        logger.info(f"RAG retrieved {len(results)} chunks.")
        return results

    def format_context_for_prompt(self, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "No additional context retrieved from knowledge bases."
        lines = ["=== RETRIEVED KNOWLEDGE BASE CONTEXT ==="]
        for i, c in enumerate(chunks, 1):
            lines.append(f"\n[{i}] Source: {c.source.upper()}")
            lines.append(c.content.strip())
        lines.append("\n=== END OF CONTEXT ===")
        return "\n".join(lines)

    def health_check(self) -> dict:
        status = {}
        for name, coll in self.collections.items():
            try:
                status[name] = {"count": coll.count(), "status": "ok"}
            except Exception as e:
                status[name] = {"count": 0, "status": f"error: {e}"}
        for name in self.COLLECTIONS:
            if name not in self.collections:
                status[name] = {"count": 0, "status": "not ingested"}
        return status
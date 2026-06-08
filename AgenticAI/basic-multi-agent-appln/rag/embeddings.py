"""
rag/embeddings.py — Sentence Transformer Embedding Wrapper

Wraps the `sentence-transformers` library in a LangChain-compatible
Embeddings class so it plugs directly into ChromaDB.

Why local embeddings?
  - No API cost (runs on your CPU/GPU)
  - No latency from network calls
  - `all-MiniLM-L6-v2` is small (80 MB) yet accurate for Q&A tasks

The model is downloaded once on first use and cached by
sentence-transformers in ~/.cache/torch/sentence_transformers/
"""

from typing import List

from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class SentenceTransformerEmbeddings(Embeddings):
    """
    LangChain-compatible wrapper around SentenceTransformer.

    Usage
    -----
    embedder = SentenceTransformerEmbeddings()
    vector   = embedder.embed_query("What is LangGraph?")
    vectors  = embedder.embed_documents(["doc1 text", "doc2 text"])
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        print(f"  🔄 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"  ✅ Embedding model ready.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of document strings.
        Called by ChromaDB when ingesting chunks.
        """
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.
        Called by ChromaDB at retrieval time.
        """
        embedding = self.model.encode([text], show_progress_bar=False)
        return embedding[0].tolist()


# Singleton — reuse one model instance across the app
_embedder: SentenceTransformerEmbeddings | None = None


def get_embedder() -> SentenceTransformerEmbeddings:
    """Return (or create) the shared embedder instance."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformerEmbeddings()
    return _embedder

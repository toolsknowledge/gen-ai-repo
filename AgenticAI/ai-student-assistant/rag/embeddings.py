"""
rag/embeddings.py
─────────────────
Creates the embedding model used throughout the RAG pipeline.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS AN EMBEDDING?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
An embedding converts text into a list of numbers (a vector).
Similar texts produce similar vectors.

Example:
  "What is photosynthesis?"  →  [0.12, -0.87, 0.44, ...]
  "Explain photosynthesis"   →  [0.13, -0.85, 0.46, ...]   ← very similar
  "What is quantum physics?" →  [-0.55, 0.32, -0.11, ...]  ← very different

ChromaDB stores these vectors.  When you ask a question, we embed the
question and find the stored vectors closest to it – those chunks are the
most relevant passages.

WHY sentence-transformers INSTEAD OF the Anthropic embedding API?
──────────────────────────────────────────────────────────────────
• Free – no API cost for embedding thousands of chunks.
• Offline – works without internet after the first model download.
• Fast – runs on CPU, good enough for student-scale document sets.
• "all-MiniLM-L6-v2" produces 384-dimensional vectors and is the community
  standard for RAG demos.

For production you'd likely switch to a larger model (e.g. text-embedding-3-large
from OpenAI) for higher accuracy, but the code stays the same.
"""

from functools import lru_cache
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings
from utils.logger import get_logger

log = get_logger(__name__)


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Return a cached HuggingFaceEmbeddings instance.

    @lru_cache means the model is loaded from disk only once per process,
    even if get_embeddings() is called many times.
    """
    log.info("Loading embedding model: %s", settings.embedding_model)
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},   # cosine similarity
    )

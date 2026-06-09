"""
config.py
─────────
Central configuration object.

WHY THIS FILE EXISTS
────────────────────
Instead of scattering os.getenv() calls across the codebase, we load all
settings once here using pydantic-settings.  Every module imports `settings`
and uses settings.anthropic_api_key, settings.chroma_persist_dir, etc.

Benefits:
  • Type-safe – pydantic validates types at startup (e.g. int fields won't
    accidentally hold a string "10").
  • Single source of truth – change .env → all modules see the new value.
  • Easy to test – swap settings in tests without monkeypatching os.environ.

HOW IT WORKS
────────────
pydantic-settings reads from environment variables first, then from the .env
file.  Field names map to env-var names (case-insensitive by default).
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ── LLM ──────────────────────────────────────────────────────────────────
    anthropic_api_key: str = ""
    claude_smart_model: str = "claude-sonnet-4-6"
    claude_fast_model: str = "claude-haiku-4-5-20251001"

    # ── Embeddings ────────────────────────────────────────────────────────────
    # "all-MiniLM-L6-v2" is a small, fast sentence-transformer model that runs
    # entirely locally – no API key or internet connection required after the
    # first download (≈ 90 MB, cached in ~/.cache/huggingface).
    embedding_model: str = "all-MiniLM-L6-v2"

    # ── ChromaDB ─────────────────────────────────────────────────────────────
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "student_docs"

    # ── RAG tuning ────────────────────────────────────────────────────────────
    rag_chunk_size: int = 500       # characters per chunk
    rag_chunk_overlap: int = 50     # overlap between adjacent chunks
    rag_top_k: int = 4              # number of chunks to retrieve per query

    # ── LangGraph ────────────────────────────────────────────────────────────
    max_iterations: int = 10        # prevents infinite supervisor loops
    debug_mode: bool = True         # verbose state printing

    # ── Paths ─────────────────────────────────────────────────────────────────
    pdf_upload_dir: str = "./data/pdfs"

    # ── pydantic-settings config ──────────────────────────────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",          # load from .env in the working directory
        env_file_encoding="utf-8",
        case_sensitive=False,     # ANTHROPIC_API_KEY == anthropic_api_key
        extra="ignore",           # ignore unknown env vars
    )

    # ── Derived helpers ───────────────────────────────────────────────────────
    @property
    def chroma_path(self) -> Path:
        """Resolved absolute path to the ChromaDB directory."""
        return Path(self.chroma_persist_dir).resolve()

    @property
    def pdf_dir(self) -> Path:
        """Resolved absolute path to the PDF upload directory."""
        p = Path(self.pdf_upload_dir).resolve()
        p.mkdir(parents=True, exist_ok=True)   # auto-create if missing
        return p


# ─── Singleton ────────────────────────────────────────────────────────────────
# Import `settings` anywhere in the project:
#   from config import settings
settings = Settings()

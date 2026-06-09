"""
rag/document_store.py
─────────────────────
Handles all ChromaDB operations: create, persist, and search the vector store.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS ChromaDB?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ChromaDB is an open-source vector database.  Think of it as a special kind
of database that stores text PLUS its numeric vector representation, and
supports "find the most similar items to this query" searches.

Traditional DB: SELECT * FROM docs WHERE topic = 'biology'
ChromaDB:       find the 4 chunks most SEMANTICALLY similar to "explain DNA"

HOW DATA FLOWS THROUGH THIS FILE
─────────────────────────────────
1. PDF Ingest:  add_documents(chunks)
   • Each chunk gets embedded → vector stored in chroma_db/ on disk.

2. RAG Agent:   get_retriever() → retriever.get_relevant_documents(query)
   • Query is embedded → cosine similarity search → top-k chunks returned.

PERSISTENCE
───────────
Chroma writes to ./data/chroma_db (set in .env).  The data survives process
restarts – you only need to ingest each PDF once.
"""

from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from config import settings
from rag.embeddings import get_embeddings
from utils.logger import get_logger

log = get_logger(__name__)


class DocumentStore:
    """
    Thin wrapper around LangChain's Chroma integration.

    Responsibilities:
      • Open (or create) a persistent ChromaDB collection.
      • Add new documents (from PDF ingest).
      • Expose a retriever for the RAG Agent to use.
    """

    def __init__(self) -> None:
        persist_dir = str(settings.chroma_path)

        # Ensure the directory exists
        Path(persist_dir).mkdir(parents=True, exist_ok=True)

        log.info(
            "Opening ChromaDB at %s  collection=%s",
            persist_dir,
            settings.chroma_collection_name,
        )

        # Chroma() opens an existing collection or creates a new empty one.
        self._store = Chroma(
            collection_name=settings.chroma_collection_name,
            embedding_function=get_embeddings(),
            persist_directory=persist_dir,
        )

    # ── Ingest ────────────────────────────────────────────────────────────────

    def add_documents(self, documents: List[Document]) -> int:
        """
        Embed and persist a list of LangChain Document objects.

        Returns the number of documents added.

        Each Document has:
          .page_content : the raw text chunk
          .metadata     : dict with keys like 'source', 'page', 'chunk_index'
        """
        if not documents:
            log.warning("add_documents called with empty list – nothing to do")
            return 0

        log.info("Adding %d chunks to ChromaDB…", len(documents))
        self._store.add_documents(documents)
        log.info("✓ Added %d chunks", len(documents))
        return len(documents)

    # ── Retrieval ─────────────────────────────────────────────────────────────

    def get_retriever(self, k: int | None = None) -> VectorStoreRetriever:
        """
        Return a LangChain retriever.

        The retriever's .get_relevant_documents(query) method:
          1. Embeds the query.
          2. Runs a cosine similarity search against ChromaDB.
          3. Returns the top-k Document objects.

        k defaults to settings.rag_top_k (set in .env).
        """
        top_k = k or settings.rag_top_k
        return self._store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": top_k},
        )

    def collection_size(self) -> int:
        """Return the total number of chunks currently stored."""
        return self._store._collection.count()


# ── Singleton ─────────────────────────────────────────────────────────────────
# Instantiate once so we don't reopen the DB file on every agent call.
# Any module can do: from rag.document_store import document_store
document_store = DocumentStore()

"""
rag/vectorstore.py — ChromaDB Vector Store

Handles:
  1. Ingesting chunked documents (build_vectorstore)
  2. Persisting them to disk so re-indexing isn't needed every run
  3. Retrieving the top-K most relevant chunks for a query (retrieve)

How ChromaDB works (beginner note):
  - Each chunk is converted to a float vector (embedding)
  - Vectors are stored in a local SQLite+FAISS-backed database
  - At query time, your question is also embedded, and ChromaDB
    returns the chunks whose vectors are geometrically closest
    (cosine similarity)
"""

from pathlib import Path
from typing import List

import chromadb
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from config import CHROMA_DIR, CHROMA_COLLECTION, TOP_K_RESULTS
from rag.embeddings import get_embedder


def _get_chroma_client() -> chromadb.PersistentClient:
    """
    Create a ChromaDB PersistentClient using the new 0.5.x API.

    ChromaDB 0.5.x replaced the Settings-based init with PersistentClient,
    which automatically creates the default tenant and database on first use.
    This avoids the 'Could not connect to tenant default_tenant' error.
    """
    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def build_vectorstore(chunks: List[Document]) -> Chroma:
    """
    Embed `chunks` and persist them in ChromaDB.

    Parameters
    ----------
    chunks : List[Document]
        Output of chunker.chunk_documents().

    Returns
    -------
    Chroma
        A LangChain Chroma object ready for similarity_search().
    """
    embedder = get_embedder()
    client = _get_chroma_client()

    print(f"  💾 Building ChromaDB collection '{CHROMA_COLLECTION}' "
          f"with {len(chunks)} chunks …")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        collection_name=CHROMA_COLLECTION,
        client=client,                  # pass PersistentClient directly
    )

    print(f"  ✅ Vectorstore built and persisted to: {CHROMA_DIR}")
    return vectorstore


def load_vectorstore() -> Chroma:
    """
    Load an existing ChromaDB collection from disk.

    Raises
    ------
    FileNotFoundError
        If the chroma_db directory doesn't exist yet.
    """
    if not Path(CHROMA_DIR).exists():
        raise FileNotFoundError(
            f"ChromaDB directory not found: {CHROMA_DIR}\n"
            "Run the ingestion step first (build_vectorstore)."
        )

    embedder = get_embedder()
    client = _get_chroma_client()

    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION,
        embedding_function=embedder,
        client=client,                  # pass PersistentClient directly
    )

    print(f"  ✅ Loaded existing vectorstore from: {CHROMA_DIR}")
    return vectorstore


def retrieve(query: str, vectorstore: Chroma) -> List[Document]:
    """
    Find the TOP_K_RESULTS chunks most relevant to `query`.

    Parameters
    ----------
    query       : str    — the user's question
    vectorstore : Chroma — the loaded/built ChromaDB instance

    Returns
    -------
    List[Document]
        Ranked list of the most relevant chunks with metadata.
    """
    results = vectorstore.similarity_search(query, k=TOP_K_RESULTS)
    print(f"  🔍 Retrieved {len(results)} chunks for query: '{query[:60]}…'")
    return results


def get_or_build_vectorstore(chunks: List[Document] | None = None) -> Chroma:
    """
    Convenience helper:
      - If chroma_db/ exists  → load from disk (fast)
      - Otherwise             → build from `chunks` (requires chunks)

    Parameters
    ----------
    chunks : optional list of Documents needed only on first build.
    """
    if Path(CHROMA_DIR).exists():
        return load_vectorstore()

    if chunks is None:
        raise ValueError(
            "No existing vectorstore found and no chunks provided. "
            "Pass chunks= to build a new one."
        )
    return build_vectorstore(chunks)

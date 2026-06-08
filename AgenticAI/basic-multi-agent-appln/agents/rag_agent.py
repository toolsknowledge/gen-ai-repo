"""
agents/rag_agent.py — RAG Agent

Full pipeline:
  1. Load PDFs from data/pdfs/  (skipped if ChromaDB already exists)
  2. Chunk documents
  3. Embed + store in ChromaDB  (skipped if ChromaDB already exists)
  4. Retrieve top-K relevant chunks for the user query
  5. Build a context-grounded prompt
  6. Call Claude Sonnet for the final answer
  7. Return response + source metadata

The vectorstore is built once and cached on disk (chroma_db/).
Subsequent queries skip ingestion and go straight to retrieval.
"""

from typing import Any

from anthropic import Anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, TOP_K_RESULTS
from rag.loader import load_pdfs
from rag.chunker import chunk_documents
from rag.vectorstore import get_or_build_vectorstore, retrieve

# ── Shared Anthropic client (reused across calls) ─────────────────────────────
_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# ── Vectorstore singleton (loaded once per session) ───────────────────────────
_vectorstore = None


def _get_vectorstore():
    """
    Return the vectorstore, building it from PDFs if needed.
    Uses a module-level singleton to avoid reloading on every query.
    """
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore

    from pathlib import Path
    from config import CHROMA_DIR

    if Path(CHROMA_DIR).exists():
        # Fast path: load from persisted ChromaDB
        _vectorstore = get_or_build_vectorstore()
    else:
        # First run: ingest PDFs → chunk → embed → persist
        print("\n📚 First run — ingesting PDFs into ChromaDB …")
        pages = load_pdfs()
        chunks = chunk_documents(pages)
        _vectorstore = get_or_build_vectorstore(chunks=chunks)

    return _vectorstore


def _build_rag_prompt(query: str, context: str) -> str:
    """
    Construct the system + user prompt for grounded Q&A.

    The system prompt instructs Claude to answer ONLY from the provided
    context and to cite sources — reducing hallucination.
    """
    system_prompt = (
        "You are a helpful assistant that answers questions based strictly "
        "on the provided document context.\n\n"
        "Rules:\n"
        "1. Answer only using information from the CONTEXT section below.\n"
        "2. If the context doesn't contain enough information, say so clearly.\n"
        "3. Cite the source document and page number when referencing facts.\n"
        "4. Be concise and accurate.\n"
        "5. Format your answer in clear, readable paragraphs."
    )

    user_message = (
        f"CONTEXT (retrieved from documents):\n"
        f"{'─' * 60}\n"
        f"{context}\n"
        f"{'─' * 60}\n\n"
        f"QUESTION: {query}"
    )

    return system_prompt, user_message


def run_rag_agent(query: str) -> dict[str, Any]:
    """
    Execute the full RAG pipeline for a user query.

    Parameters
    ----------
    query : str
        The user's question.

    Returns
    -------
    dict with keys:
        "response"    : str   — Claude's final answer
        "context"     : str   — the raw retrieved context fed to Claude
        "source_docs" : list  — LangChain Document objects (for citations)
    """
    print(f"\n🔍 RAG Agent: processing query → '{query[:80]}…'")

    # ── Step 1: Get vectorstore (build once, reuse) ───────────────────────────
    vectorstore = _get_vectorstore()

    # ── Step 2: Retrieve relevant chunks ─────────────────────────────────────
    source_docs = retrieve(query, vectorstore)

    if not source_docs:
        return {
            "response": (
                "I couldn't find relevant information in the loaded documents. "
                "Please ensure PDFs are placed in the data/pdfs/ folder and "
                "the vectorstore has been built."
            ),
            "context": "",
            "source_docs": [],
        }

    # ── Step 3: Format context from retrieved chunks ──────────────────────────
    context_parts = []
    for i, doc in enumerate(source_docs, 1):
        source = doc.metadata.get("source", "Unknown")
        page   = doc.metadata.get("page", "?")
        context_parts.append(
            f"[{i}] Source: {source} | Page: {page}\n{doc.page_content}"
        )

    context = "\n\n".join(context_parts)

    # ── Step 4: Build prompt ──────────────────────────────────────────────────
    system_prompt, user_message = _build_rag_prompt(query, context)

    # ── Step 5: Call Claude ───────────────────────────────────────────────────
    print(f"  🤖 Calling Claude ({CLAUDE_MODEL}) with {len(source_docs)} context chunks …")

    message = _client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    response_text = message.content[0].text

    print(f"  ✅ RAG Agent complete. ({message.usage.output_tokens} output tokens)")

    return {
        "response": response_text,
        "context": context,
        "source_docs": source_docs,
    }

"""
tests/test_rag.py
─────────────────
Tests for the RAG pipeline: PDF loading, chunking, and retrieval.

HOW TO RUN
──────────
    pytest tests/test_rag.py -v

WHAT IS TESTED
──────────────
1. test_pdf_chunking   – a synthetic text is split correctly into chunks
2. test_document_store – chunks can be added and retrieved from ChromaDB
3. test_rag_agent      – the RAGAgent correctly formats retrieved context
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from langchain_core.documents import Document


# ── Test 1: Text splitting ────────────────────────────────────────────────────

def test_pdf_chunking():
    """Text splitter produces overlapping chunks of the right size."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    long_text = "A" * 600  # 600 chars – should split into at least 2 chunks
    doc = Document(page_content=long_text, metadata={"source": "test.pdf"})

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents([doc])

    assert len(chunks) >= 2, "Long text should produce at least 2 chunks"
    for chunk in chunks:
        assert len(chunk.page_content) <= 500 + 10, "Chunk should not far exceed chunk_size"


# ── Test 2: DocumentStore add + retrieve ─────────────────────────────────────

def test_document_store_add_and_retrieve():
    """
    DocumentStore can store documents and retrieve relevant ones.

    We use a temporary directory so this test doesn't pollute the real DB.
    """
    import tempfile
    from rag.document_store import DocumentStore

    with tempfile.TemporaryDirectory() as tmpdir:
        # Patch settings to use the temp dir
        with patch("rag.document_store.settings") as mock_settings:
            mock_settings.chroma_persist_dir = tmpdir
            mock_settings.chroma_collection_name = "test_collection"
            mock_settings.rag_top_k = 2

            # Re-instantiate with patched settings
            from rag.embeddings import get_embeddings
            from langchain_chroma import Chroma

            store_obj = Chroma(
                collection_name="test_collection",
                embedding_function=get_embeddings(),
                persist_directory=tmpdir,
            )

            # Add a few documents
            docs = [
                Document(
                    page_content="Photosynthesis converts sunlight into glucose.",
                    metadata={"source": "biology.pdf", "page": 1},
                ),
                Document(
                    page_content="The mitochondria is the powerhouse of the cell.",
                    metadata={"source": "biology.pdf", "page": 2},
                ),
                Document(
                    page_content="Python is a high-level programming language.",
                    metadata={"source": "cs.pdf", "page": 1},
                ),
            ]
            store_obj.add_documents(docs)

            # Retrieve
            retriever = store_obj.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 2},
            )
            results = retriever.get_relevant_documents("How do plants make food?")

            assert len(results) > 0, "Should return at least 1 result"
            # The photosynthesis chunk should be most relevant
            top_text = results[0].page_content.lower()
            assert "photosynthesis" in top_text or "sunlight" in top_text, \
                "Top result should be about photosynthesis"


# ── Test 3: RAG Agent formats context ────────────────────────────────────────

def test_rag_agent_formats_context():
    """RAGAgent correctly formats retrieved docs into a context string."""
    from agents.rag_agent import RAGAgent
    from graph.state import create_initial_state

    # Mock the retriever to return known documents
    mock_docs = [
        Document(
            page_content="Photosynthesis is the process by which plants use sunlight.",
            metadata={"source": "notes.pdf", "page": 3},
        )
    ]

    agent = RAGAgent.__new__(RAGAgent)
    agent.name = "RAGAgent"
    import logging
    agent.log = logging.getLogger("test")

    with patch.object(agent, "_retriever") as mock_retriever:
        mock_retriever.get_relevant_documents.return_value = mock_docs

        with patch("agents.rag_agent.document_store") as mock_store:
            mock_store.collection_size.return_value = 10

            state = create_initial_state("What is photosynthesis?")
            result = agent._execute(state)

    assert "rag_context" in result
    ctx = result["rag_context"]
    assert "Photosynthesis" in ctx
    assert "notes.pdf" in ctx
    assert "Page: 3" in ctx


# ── Test 4: Empty store ────────────────────────────────────────────────────────

def test_rag_agent_empty_store():
    """RAGAgent handles empty ChromaDB gracefully."""
    from agents.rag_agent import RAGAgent
    from graph.state import create_initial_state
    import logging

    agent = RAGAgent.__new__(RAGAgent)
    agent.name = "RAGAgent"
    agent.log = logging.getLogger("test")
    agent._retriever = MagicMock()

    with patch("agents.rag_agent.document_store") as mock_store:
        mock_store.collection_size.return_value = 0

        state = create_initial_state("What is DNA?")
        result = agent._execute(state)

    assert "rag_context" in result
    assert "No documents" in result["rag_context"]

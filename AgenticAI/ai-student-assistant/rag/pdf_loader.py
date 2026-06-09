"""
rag/pdf_loader.py
─────────────────
Loads PDF files, splits them into chunks, and stores them in ChromaDB.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE FULL RAG INGEST PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  PDF file
     │
     ▼
  [PyMuPDFLoader]          ← reads pages, preserves layout
     │
     ▼  list of Document(page_content=full_page_text, metadata={source, page})
     │
  [RecursiveCharacterTextSplitter]
     │  splits each page into overlapping chunks of ~500 chars
     ▼  list of smaller Document objects
     │
  [HuggingFaceEmbeddings]  ← converts each chunk's text to a vector
     │
     ▼
  [ChromaDB]               ← stores (text, vector, metadata) on disk

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY CHUNK_OVERLAP?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
If a sentence is split across two chunks, the context is broken.
Overlap ensures each chunk shares 50 characters with the previous chunk,
so no sentence is ever completely cut off.

WHY RecursiveCharacterTextSplitter?
────────────────────────────────────
It tries to split at natural boundaries in order:
  1. Paragraph break (\n\n)
  2. Newline (\n)
  3. Space
  4. Character
This produces more coherent chunks than a simple fixed-size split.
"""

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import settings
from rag.document_store import document_store
from utils.logger import get_logger

log = get_logger(__name__)


def load_and_ingest_pdf(pdf_path: str | Path) -> int:
    """
    Load a PDF, chunk it, embed it, and store it in ChromaDB.

    Parameters
    ──────────
    pdf_path : Path to the PDF file.

    Returns
    ───────
    Number of chunks ingested.

    Raises
    ──────
    FileNotFoundError  if the PDF doesn't exist.
    ValueError         if the PDF has no extractable text.
    """
    pdf_path = Path(pdf_path).resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    log.info("Loading PDF: %s", pdf_path.name)

    # ── Step 1: Load PDF pages ────────────────────────────────────────────────
    # PyMuPDFLoader (via pymupdf / fitz) is faster and more accurate than
    # pypdf for most PDFs.  It preserves column layout, tables (partially),
    # and returns one Document per page.
    loader = PyMuPDFLoader(str(pdf_path))
    pages: List[Document] = loader.load()
    log.info("  Loaded %d pages", len(pages))

    if not pages or not any(p.page_content.strip() for p in pages):
        raise ValueError(f"PDF has no extractable text: {pdf_path.name}")

    # ── Step 2: Add source metadata ───────────────────────────────────────────
    # We tag every chunk with the original filename so the Answer Agent can
    # cite its sources.
    for doc in pages:
        doc.metadata["source"] = pdf_path.name

    # ── Step 3: Split into chunks ─────────────────────────────────────────────
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.rag_chunk_size,
        chunk_overlap=settings.rag_chunk_overlap,
        length_function=len,
        # Preferred split points (tried in order)
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks: List[Document] = splitter.split_documents(pages)
    log.info("  Split into %d chunks (size=%d, overlap=%d)",
             len(chunks), settings.rag_chunk_size, settings.rag_chunk_overlap)

    # Add a chunk_index to each chunk's metadata for traceability
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    # ── Step 4: Embed & store ─────────────────────────────────────────────────
    count = document_store.add_documents(chunks)

    log.info("✅ PDF '%s' ingested: %d chunks stored in ChromaDB",
             pdf_path.name, count)
    return count


def ingest_directory(directory: str | Path | None = None) -> dict:
    """
    Ingest all PDFs found in a directory.

    Parameters
    ──────────
    directory : Directory to scan.  Defaults to settings.pdf_dir.

    Returns
    ───────
    dict mapping filename → number of chunks ingested.
    """
    scan_dir = Path(directory or settings.pdf_dir)
    pdf_files = list(scan_dir.glob("*.pdf"))

    if not pdf_files:
        log.warning("No PDF files found in %s", scan_dir)
        return {}

    results = {}
    for pdf in pdf_files:
        try:
            count = load_and_ingest_pdf(pdf)
            results[pdf.name] = count
        except Exception as exc:
            log.error("Failed to ingest %s: %s", pdf.name, exc)
            results[pdf.name] = 0

    return results

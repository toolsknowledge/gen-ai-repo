"""
rag/loader.py — PDF Document Loader

Reads every PDF file from the configured data directory and returns
a list of LangChain Document objects, one per page.

Why per-page?
  Keeping pages as separate Documents lets us attach page-number
  metadata, which we surface in citations shown to the user.
"""

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

from config import DATA_DIR


def load_pdfs(data_dir: Path = DATA_DIR) -> List[Document]:
    """
    Load all PDF files found in `data_dir`.

    Returns
    -------
    List[Document]
        Each Document has:
          - page_content : str   — extracted text for that page
          - metadata     : dict  — {"source": filename, "page": page_number}

    Raises
    ------
    FileNotFoundError
        If `data_dir` does not exist.
    ValueError
        If no PDF files are found in `data_dir`.
    """
    data_dir = Path(data_dir)

    if not data_dir.exists():
        raise FileNotFoundError(
            f"PDF directory not found: {data_dir}\n"
            "Create the folder and drop your PDF files into it."
        )

    pdf_files = list(data_dir.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(
            f"No PDF files found in: {data_dir}\n"
            "Add at least one PDF before running the RAG agent."
        )

    all_documents: List[Document] = []

    for pdf_path in pdf_files:
        print(f"  📄 Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()           # one Document per page

        # Normalise metadata: keep just filename (not full path)
        for doc in pages:
            doc.metadata["source"] = pdf_path.name

        all_documents.extend(pages)

    print(f"  ✅ Loaded {len(all_documents)} pages from {len(pdf_files)} PDF(s).")
    return all_documents

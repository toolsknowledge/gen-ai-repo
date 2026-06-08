"""
rag/chunker.py — Text Chunker

Splits LangChain Documents into smaller, overlapping chunks.

Why chunk?
  LLMs have context limits and embeddings work best on short passages.
  Overlapping chunks (chunk_overlap) prevent losing context at boundaries.

Example with CHUNK_SIZE=500, CHUNK_OVERLAP=50:
  [...........500 chars............]
                            [...........500 chars............]
                            ^--- 50-char overlap keeps context
"""

from typing import List

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split a list of Documents into smaller overlapping chunks.

    Parameters
    ----------
    documents : List[Document]
        Raw documents returned by the loader.

    Returns
    -------
    List[Document]
        Chunked documents — each carries the same metadata as its
        parent (source filename, page number) so citations still work.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Try to split on paragraphs → sentences → words → characters
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    print(f"  ✂️  Created {len(chunks)} chunks from {len(documents)} pages "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}).")

    return chunks

"""
One-time script: Reads all knowledge base text files and stores them
as vector embeddings in ChromaDB using local SentenceTransformer model.
Run once before starting the server. Re-run after adding new KB files.
"""
import os, sys
sys.path.insert(0, ".")
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from loguru import logger

load_dotenv("backend/.env")

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")
KNOWLEDGE_BASE_DIR = Path("backend/knowledge_bases")

# Local embeddings — no API key needed
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)

COLLECTION_MAP = {
    "cwe": "cwe_database",
    "owasp": "owasp_rules",
    "fix_examples": "fix_examples",
    "team_standards": "team_standards",
    "past_reviews": "past_reviews",
}

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def ingest_directory(folder_name: str, collection_name: str):
    folder = KNOWLEDGE_BASE_DIR / folder_name
    if not folder.exists():
        logger.warning(f"Skipping '{folder_name}' — folder not found")
        return

    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_fn
    )
    doc_id = 0
    for txt_file in folder.glob("*.txt"):
        logger.info(f"Ingesting {txt_file.name}...")
        text = txt_file.read_text(encoding="utf-8")
        for chunk in chunk_text(text):
            collection.upsert(
                documents=[chunk],
                ids=[f"{folder_name}_{doc_id}"],
                metadatas=[{"source": txt_file.name, "kb": folder_name}]
            )
            doc_id += 1
    logger.success(f"Ingested {doc_id} chunks into '{collection_name}'")

if __name__ == "__main__":
    for folder, coll in COLLECTION_MAP.items():
        ingest_directory(folder, coll)
    logger.success("All knowledge bases ingested into ChromaDB!")
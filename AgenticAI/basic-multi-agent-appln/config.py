"""
config.py — Global configuration for the Multi-Agent AI Application.

All file paths, model settings, chunking parameters, and tool options
are defined here. Every other module imports from this file, so you
only ever need to change a value in one place.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Load .env file ──────────────────────────────────────────────────────────
load_dotenv()

# ── Base Paths ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent          # project root
DATA_DIR = BASE_DIR / "data" / "pdfs"               # drop PDFs here
CHROMA_DIR = BASE_DIR / "chroma_db"                 # ChromaDB persistence dir

# ── Anthropic / Claude ───────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

# Model used by both agents
CLAUDE_MODEL: str = "claude-sonnet-4-6"

# Safety: raise early if key is missing
if not ANTHROPIC_API_KEY:
    raise EnvironmentError(
        "ANTHROPIC_API_KEY is not set. "
        "Copy .env.example to .env and add your key."
    )

# ── RAG Agent settings ───────────────────────────────────────────────────────
# Sentence-Transformers model for local embeddings (no API call needed)
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

# ChromaDB collection name
CHROMA_COLLECTION: str = "rag_documents"

# Text splitting parameters
CHUNK_SIZE: int = 500        # characters per chunk
CHUNK_OVERLAP: int = 50      # overlap between consecutive chunks

# Number of chunks to retrieve per query
TOP_K_RESULTS: int = 4

# ── MCP Server settings ──────────────────────────────────────────────────────
MCP_SERVER_HOST: str = "127.0.0.1"
MCP_SERVER_PORT: int = 8765
MCP_SERVER_NAME: str = "multi-agent-tools"

# Weather tool
WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"

# ── LangGraph settings ───────────────────────────────────────────────────────
# Keywords in user query that route to the MCP/Tool agent
MCP_TRIGGER_KEYWORDS: list[str] = [
    "calculate", "calculator", "compute", "math",
    "weather", "temperature", "forecast", "humidity",
    "add", "subtract", "multiply", "divide",
    "plus", "minus", "times",
]

# ── Streamlit UI settings ────────────────────────────────────────────────────
APP_TITLE: str = "Multi-Agent AI Assistant"
APP_ICON: str = "🤖"

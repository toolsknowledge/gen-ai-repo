# Multi-Agent AI Application

A beginner-friendly multi-agent AI app built with Claude Sonnet, LangGraph, LangChain, MCP, ChromaDB, Sentence Transformers, and Streamlit.

## Architecture

```
User Query
  → Streamlit UI
  → LangGraph Router
  → RAG Agent  (PDF Q&A via ChromaDB)   OR
  → MCP Agent  (Calculator / Weather tools)
  → Claude Sonnet
  → Final Response
```

## Folder Structure

```
basic-multi-agent-appln/
├── agents/          # rag_agent.py, mcp_agent.py
├── graph/           # state.py, router.py, nodes.py, workflow.py
├── mcp_server/      # server.py + tools/calculator.py + tools/weather.py
├── rag/             # loader.py, chunker.py, embeddings.py, vectorstore.py
├── ui/              # app.py (Streamlit)
├── data/pdfs/       # drop your PDFs here
├── chroma_db/       # auto-created on first ingest
├── config.py
├── requirements.txt
└── .env
```

## Quick Start

### 1. Create virtual environment

```bash
python3.12 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set:
#   ANTHROPIC_API_KEY=sk-ant-...
#   WEATHER_API_KEY=...   (optional — mock data used if not set)
```

### 4. Run the app

```bash
streamlit run ui/app.py
```

Open http://localhost:8501 in your browser.

## Usage

### RAG Agent (Document Q&A)
1. Open the sidebar → upload one or more PDF files
2. Click **Build / Rebuild Vectorstore**
3. Ask questions about your documents

Example queries:
- "What is the main topic of the document?"
- "Summarise the key findings"
- "What does the document say about X?"

### MCP Tool Agent (Calculator + Weather)
No setup needed — just ask:

Example queries:
- "Calculate sqrt(144) + 3 * 7"
- "What is the weather in London?"
- "What is 15% of 2500?"
- "Temperature in Tokyo today?"

## Routing Logic

The LangGraph router uses keyword matching (defined in `config.py`):

| Keywords | Agent |
|----------|-------|
| calculate, compute, math, sqrt, add, multiply … | MCP Agent |
| weather, temperature, forecast, humidity … | MCP Agent |
| Everything else | RAG Agent |

## Testing

```bash
# Test RAG ingestion (add a PDF to data/pdfs/ first)
python -c "
from rag.loader import load_pdfs
from rag.chunker import chunk_documents
pages = load_pdfs()
chunks = chunk_documents(pages)
print(f'Loaded {len(chunks)} chunks')
"

# Test calculator tool
python -c "
from mcp_server.tools.calculator import calculate
print(calculate('sqrt(144) + 3 * 7'))
"

# Test weather tool (returns mock if no API key)
python -c "
from mcp_server.tools.weather import get_weather
print(get_weather('London'))
"

# Test full graph
python -c "
from graph.workflow import get_graph
g = get_graph()
r = g.invoke({'query': 'calculate 2 + 2'})
print(r['final_response'])
"
```

# AI Student Assistant — Complete Multi-Agent System

A beginner-friendly multi-agent AI project built with **Python**, **LangChain**, **LangGraph**, **MCP**, and **ChromaDB**, powered by **Claude (Anthropic)**.

---

## Architecture at a Glance

```
User Query
    │
    ▼
LangGraph State Machine
    │
    ├── Supervisor Agent  (routes every step)
    │       │
    │       ├──► RAG Agent      → ChromaDB vector search
    │       ├──► MCP Tool Agent → MCP Server (calculator, date, search)
    │       └──► Answer Agent   → LangChain LCEL chain → Claude
    │
    └── Final Answer → User
```

---

## Project Structure

```
ai-student-assistant/
│
├── main.py               ← Entry point; interactive REPL
├── upload_pdf.py         ← CLI tool to ingest PDFs
├── config.py             ← All settings (reads from .env)
├── requirements.txt      ← Python dependencies
├── .env.example          ← Copy to .env and add your API key
│
├── agents/               ← The four agents
│   ├── base_agent.py     ← Abstract base class (Template Method pattern)
│   ├── supervisor_agent.py ← Routes to next agent (uses Claude Haiku)
│   ├── rag_agent.py      ← Retrieves relevant document chunks
│   ├── mcp_tool_agent.py ← Calls MCP tools (calculator, date, search)
│   └── answer_agent.py   ← Synthesises the final answer
│
├── rag/                  ← Retrieval-Augmented Generation pipeline
│   ├── embeddings.py     ← HuggingFace sentence-transformers (local, free)
│   ├── document_store.py ← ChromaDB wrapper (add + retrieve)
│   └── pdf_loader.py     ← PDF → chunks → ChromaDB
│
├── mcp_tools/            ← Model Context Protocol server
│   └── server.py         ← MCP tools: calculate, get_current_date, web_search
│
├── chains/               ← LangChain LCEL chains
│   ├── prompts.py        ← All prompt templates (supervisor + answer)
│   └── answer_chain.py   ← prompt | llm | StrOutputParser
│
├── graph/                ← LangGraph orchestration
│   ├── state.py          ← AgentState TypedDict (shared between all nodes)
│   └── graph_builder.py  ← StateGraph: nodes, edges, conditional routing
│
├── utils/                ← Shared utilities
│   ├── logger.py         ← Rich-formatted logger
│   └── llm_factory.py    ← Creates cached ChatAnthropic instances
│
├── data/
│   ├── pdfs/             ← Drop PDFs here before ingesting
│   └── chroma_db/        ← ChromaDB persists here (auto-created)
│
└── tests/
    ├── test_rag.py        ← RAG pipeline tests
    ├── test_mcp_server.py ← MCP tools tests (no subprocess, no API key)
    └── test_graph.py      ← Graph state + routing tests (mocked LLM)
```

---

## Why Each Technology?

| Technology | Role | Why this one? |
|---|---|---|
| **LangChain** | Prompt templates, LCEL chains, retrievers | Rich ecosystem, standard abstraction |
| **LangGraph** | Agent orchestration, state machine | Built for loops/branching; uses the same state |
| **MCP** | Tool protocol standard | Open standard; any MCP server works |
| **ChromaDB** | Vector database | Local, zero-config, great for prototypes |
| **sentence-transformers** | Text embeddings | Free, local, no API key needed |
| **Claude Sonnet** | Answer synthesis | Best reasoning for long-form answers |
| **Claude Haiku** | Routing decisions | Cheap & fast; routing doesn't need big model |

---

## Quick Start

### 1. Set up Python environment

```bash
cd ai-student-assistant
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure your API key

```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Get your key at: https://console.anthropic.com/

### 3. Upload a PDF (optional)

```bash
# Drop any PDF into data/pdfs/ then run:
python upload_pdf.py data/pdfs/lecture_notes.pdf

# Or ingest an entire directory:
python upload_pdf.py data/pdfs/
```

### 4. Ask questions

```bash
# Interactive mode
python main.py

# Single question
python main.py "What is photosynthesis?"
python main.py "Calculate the compound interest on $1000 at 5% for 3 years"
python main.py "What does chapter 2 of my notes say about mitosis?"
```

---

## Agent-by-Agent Flow Walkthrough

### Example 1: Document question

**User:** "What is the exam schedule according to my notes?"

```
1. create_initial_state → AgentState{query="What is the exam schedule..."}

2. Supervisor runs → asks Haiku: "which agent next?"
   Haiku sees: no rag_context, no tool_results
   Haiku returns: "rag_agent"
   State: {next_agent: "rag_agent"}

3. RAG Agent runs
   → embeds query: [0.12, -0.87, ...]
   → ChromaDB cosine search → top 4 chunks
   → State: {rag_context: "[Chunk 1 | notes.pdf | Page: 3]\n..."}

4. Supervisor runs again → asks Haiku: "which agent next?"
   Haiku sees: rag_context populated, no answer yet
   Haiku returns: "answer_agent"

5. Answer Agent runs
   → calls generate_answer(query, rag_context, tool_results)
   → ANSWER_PROMPT | Claude Sonnet | StrOutputParser
   → State: {final_answer: "According to your notes...", next_agent: "END"}

6. Supervisor runs → sees final_answer exists → returns "END"

7. Graph terminates → main.py prints final_answer
```

### Example 2: Calculation

**User:** "What is 15% tip on a $47.50 meal?"

```
1. Supervisor → "mcp_agent"
   (Haiku detects calculation intent)

2. MCP Tool Agent
   → connects to mcp_tools/server.py via stdio
   → lists tools: [calculate, get_current_date, web_search]
   → asks Claude: "call calculate(47.50 * 0.15)"
   → MCP returns: "7.125"
   → State: {tool_results: {"calculate": "7.125"}}

3. Supervisor → "answer_agent"

4. Answer Agent → "A 15% tip on $47.50 is $7.13."
```

---

## Testing

```bash
# Run all tests (no API key needed – LLM is mocked)
pytest tests/ -v

# Run individual test files
pytest tests/test_mcp_server.py -v     # tests MCP tools directly
pytest tests/test_rag.py -v            # tests RAG pipeline (needs local embedding model)
pytest tests/test_graph.py -v          # tests routing logic
```

---

## Common Mistakes & Fixes

### ❌ "No module named 'mcp'"
```bash
pip install mcp==1.0.0
```

### ❌ "ANTHROPIC_API_KEY not set"
```bash
cp .env.example .env
# Add your key to .env
```

### ❌ "ChromaDB is empty – no PDFs ingested"
```bash
python upload_pdf.py data/pdfs/your_file.pdf
```

### ❌ "Supervisor loops forever"
- Check `MAX_ITERATIONS` in `.env` (default: 10).
- If the LLM routing is confused, add more detail to your query.

### ❌ "sentence_transformers model downloading forever"
- The first run downloads `all-MiniLM-L6-v2` (~90 MB) from HuggingFace.
- Subsequent runs use the cache in `~/.cache/huggingface/`.
- Ensure internet access for the first run.

### ❌ PDF has no text (scanned image PDF)
```bash
# Install tesseract OCR, then use pytesseract in pdf_loader.py
# (This is an advanced enhancement – not in scope for this project)
```

---

## Extending the System

### Add a new MCP tool
In `mcp_tools/server.py`:
```python
@mcp.tool()
def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between units."""
    # your implementation
    ...
```
The Supervisor will automatically discover and use it.

### Add a new agent
1. Create `agents/my_new_agent.py` extending `BaseAgent`.
2. Add `graph.add_node("my_agent", my_agent.run)` in `graph_builder.py`.
3. Add `graph.add_edge("my_agent", "supervisor")` for the loop-back.
4. Add `"my_agent": "my_agent"` to the conditional edge mapping.
5. Update `SUPERVISOR_PROMPT` in `chains/prompts.py` to describe the new agent.

---

## Technology Deep-Dives

### What is Retrieval-Augmented Generation (RAG)?
LLMs have a knowledge cutoff and don't know about your private documents.
RAG solves this by:
1. **Indexing**: Split documents into chunks, convert to vectors, store in ChromaDB.
2. **Retrieval**: On each query, find the most similar chunks using vector search.
3. **Augmentation**: Include those chunks in the prompt so Claude can reference them.

### What is LangGraph?
LangGraph models multi-step AI workflows as a directed graph where:
- **Nodes** are Python functions (agents) that transform state.
- **Edges** define the flow between nodes.
- **State** is a TypedDict shared by all nodes.
- **Conditional edges** allow dynamic routing based on state values.

### What is MCP (Model Context Protocol)?
MCP is an open standard (by Anthropic) for connecting LLMs to external tools.
- **Server**: exposes tools via JSON-RPC over stdio/HTTP.
- **Client**: discovers tools, calls them, reads results.
- **Benefit**: any MCP server works with any MCP client (Claude, VS Code, etc.).

---

*Built as a complete beginner tutorial for Multi-Agent AI Systems.*

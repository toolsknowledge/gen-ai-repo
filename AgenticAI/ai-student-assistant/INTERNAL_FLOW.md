# AI Student Assistant — Internal Execution Flow

> How the code runs from the moment you type a question to the moment you see the answer.

---

## The Big Picture

```
You type a question
       │
       ▼
main.py creates AgentState (shared notepad)
       │
       ▼
LangGraph starts the loop
       │
       ├──► Supervisor (iteration 1) ──► RAG Agent ──┐
       │                                              │ (loops back)
       ├──► Supervisor (iteration 2) ──► Answer Agent─┤
       │                                              │ (loops back)
       └──► Supervisor (iteration 3) ──► END          │
                                                      ▼
                                            Answer printed to terminal
```

---

## Step-by-Step Walkthrough

### Step 1 — You type a question

**File:** `main.py` → `interactive_mode()`

You run `python main.py` and type:
```
You: Summarise what my document says
```

The `input()` call captures your text and passes it to the `ask(query)` function.

---

### Step 2 — The shared notepad is created

**File:** `graph/state.py` → `create_initial_state(query)`

Before any agent runs, a Python dictionary called `AgentState` is created.
Think of it as a **shared notepad** every agent can read and write on.

```python
AgentState = {
    "query":         "Summarise what my document says",
    "history":       [{"role": "user", "content": "Summarise..."}],
    "rag_context":   "",    # ← empty, nothing retrieved yet
    "tool_results":  {},    # ← empty, no tools called yet
    "final_answer":  "",    # ← empty, not answered yet
    "next_agent":    "supervisor",
    "iteration_count": 0,
    "error":         "",
}
```

**Why this matters:** Every agent reads from this dict and writes back to it.
LangGraph merges partial updates automatically — an agent only needs to return
the fields it changed, not the entire state.

---

### Step 3 — LangGraph takes control

**File:** `graph/graph_builder.py` → `student_assistant_graph.invoke(state)`

`main.py` calls:
```python
final_state = student_assistant_graph.invoke(initial_state)
```

LangGraph reads `entry_point = "supervisor"` and jumps to the Supervisor node first.
From this point, LangGraph controls the routing — it keeps running nodes in a loop
until it hits the `END` node.

**What LangGraph does internally:**
1. Calls the next node function with the current state
2. Merges the returned partial state into the full state
3. Calls the conditional edge function to decide which node is next
4. Repeats until `END`

---

### Step 4 — Supervisor Agent runs (Iteration 1)

**Files:** `agents/supervisor_agent.py` → `chains/prompts.py` → `utils/llm_factory.py`

The Supervisor is the "traffic controller." It looks at the current state and decides
which agent should run next.

**What happens:**
1. Checks if `final_answer` is already filled → No, skip
2. Checks if there is an error in state → No, skip
3. Builds the supervisor prompt from `chains/prompts.py`:
   ```
   Query: "Summarise what my document says"
   RAG context collected: False
   Tool results collected: False
   Final answer written: False
   Iteration: 1 / 10
   → Which agent should handle this next?
   ```
4. Sends this to **Claude Haiku** (fast, cheap model) via `utils/llm_factory.py`
5. Haiku replies: `"rag_agent"`
6. Supervisor writes `state["next_agent"] = "rag_agent"`

**The conditional edge in `graph_builder.py`** reads `next_agent` and routes the
graph to the `rag_agent` node.

```python
# This function decides the routing
def route_to_next_agent(state):
    return state["next_agent"]   # returns "rag_agent"
```

---

### Step 5 — RAG Agent runs

**Files:** `agents/rag_agent.py` → `rag/document_store.py` → `rag/embeddings.py` → ChromaDB on disk

RAG = Retrieval-Augmented Generation. This agent finds the most relevant text
from your uploaded PDF and puts it into the state so the Answer Agent can use it.

**What happens — 3 sub-steps:**

#### Sub-step A: Embed the query
```
"Summarise what my document says"
        │
        ▼
HuggingFace all-MiniLM-L6-v2 (runs locally on your CPU)
        │
        ▼
[0.12, -0.45, 0.87, 0.03, ...]   ← 384 numbers (a vector)
```
The embedding model converts text into numbers. Similar sentences produce similar
number lists. This is what makes the search "intelligent."

#### Sub-step B: Search ChromaDB
```
Your query vector: [0.12, -0.45, 0.87, ...]
        │
        ▼
ChromaDB compares it against all 9 stored chunk vectors
using cosine similarity (angle between vectors)
        │
        ▼
Returns 4 most similar chunks from biology_notes.pdf
```
No LLM is called here. This is pure math — no API cost.

#### Sub-step C: Format and save
```python
# rag_agent.py builds this string:
rag_context = """
[Chunk 1 | Source: biology_notes.pdf | Page: 1]
The cell is the basic structural and functional unit...

---

[Chunk 2 | Source: biology_notes.pdf | Page: 1]
Photosynthesis is the process by which green plants...

---
...
"""

# Writes it back to state
state["rag_context"] = rag_context
```

After RAG Agent finishes, the **fixed edge** `rag_agent → supervisor` in
`graph_builder.py` sends control back to the Supervisor.

---

### Step 6 — Supervisor Agent runs (Iteration 2)

**Files:** `agents/supervisor_agent.py` → Claude Haiku

The Supervisor runs again with updated state.

**What happens:**
1. Checks `final_answer` → still empty
2. Builds the prompt again, now with updated state:
   ```
   RAG context collected: True   ← changed!
   Tool results collected: False
   Final answer written: False
   ```
3. Sends to Haiku again
4. Haiku sees `rag_context` is populated → replies: `"answer_agent"`
5. Supervisor writes `state["next_agent"] = "answer_agent"`

The conditional edge routes to the `answer_agent` node.

---

### Step 7 — Answer Agent runs

**Files:** `agents/answer_agent.py` → `chains/answer_chain.py` → `chains/prompts.py` → Claude Sonnet

This is the only step where the smart, expensive model (Claude Sonnet) is called.

**What happens — the LCEL Chain:**

```
ANSWER_PROMPT.format_messages(
    query       = "Summarise what my document says",
    rag_context = "[Chunk 1 | biology_notes.pdf]...",
    tool_results = "No tool results available."
)
        │
        ▼
[SystemMessage, HumanMessage]     ← list of chat messages
        │
        ▼
ChatAnthropic(model="claude-sonnet-4-6")   ← API call to Anthropic
        │
        ▼
AIMessage(content="The document covers cell biology...")
        │
        ▼
StrOutputParser()                 ← extracts plain string from AIMessage
        │
        ▼
"The document covers cell biology, photosynthesis..."
```

The chain is defined as:
```python
_answer_chain = ANSWER_PROMPT | get_smart_llm() | StrOutputParser()
```

The `|` pipe operator is LangChain LCEL — it chains components like Unix pipes.

After the Answer Agent finishes:
```python
state["final_answer"] = "The document covers..."
state["next_agent"]   = "END"
```

The fixed edge `answer_agent → supervisor` sends control back to Supervisor.

---

### Step 8 — Supervisor Agent runs (Iteration 3)

**File:** `agents/supervisor_agent.py`

```python
# First check in supervisor_agent.py:
if state.get("final_answer"):
    log.info("Final answer already written → END")
    return {"next_agent": "END", "iteration_count": iteration}
```

`final_answer` is now filled → Supervisor **skips the LLM call entirely** and
immediately returns `"END"`.

The conditional edge hits the `END` node. LangGraph stops the loop and returns
the final state to `main.py`.

---

### Step 9 — Answer is printed

**File:** `main.py`

```python
final_state = student_assistant_graph.invoke(initial_state)
answer = final_state["final_answer"]
console.print(Markdown(answer))
```

The `rich` library renders the answer with Markdown formatting in your terminal.

---

## Complete File Map

| Step | Files Called | What They Do |
|------|-------------|--------------|
| 1 | `main.py` | Captures user input, calls `ask()` |
| 2 | `graph/state.py` | Creates `AgentState` TypedDict |
| 3 | `graph/graph_builder.py` | Starts LangGraph loop, routes nodes |
| 4,6,8 | `agents/supervisor_agent.py` | Decides next agent using Haiku |
| 4,6,8 | `chains/prompts.py` | Supervisor prompt template |
| 4,6,8 | `utils/llm_factory.py` | Creates cached ChatAnthropic instance |
| 5 | `agents/rag_agent.py` | Orchestrates RAG retrieval |
| 5 | `rag/embeddings.py` | Loads HuggingFace embedding model |
| 5 | `rag/document_store.py` | Queries ChromaDB |
| 7 | `agents/answer_agent.py` | Calls the answer chain |
| 7 | `chains/answer_chain.py` | LCEL chain: prompt | llm | parser |
| 7 | `chains/prompts.py` | Answer prompt template |
| All | `agents/base_agent.py` | Error handling wrapper for all agents |
| All | `config.py` | Settings loaded from .env |
| All | `utils/logger.py` | Coloured log output |

---

## API Calls Made (for one question)

| Call # | Model | File | Why |
|--------|-------|------|-----|
| 1 | Claude Haiku | `supervisor_agent.py` | Routing decision: → rag_agent |
| 2 | HuggingFace (local) | `rag/embeddings.py` | Embed the query — **no API cost** |
| 3 | ChromaDB (local) | `rag/document_store.py` | Vector search — **no API cost** |
| 4 | Claude Haiku | `supervisor_agent.py` | Routing decision: → answer_agent |
| 5 | Claude Sonnet | `chains/answer_chain.py` | Generate the final answer |

**Total Anthropic API calls: 3** (2 Haiku + 1 Sonnet)

---

## What Happens for Different Query Types

### Query about your PDF
```
Supervisor → rag_agent → Supervisor → answer_agent → END
```

### Calculation or date question
```
Supervisor → mcp_agent → Supervisor → answer_agent → END
```
MCP Agent spawns `mcp_tools/server.py` as a subprocess, calls the tool over
stdio, gets the result back.

### Simple general knowledge question
```
Supervisor → answer_agent → END
```
Supervisor routes directly to answer_agent — no RAG or tools needed.

---

## The State at Each Stage

```
After Step 2 (initial):
  query="Summarise..."  rag_context=""  final_answer=""  next_agent="supervisor"

After Step 4 (Supervisor 1):
  next_agent="rag_agent"  iteration_count=1

After Step 5 (RAG Agent):
  rag_context="[Chunk 1 | biology_notes.pdf]..."  (4 chunks)

After Step 6 (Supervisor 2):
  next_agent="answer_agent"  iteration_count=2

After Step 7 (Answer Agent):
  final_answer="The document covers cell biology..."  next_agent="END"

After Step 8 (Supervisor 3):
  next_agent="END"  iteration_count=3  ← LangGraph stops here
```

---

## Key Design Decisions Explained

**Why does the Supervisor loop back after every agent?**
So it can re-evaluate after each step. If RAG finds nothing useful, it can decide
to call an MCP tool instead. This "plan → act → re-plan" loop is the core of
agentic AI.

**Why use Haiku for routing and Sonnet for answering?**
Routing is simple (pick one word from 4 options) — Haiku is 10× cheaper and
3× faster for this. Answering requires intelligence and long context — Sonnet
is worth the cost there.

**Why is the embedding model local (HuggingFace) instead of an API?**
You might embed thousands of chunks when uploading PDFs. A local model costs
nothing per call, works offline, and is fast enough for document-scale workloads.

**Why TypedDict for AgentState instead of a class?**
LangGraph requires the state to be a dict (TypedDict or plain dict). This also
makes it trivially serializable — you could save/restore a conversation by
pickling the dict.

**Why LCEL (`prompt | llm | parser`) instead of plain Python?**
LCEL gives you streaming, retries, and LangSmith tracing for free. The `|` syntax
also makes the data flow visually obvious — left to right, like a Unix pipe.

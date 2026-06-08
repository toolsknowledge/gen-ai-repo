"""
ui/app.py — Streamlit Frontend

Single-page chat interface for the Multi-Agent AI Application.

Layout
------
┌─────────────────────────────────────────────────────────┐
│  Sidebar                  │  Main chat area             │
│  ─────────────────────    │  ─────────────────────────  │
│  • PDF upload             │  • Conversation history     │
│  • Ingest button          │  • Agent badge (RAG/MCP)    │
│  • Status messages        │  • Source citations         │
│  • App info               │  • Query input box          │
└─────────────────────────────────────────────────────────┘

Run
---
streamlit run ui/app.py
"""

import sys
import os
from pathlib import Path

# ── Make project root importable regardless of where streamlit is launched ────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import shutil
import streamlit as st

from config import APP_TITLE, APP_ICON, DATA_DIR
from graph.workflow import get_graph


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Session state initialisation ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # [{role, content, meta}]

if "vectorstore_ready" not in st.session_state:
    chroma_dir = ROOT / "chroma_db"
    st.session_state.vectorstore_ready = chroma_dir.exists()

if "graph" not in st.session_state:
    st.session_state.graph = None           # lazy-loaded on first query


def load_graph():
    """Load (compile) the LangGraph workflow once per session."""
    if st.session_state.graph is None:
        with st.spinner("⚙️ Compiling LangGraph workflow…"):
            st.session_state.graph = get_graph()
    return st.session_state.graph


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title(f"{APP_ICON} {APP_TITLE}")
    st.markdown("---")

    # ── PDF Upload ────────────────────────────────────────────────────────────
    st.subheader("📄 Document Ingestion (RAG)")
    st.caption("Upload PDFs to build the knowledge base.")

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Files will be saved to data/pdfs/ and indexed into ChromaDB.",
    )

    if uploaded_files:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        saved = []
        for uf in uploaded_files:
            dest = DATA_DIR / uf.name
            with open(dest, "wb") as f:
                f.write(uf.read())
            saved.append(uf.name)
        st.success(f"Saved {len(saved)} file(s): {', '.join(saved)}")

    # ── Ingest Button ─────────────────────────────────────────────────────────
    if st.button("🔄 Build / Rebuild Vectorstore", use_container_width=True):
        pdf_files = list(DATA_DIR.glob("*.pdf")) if DATA_DIR.exists() else []
        if not pdf_files:
            st.error("No PDFs found in data/pdfs/. Upload files first.")
        else:
            # Wipe existing ChromaDB so it rebuilds cleanly
            chroma_dir = ROOT / "chroma_db"
            if chroma_dir.exists():
                shutil.rmtree(chroma_dir)
            st.session_state.vectorstore_ready = False

            # Reset the RAG agent's cached vectorstore
            import agents.rag_agent as rag_mod
            rag_mod._vectorstore = None

            with st.spinner(f"Ingesting {len(pdf_files)} PDF(s)…"):
                try:
                    from rag.loader import load_pdfs
                    from rag.chunker import chunk_documents
                    from rag.vectorstore import build_vectorstore

                    pages  = load_pdfs(DATA_DIR)
                    chunks = chunk_documents(pages)
                    vs     = build_vectorstore(chunks)
                    rag_mod._vectorstore = vs

                    st.session_state.vectorstore_ready = True
                    st.success(
                        f"✅ Indexed {len(chunks)} chunks from "
                        f"{len(pdf_files)} PDF(s)."
                    )
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")

    # ── Status ────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("🔌 System Status")

    rag_status  = "✅ Ready" if st.session_state.vectorstore_ready else "⚠️ No vectorstore"
    mcp_status  = "✅ Ready"
    llm_status  = "✅ Claude Sonnet"

    st.markdown(f"**RAG Agent** — {rag_status}")
    st.markdown(f"**MCP Agent** — {mcp_status}")
    st.markdown(f"**LLM** — {llm_status}")

    st.markdown("---")
    st.caption(
        "**How routing works:**\n\n"
        "Queries containing keywords like *calculate*, *weather*, *sqrt* "
        "→ **MCP Agent** (tools)\n\n"
        "All other queries → **RAG Agent** (documents)"
    )

    # ── Clear Chat ────────────────────────────────────────────────────────────
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Main Chat Area ────────────────────────────────────────────────────────────
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption("Ask anything — I'll route your question to the right agent automatically.")
st.markdown("---")

# ── Render conversation history ───────────────────────────────────────────────
for msg in st.session_state.messages:
    role    = msg["role"]
    content = msg["content"]
    meta    = msg.get("meta", {})

    with st.chat_message(role):
        st.markdown(content)

        # Show agent badge + tool result / sources for assistant messages
        if role == "assistant" and meta:
            agent = meta.get("agent", "")
            cols  = st.columns([1, 4])

            with cols[0]:
                if agent == "rag":
                    st.success("📄 RAG Agent")
                elif agent == "mcp":
                    st.info("🔧 MCP Agent")

            # Tool result (MCP)
            tool_result = meta.get("tool_result", "")
            if tool_result:
                with st.expander("🛠 Tool Output"):
                    st.code(tool_result, language="text")

            # Source citations (RAG)
            source_docs = meta.get("source_docs", [])
            if source_docs:
                with st.expander(f"📚 Sources ({len(source_docs)} chunks)"):
                    for i, doc in enumerate(source_docs, 1):
                        src  = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "?")
                        st.markdown(f"**[{i}] {src} — page {page}**")
                        st.caption(doc.page_content[:300] + "…")
                        if i < len(source_docs):
                            st.divider()


# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask a question…"):

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the LangGraph pipeline
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                graph  = load_graph()
                result = graph.invoke({"query": prompt})

                response    = result.get("final_response", "No response generated.")
                route       = result.get("route", "rag")
                tool_result = result.get("tool_result", "")
                source_docs = result.get("source_docs", [])
                error       = result.get("error")

                if error:
                    st.error(f"⚠️ Error: {error}")

                st.markdown(response)

                # Agent badge
                cols = st.columns([1, 4])
                with cols[0]:
                    if route == "rag":
                        st.success("📄 RAG Agent")
                    elif route == "mcp":
                        st.info("🔧 MCP Agent")

                # Tool output
                if tool_result:
                    with st.expander("🛠 Tool Output"):
                        st.code(tool_result, language="text")

                # Source citations
                if source_docs:
                    with st.expander(f"📚 Sources ({len(source_docs)} chunks)"):
                        for i, doc in enumerate(source_docs, 1):
                            src  = doc.metadata.get("source", "Unknown")
                            page = doc.metadata.get("page", "?")
                            st.markdown(f"**[{i}] {src} — page {page}**")
                            st.caption(doc.page_content[:300] + "…")
                            if i < len(source_docs):
                                st.divider()

                # Persist to session history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "meta": {
                        "agent": route,
                        "tool_result": tool_result,
                        "source_docs": source_docs,
                    },
                })

            except Exception as e:
                error_msg = f"⚠️ An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "meta": {},
                })

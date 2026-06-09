"""
agents/rag_agent.py
───────────────────
The RAG Agent: retrieves relevant document chunks from ChromaDB.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT DOES THE RAG AGENT DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RAG = Retrieval-Augmented Generation.

Problem with pure LLMs: they only know what was in their training data.
If you upload a PDF about your company's internal policies, Claude has
never seen it.

Solution: Before asking Claude to answer, RETRIEVE the relevant passages
from the PDF and include them in the prompt.  Claude then answers based on
YOUR content, not just its training data.

Step-by-step:
  1. Take the user's query (e.g. "What is the exam schedule?")
  2. Embed it into a vector using the same model we used during ingest.
  3. Search ChromaDB for the top-4 chunks most similar to that vector.
  4. Join those chunks into a single text block.
  5. Write that text into state["rag_context"].
  6. The Answer Agent later uses state["rag_context"] to formulate the answer.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS THE AGENT'S CONTRIBUTION TO THE LANGCHAIN CHAIN?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The RAG Agent is a "tool node" in LangGraph.  It doesn't call the LLM –
it just queries the vector database.  The LLM is only invoked once, by
the Answer Agent, after all context has been gathered.

This is the most efficient pattern: gather all information FIRST, then
generate ONE response.
"""

from langchain_core.documents import Document

from agents.base_agent import BaseAgent
from graph.state import AgentState
from rag.document_store import document_store
from utils.logger import get_logger

log = get_logger(__name__)


class RAGAgent(BaseAgent):
    """Retrieves relevant document chunks from ChromaDB for the user's query."""

    def __init__(self) -> None:
        super().__init__("RAGAgent")
        # Get the retriever once; it's stateless so we can reuse it
        self._retriever = document_store.get_retriever()

    # ── Core logic ────────────────────────────────────────────────────────────

    def _execute(self, state: AgentState) -> AgentState:
        """
        Retrieve top-k relevant chunks and write them to state["rag_context"].

        Returns a partial state dict (only the fields this agent modifies).
        """
        query = state["query"]

        # Check if the store has any documents at all
        size = document_store.collection_size()
        if size == 0:
            log.warning("ChromaDB is empty – no PDFs have been ingested yet")
            return {                                         # type: ignore
                "rag_context": "No documents have been uploaded yet.",
                "history": [{"role": "system",
                             "content": "RAGAgent: ChromaDB is empty"}],
            }

        log.info("Searching ChromaDB (%d chunks) for: '%s'",
                 size, query[:60])

        # ── Retrieval ─────────────────────────────────────────────────────────
        # The retriever embeds the query and runs cosine similarity search.
        docs: list[Document] = self._retriever.invoke(query)

        if not docs:
            log.warning("No relevant chunks found for query")
            return {                                         # type: ignore
                "rag_context": "No relevant documents found for this query.",
                "history": [{"role": "system",
                             "content": "RAGAgent: no results"}],
            }

        # ── Format context block ──────────────────────────────────────────────
        # We format each chunk with its source and page number so the Answer
        # Agent can include citations in the final response.
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get("source", "unknown")
            page   = doc.metadata.get("page", "?")
            context_parts.append(
                f"[Chunk {i} | Source: {source} | Page: {page}]\n"
                f"{doc.page_content.strip()}"
            )

        rag_context = "\n\n---\n\n".join(context_parts)

        log.info("Retrieved %d chunks  (sources: %s)",
                 len(docs),
                 ", ".join({d.metadata.get("source", "?") for d in docs}))

        # ── Return partial state ──────────────────────────────────────────────
        # LangGraph merges this dict with the existing state.
        return {                                             # type: ignore
            "rag_context": rag_context,
            "history": [{
                "role": "system",
                "content": f"RAGAgent: retrieved {len(docs)} chunks",
            }],
        }


# ── Singleton ─────────────────────────────────────────────────────────────────
rag_agent = RAGAgent()

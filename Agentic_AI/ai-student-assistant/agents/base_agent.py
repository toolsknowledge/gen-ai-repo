"""
agents/base_agent.py
────────────────────
Abstract base class that every agent inherits from.

WHY A BASE CLASS?
──────────────────
All four agents (Supervisor, RAG, MCP Tool, Answer) share:
  • A name and a logger.
  • The same interface: run(state) → AgentState.
  • Error-handling boilerplate (try/except → write error into state).

Centralising this avoids copy-paste and makes the graph wiring easy:
    graph.add_node("rag_agent", rag_agent.run)
    graph.add_node("answer_agent", answer_agent.run)
Every agent's .run() has the same signature expected by LangGraph.

DESIGN PATTERN
──────────────
This is the Template Method pattern:
  • BaseAgent.run() calls self._execute() which subclasses override.
  • BaseAgent.run() wraps _execute() in a try/except for free error handling.
"""

from abc import ABC, abstractmethod
from graph.state import AgentState
from utils.logger import get_logger


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.log = get_logger(f"agents.{name}")

    # ── Public interface called by LangGraph nodes ────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """
        Entry point called by LangGraph.

        Wraps _execute() with:
          • A debug log showing the current query.
          • Error catching: any unhandled exception is written to state["error"]
            so the Supervisor can handle it gracefully.

        Returns a *partial* state dict – LangGraph merges it with the existing
        state automatically.  You only need to return the fields you changed.
        """
        self.log.info("[bold cyan]%s[/bold cyan] ▶ processing: '%s'",
                      self.name, state["query"][:60])

        try:
            result = self._execute(state)
            self.log.debug("%s ✓ completed", self.name)
            return result
        except Exception as exc:
            self.log.error("%s ✗ error: %s", self.name, exc, exc_info=True)
            # Return a partial state with only the error field updated.
            # LangGraph merges this with the existing state.
            return {"error": f"[{self.name}] {exc}"}   # type: ignore[return-value]

    # ── Subclasses must implement this ────────────────────────────────────────

    @abstractmethod
    def _execute(self, state: AgentState) -> AgentState:
        """
        Core logic for this agent.

        Receives the full current state.
        Returns a *partial* state dict with only the fields this agent updates.

        Example (RAG Agent):
            return {"rag_context": retrieved_text}
        """
        ...

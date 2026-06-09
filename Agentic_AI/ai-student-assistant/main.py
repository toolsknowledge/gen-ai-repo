"""
main.py
───────
Entry point for the AI Student Assistant.

USAGE
─────
  # Interactive chat mode
  python main.py

  # Ask a single question
  python main.py "What is photosynthesis?"

  # Ask about uploaded documents
  python main.py "Summarise chapter 2 of my notes"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  User types question
       │
       ▼
  create_initial_state(query)   ← initialise AgentState dict
       │
       ▼
  graph.invoke(state)            ← hand control to LangGraph
       │
       │  LangGraph loops:
       │    supervisor → rag_agent → supervisor
       │    supervisor → mcp_agent → supervisor
       │    supervisor → answer_agent → supervisor → END
       │
       ▼
  Print state["final_answer"]    ← show the result

Everything else (routing, retrieval, tool calls, synthesis) happens
automatically inside the graph.
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent))

from graph.state import create_initial_state
from graph.graph_builder import student_assistant_graph
from rag.document_store import document_store
from utils.logger import get_logger

console = Console()
log = get_logger(__name__)


def ask(query: str) -> str:
    """
    Send a question through the multi-agent graph and return the answer.

    This is the public API – tests and external callers use this.
    """
    if not query.strip():
        return "Please enter a question."

    log.info("="*60)
    log.info("User query: %s", query)
    log.info("="*60)

    # Build the initial state
    initial_state = create_initial_state(query)

    # Run the graph  (synchronous invoke – blocks until END node is reached)
    final_state = student_assistant_graph.invoke(initial_state)

    answer = final_state.get("final_answer", "")
    error  = final_state.get("error", "")

    if error:
        return f"⚠️  An error occurred: {error}"

    if not answer:
        return "I was unable to generate an answer. Please try again."

    return answer


def interactive_mode():
    """Run an interactive REPL loop."""
    db_size = document_store.collection_size()

    console.print(Panel(
        "[bold cyan]AI Student Assistant[/bold cyan]\n"
        "Powered by Claude + LangGraph + ChromaDB\n\n"
        f"📚 Documents in store: [bold]{db_size} chunks[/bold]\n"
        "   (To add PDFs: [italic]python upload_pdf.py yourfile.pdf[/italic])\n\n"
        "Type [bold]'quit'[/bold] or [bold]'exit'[/bold] to stop.\n"
        "Type [bold]'status'[/bold] to see the ChromaDB status.",
        title="Welcome",
        border_style="cyan",
    ))

    while True:
        try:
            query = console.input("\n[bold green]You:[/bold green] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not query:
            continue

        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye![/dim]")
            break

        if query.lower() == "status":
            size = document_store.collection_size()
            console.print(f"📊 ChromaDB has [bold]{size}[/bold] chunks stored.")
            continue

        # ── Ask the agent ──────────────────────────────────────────────────
        with console.status("[bold yellow]🤔 Thinking…[/bold yellow]"):
            answer = ask(query)

        # Render the answer as Markdown for nice formatting
        console.print("\n[bold blue]Assistant:[/bold blue]")
        console.print(Markdown(answer))
        console.print()


def main():
    if len(sys.argv) > 1:
        # One-shot mode: answer a single question and exit
        query  = " ".join(sys.argv[1:])
        answer = ask(query)
        console.print(Markdown(answer))
    else:
        interactive_mode()


if __name__ == "__main__":
    main()

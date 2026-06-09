"""
chains/answer_chain.py
──────────────────────
The LangChain LCEL chain used by the Answer Agent to synthesise a final answer.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS LCEL?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LCEL = LangChain Expression Language.

It's a way to compose LangChain components using the pipe `|` operator:
  chain = prompt | llm | output_parser

Reading left to right:
  1. prompt      : takes input variables → produces ChatMessages
  2. llm         : takes ChatMessages → produces an AIMessage
  3. output_parser: takes AIMessage → extracts the .content string

Under the hood, LangChain calls each component in sequence, passing the
output of one as the input to the next.  This is the Chain in LangChain.

WHY LCEL INSTEAD OF PLAIN PYTHON?
───────────────────────────────────
• Streaming: LCEL chains support .astream() out of the box.
• Retry / fallback: .with_retry() adds automatic retry logic.
• LangSmith tracing: LCEL chains are automatically traced in LangSmith
  for debugging.
• Composability: small chains can be combined into larger ones.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THIS CHAIN'S DATA FLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  {query, rag_context, tool_results}
           │
    ANSWER_PROMPT.format_messages(...)
           │  → list[SystemMessage, HumanMessage]
           │
    ChatAnthropic.invoke(messages)
           │  → AIMessage(content="...")
           │
    StrOutputParser()
           │  → plain string
           ▼
       final_answer
"""

import json
from langchain_core.output_parsers import StrOutputParser

from chains.prompts import ANSWER_PROMPT, NO_CONTEXT_PROMPT
from utils.llm_factory import get_smart_llm
from utils.logger import get_logger

log = get_logger(__name__)

# ── Build the chain ────────────────────────────────────────────────────────────
# StrOutputParser converts AIMessage → str automatically.
_answer_chain = ANSWER_PROMPT | get_smart_llm() | StrOutputParser()
_no_context_chain = NO_CONTEXT_PROMPT | get_smart_llm() | StrOutputParser()


def generate_answer(
    query: str,
    rag_context: str = "",
    tool_results: dict | None = None,
) -> str:
    """
    Generate a final answer using the ANSWER_PROMPT chain.

    Parameters
    ──────────
    query        : The user's original question.
    rag_context  : Retrieved document chunks (may be empty string).
    tool_results : Dict of {tool_name: result} (may be empty dict).

    Returns
    ───────
    A formatted answer string ready to show to the user.
    """
    tool_results = tool_results or {}

    # Format tool results for the prompt
    tool_str = ""
    if tool_results and not all(k == "info" for k in tool_results):
        lines = []
        for tool_name, result in tool_results.items():
            if tool_name not in ("info", "error"):
                lines.append(f"• {tool_name}: {result}")
        tool_str = "\n".join(lines)

    has_context = bool(rag_context.strip()) or bool(tool_str.strip())

    if not has_context:
        log.info("No context available – using fallback prompt")
        return _no_context_chain.invoke({"query": query})

    log.info("Generating answer with context (rag=%d chars, tools=%d)",
             len(rag_context), len(tool_str))

    return _answer_chain.invoke({
        "query": query,
        "rag_context": rag_context or "No document context available.",
        "tool_results": tool_str or "No tool results available.",
    })

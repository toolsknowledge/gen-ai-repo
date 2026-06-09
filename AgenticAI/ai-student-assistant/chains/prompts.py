"""
chains/prompts.py
─────────────────
All prompt templates used by the agents.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT IS A PROMPT TEMPLATE?  (Beginner explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
A prompt template is like a Mad Libs form:
  "Dear {name}, your score is {score}."

We define the template once with {placeholders}.
At runtime we fill in the placeholders with real values and send the
completed text to the LLM.

LangChain's ChatPromptTemplate handles:
  • Multiple message roles: SystemMessage, HumanMessage, AIMessage.
  • Type-safe placeholder substitution (.format_messages(name="Alice")).
  • Composability: templates can be combined into chains.

WHY KEEP PROMPTS IN A SEPARATE FILE?
─────────────────────────────────────
• Easier to iterate on prompts without touching agent logic.
• Can A/B test different prompt styles.
• Keeps agents focused on orchestration, not text crafting.
"""

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUPERVISOR ROUTING PROMPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """You are the Supervisor Agent in a multi-agent student assistant system.
Your job is to decide which agent should handle the user's query next.

AVAILABLE AGENTS
────────────────
• rag_agent    — Use when the query needs information from uploaded PDFs
                 or documents. Keywords: "what does the document say",
                 "according to", "in the notes", "explain from the PDF", etc.

• mcp_agent    — Use when the query needs external tools such as:
                 - Mathematical calculations ("calculate", "what is X * Y")
                 - Current date/time ("what day is it", "today's date")
                 - Web search ("search for", "find online", "latest news")

• answer_agent — Use when enough context has been gathered (rag_context or
                 tool_results are populated) and we are ready to write the
                 final answer.  Also use directly for simple conversational
                 questions that don't require documents or tools.

• END          — Use ONLY when final_answer is already populated.

CURRENT STATE
─────────────
Query: {query}
RAG context collected: {has_rag}
Tool results collected: {has_tools}
Final answer written: {has_answer}
Iteration: {iteration}/{max_iterations}

RULES
─────
1. Reply with EXACTLY ONE word from: rag_agent, mcp_agent, answer_agent, END
2. If iteration >= max_iterations, reply: answer_agent  (force conclusion)
3. If has_answer is True, reply: END
4. Never call the same agent twice in a row unless you have a good reason.
"""
    ),
    HumanMessagePromptTemplate.from_template(
        "Which agent should handle this next? Reply with one word only."
    ),
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ANSWER AGENT SYNTHESIS PROMPT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANSWER_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """You are a helpful AI Student Assistant.
Your job is to provide a clear, accurate, and well-structured answer to the
student's question using the context provided below.

GUIDELINES
──────────
• Use the RAG context to answer questions about uploaded documents.
• Use tool results for calculations, dates, and search results.
• If context is empty or irrelevant, answer from your general knowledge and
  say so clearly.
• Be concise but thorough. Use bullet points for lists.
• Always cite sources when using RAG context (mention the source filename).
• Do NOT make up information. If you don't know, say "I don't have enough
  information to answer that."

CONTEXT AVAILABLE
─────────────────
[RAG Document Context]
{rag_context}

[Tool Results]
{tool_results}
"""
    ),
    HumanMessagePromptTemplate.from_template(
        "Student question: {query}\n\nPlease provide a comprehensive answer."
    ),
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FALLBACK PROMPT (no context available)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NO_CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        """You are a helpful AI Student Assistant.
No documents have been uploaded yet and no tools were invoked.
Answer the student's question using your general knowledge.
Be honest about the limits of your knowledge."""
    ),
    HumanMessagePromptTemplate.from_template("{query}"),
])

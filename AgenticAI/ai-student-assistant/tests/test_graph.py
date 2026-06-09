"""
tests/test_graph.py
───────────────────
Tests for the LangGraph graph and state management.

These tests mock the LLM so they run without an API key.

HOW TO RUN
──────────
    pytest tests/test_graph.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

from graph.state import create_initial_state, AgentState


# ── State creation tests ──────────────────────────────────────────────────────

class TestAgentState:

    def test_initial_state_query(self):
        state = create_initial_state("What is DNA?")
        assert state["query"] == "What is DNA?"

    def test_initial_state_defaults(self):
        state = create_initial_state("test")
        assert state["rag_context"] == ""
        assert state["tool_results"] == {}
        assert state["final_answer"] == ""
        assert state["next_agent"] == "supervisor"
        assert state["iteration_count"] == 0
        assert state["error"] == ""

    def test_initial_history_has_user_message(self):
        state = create_initial_state("Hello!")
        assert len(state["history"]) == 1
        assert state["history"][0]["role"] == "user"
        assert state["history"][0]["content"] == "Hello!"

    def test_state_is_typed_dict(self):
        state = create_initial_state("test")
        # TypedDict instances are plain dicts
        assert isinstance(state, dict)


# ── Supervisor Agent tests (mocked LLM) ──────────────────────────────────────

class TestSupervisorAgent:

    def _make_agent(self):
        from agents.supervisor_agent import SupervisorAgent
        return SupervisorAgent()

    def test_routes_to_end_when_answer_present(self):
        agent = self._make_agent()
        state = create_initial_state("test")
        state["final_answer"] = "Here is the answer."
        state["iteration_count"] = 1

        result = agent.run(state)
        assert result["next_agent"] == "END"

    def test_respects_max_iterations(self):
        """After max iterations, supervisor forces answer_agent."""
        from config import settings

        agent = self._make_agent()
        state = create_initial_state("test")
        state["iteration_count"] = settings.max_iterations + 1

        result = agent.run(state)
        assert result["next_agent"] == "answer_agent"

    @patch("agents.supervisor_agent._routing_chain")
    def test_routes_to_rag_agent(self, mock_chain):
        """Supervisor routes to rag_agent when LLM says so."""
        mock_chain.invoke.return_value = "rag_agent"

        agent = self._make_agent()
        state = create_initial_state("What does the PDF say?")

        result = agent.run(state)
        assert result["next_agent"] == "rag_agent"

    @patch("agents.supervisor_agent._routing_chain")
    def test_handles_invalid_llm_response(self, mock_chain):
        """Supervisor defaults to answer_agent if LLM returns garbage."""
        mock_chain.invoke.return_value = "purple_unicorn"  # invalid

        agent = self._make_agent()
        state = create_initial_state("test")

        result = agent.run(state)
        assert result["next_agent"] == "answer_agent"


# ── Answer Agent tests (mocked LLM) ──────────────────────────────────────────

class TestAnswerAgent:

    @patch("chains.answer_chain.get_smart_llm")
    def test_writes_final_answer(self, mock_llm_fn):
        """Answer agent writes a non-empty final_answer to state."""
        # Mock the LLM to return a simple answer
        mock_llm = MagicMock()
        mock_llm.return_value = MagicMock()
        mock_llm_fn.return_value = mock_llm

        from agents.answer_agent import AnswerAgent
        from chains.answer_chain import generate_answer

        with patch("chains.answer_chain.generate_answer") as mock_gen:
            mock_gen.return_value = "Photosynthesis is the process of converting light."

            agent = AnswerAgent()
            state = create_initial_state("What is photosynthesis?")
            state["rag_context"] = "Photosynthesis converts sunlight…"

            result = agent.run(state)

        assert result["final_answer"] == "Photosynthesis is the process of converting light."
        assert result["next_agent"] == "END"

    def test_sets_next_agent_to_end(self):
        """Answer agent always sets next_agent=END."""
        with patch("chains.answer_chain.generate_answer") as mock_gen:
            mock_gen.return_value = "Answer."

            from agents.answer_agent import AnswerAgent
            agent = AnswerAgent()
            state = create_initial_state("test?")
            result = agent.run(state)

        assert result["next_agent"] == "END"


# ── Graph routing tests ───────────────────────────────────────────────────────

class TestGraphRouting:

    def test_router_fn_reads_state(self):
        """route_to_next_agent reads next_agent from state."""
        from graph.graph_builder import route_to_next_agent

        state = create_initial_state("test")
        state["next_agent"] = "rag_agent"

        assert route_to_next_agent(state) == "rag_agent"

    def test_router_fn_defaults_to_end(self):
        from graph.graph_builder import route_to_next_agent

        state = create_initial_state("test")
        # next_agent defaults to "supervisor", not "END"
        # If for some reason it's missing, should return END
        del state["next_agent"]

        result = route_to_next_agent(state)
        assert result == "END"  # get() default

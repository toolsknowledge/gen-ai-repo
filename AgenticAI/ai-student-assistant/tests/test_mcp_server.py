"""
tests/test_mcp_server.py
────────────────────────
Tests for the MCP server tools in isolation (no agent, no subprocess).

We test the Python functions directly since the MCP decorators
don't change their behaviour – they just register them as tools.

HOW TO RUN
──────────
    pytest tests/test_mcp_server.py -v
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the raw functions from the server (bypass MCP decorators)
from mcp_tools.server import calculate, get_current_date, web_search


# ── Calculator tests ──────────────────────────────────────────────────────────

class TestCalculate:

    def test_addition(self):
        assert calculate("2 + 3") == "5"

    def test_multiplication(self):
        assert calculate("6 * 7") == "42"

    def test_division(self):
        result = calculate("10 / 4")
        assert result == "2.5"

    def test_power(self):
        assert calculate("2 ** 10") == "1024"

    def test_sqrt(self):
        assert calculate("sqrt(144)") == "12"

    def test_complex_expression(self):
        result = calculate("(10 + 5) * 3 / 4")
        assert result == "11.25"

    def test_float_result(self):
        result = calculate("1 / 3")
        assert "0.33" in result

    def test_pi(self):
        result = calculate("pi")
        assert "3.14" in result

    def test_invalid_expression(self):
        result = calculate("import os")
        assert "Error" in result

    def test_division_by_zero(self):
        result = calculate("1 / 0")
        assert "Error" in result or "inf" in result.lower()

    def test_trig(self):
        result = calculate("sin(0)")
        assert result == "0"


# ── Date tool tests ───────────────────────────────────────────────────────────

class TestGetCurrentDate:

    def test_returns_string(self):
        result = get_current_date()
        assert isinstance(result, str)
        assert len(result) > 10

    def test_contains_year(self):
        result = get_current_date()
        import datetime
        year = str(datetime.datetime.now().year)
        assert year in result

    def test_contains_utc(self):
        result = get_current_date()
        assert "UTC" in result

    def test_accepts_timezone_param(self):
        result = get_current_date(timezone="US/Eastern")
        assert "US/Eastern" in result


# ── Web search stub tests ─────────────────────────────────────────────────────

class TestWebSearch:

    def test_returns_string(self):
        result = web_search("Python tutorial")
        assert isinstance(result, str)

    def test_contains_query(self):
        result = web_search("machine learning")
        assert "machine learning" in result

    def test_stub_message(self):
        result = web_search("anything")
        assert "STUB" in result or "stub" in result.lower() or "TODO" in result

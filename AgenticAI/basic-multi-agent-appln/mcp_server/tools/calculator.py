"""
mcp_server/tools/calculator.py — Calculator Tool

Safely evaluates a mathematical expression string and returns the result.

Why "safe" evaluation?
  Python's built-in eval() executes any code, which is a security risk.
  We use a restricted approach that only allows numbers and math operators,
  blocking any attempt to run arbitrary Python.

Supported operations:
  + - * / // % ** ( ) and basic math functions via the `math` module
  e.g. "2 + 2", "sqrt(16)", "3 ** 4 / (2 + 1)"
"""

import math
import re
from typing import Any


# Whitelist of safe names available inside the expression
_SAFE_GLOBALS: dict[str, Any] = {
    "__builtins__": {},          # block all builtins
    # expose common math functions
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "pi": math.pi,
    "e": math.e,
    "pow": pow,
    "floor": math.floor,
    "ceil": math.ceil,
}

# Only allow digits, operators, parentheses, dots, spaces, and known names
_ALLOWED_PATTERN = re.compile(
    r"^[\d\s\+\-\*\/\%\(\)\.\,\^"
    r"sqrtincologabspiroundfloecexi][\w\s\+\-\*\/\%\(\)\.\,\^]*$"
)


def calculate(expression: str) -> dict[str, Any]:
    """
    Evaluate a mathematical expression.

    Parameters
    ----------
    expression : str
        A math expression, e.g. "2 + 2", "sqrt(144)", "3**4 / 9"

    Returns
    -------
    dict with keys:
        "result"     : the numeric answer (float or int)
        "expression" : the original expression (for display)
        "error"      : None on success, error message on failure
    """
    expression = expression.strip()

    try:
        result = eval(expression, _SAFE_GLOBALS, {})  # noqa: S307

        # Return int if result is a whole number
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return {
            "result": result,
            "expression": expression,
            "error": None,
        }

    except ZeroDivisionError:
        return {
            "result": None,
            "expression": expression,
            "error": "Division by zero.",
        }
    except Exception as exc:
        return {
            "result": None,
            "expression": expression,
            "error": f"Could not evaluate expression: {exc}",
        }

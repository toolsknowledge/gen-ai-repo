"""
FastAPI Backend Server for Code Review Agent
Run: uvicorn server:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import anthropic
import os
import json
import re
from typing import Optional

app = FastAPI(title="Code Review Agent API")

# Allow React frontend (localhost:3000) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Anthropic client / Open AI / Gemini AI ──────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── Tool definitions (same as CLI version) ────────────
TOOLS = [
    {
        "name": "analyze_complexity",
        "description": "Analyze complexity metrics: line count, function count, nesting depth, cyclomatic complexity.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Source code to analyze"},
                "language": {"type": "string", "description": "Programming language", "default": "python"}
            },
            "required": ["code"]
        }
    },
    {
        "name": "check_security_patterns",
        "description": "Scan code for security anti-patterns: hardcoded secrets, SQL injection, eval usage, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Source code to scan"}
            },
            "required": ["code"]
        }
    }
]

SYSTEM_PROMPT = """You are an expert Code Review Agent with 15+ years of software engineering experience.

Always use analyze_complexity and check_security_patterns tools first, then give a full review.

Structure your review EXACTLY like this markdown:

## Overview
One paragraph describing what the code does.

## Bugs & Logic Errors
List each bug. Reference line numbers. Explain why it's a bug.

## Security Issues
List each issue with severity: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW

## Performance
List inefficiencies. Mention Big-O complexity where relevant.

## Readability & Style
Naming conventions, structure, comments.

## What's Done Well
At least 2 positive observations.

## Priority Fixes
1. [CRITICAL] ...
2. [HIGH] ...
3. [MEDIUM] ...

## Score
| Category | Score |
|---|---|
| Security | X/10 |
| Performance | X/10 |
| Readability | X/10 |
| **Overall** | **X/10** |
"""

# ── Tool implementations ──────────────────────────────
def tool_analyze_complexity(code: str, language: str = "python") -> dict:
    lines = code.splitlines()
    non_empty = [l for l in lines if l.strip() and not l.strip().startswith('#')]
    func_count = len([l for l in lines if re.search(r'^\s*(def |function |async function |\w+\s*=\s*(async\s*)?\()', l)])
    max_depth = max((len(l) - len(l.lstrip())) // 4 for l in lines if l.strip()) if lines else 0
    complexity = sum(1 for l in lines for kw in ['if ', 'elif ', 'else:', 'for ', 'while ', 'except', ' and ', ' or '] if kw in l) + 1
    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty),
        "function_count": func_count,
        "max_nesting_depth": max_depth,
        "cyclomatic_complexity": complexity,
        "rating": "Low" if complexity < 10 else "Medium" if complexity < 20 else "High"
    }

def tool_check_security_patterns(code: str) -> dict:
    patterns = [
        (r'password\s*=\s*["\'][^"\']+["\']', "Hardcoded password", "HIGH"),
        (r'api_key\s*=\s*["\'][^"\']+["\']', "Hardcoded API key", "HIGH"),
        (r'secret\s*=\s*["\'][^"\']+["\']', "Hardcoded secret", "HIGH"),
        (r'SELECT.*\+', "SQL Injection risk", "HIGH"),
        (r'eval\s*\(', "eval() — code injection risk", "HIGH"),
        (r'exec\s*\(', "exec() — injection risk", "HIGH"),
        (r'pickle\.loads?', "Pickle deserialization — RCE risk", "HIGH"),
        (r'shell=True', "Shell injection risk", "HIGH"),
        (r'hashlib\.md5|md5\(', "Weak MD5 hashing", "MEDIUM"),
        (r'http://', "Insecure HTTP", "MEDIUM"),
        (r'DEBUG\s*=\s*True', "Debug mode enabled", "MEDIUM"),
        (r'TODO|FIXME|HACK', "Unresolved TODO/FIXME", "LOW"),
    ]
    issues = []
    for pattern, label, sev in patterns:
        if re.search(pattern, code, re.IGNORECASE):
            issues.append({"issue": label, "severity": sev})
    return {"issues_found": len(issues), "issues": issues,
            "score": "PASS" if not issues else "WARN" if len(issues) < 3 else "FAIL"}

def execute_tool(name: str, inputs: dict) -> str:
    if name == "analyze_complexity":
        return json.dumps(tool_analyze_complexity(**inputs))
    if name == "check_security_patterns":
        return json.dumps(tool_check_security_patterns(**inputs))
    return json.dumps({"error": f"Unknown tool: {name}"})

# ── Request/Response models ───────────────────────────
class ReviewRequest(BaseModel):
    code: str
    language: str = "python"
    filename: Optional[str] = None

class ReviewResponse(BaseModel):
    review: str
    metrics: dict
    security: dict

# ── Agent loop ────────────────────────────────────────
def run_agent(code: str, language: str) -> tuple[str, dict, dict]:
    messages = [{
        "role": "user",
        "content": f"Review this {language} code:\n\n```{language}\n{code}\n```"
    }]
    metrics = {}
    security = {}
    review_text = ""

    for _ in range(8):  # max iterations
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        for block in response.content:
            if block.type == "text":
                review_text = block.text

        if not tool_uses:
            break

        results = []
        for tu in tool_uses:
            result_str = execute_tool(tu.name, tu.input)
            result_data = json.loads(result_str)
            if tu.name == "analyze_complexity":
                metrics = result_data
            elif tu.name == "check_security_patterns":
                security = result_data
            results.append({"type": "tool_result", "tool_use_id": tu.id, "content": result_str})
        messages.append({"role": "user", "content": results})

    return review_text, metrics, security

# ── API Endpoints ─────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Code Review Agent API running", "version": "1.0"}

@app.get("/health")
def health():
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return {"status": "ok", "api_key_set": key_set}

@app.post("/review", response_model=ReviewResponse)
def review_code(req: ReviewRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set on server")
    try:
        review, metrics, security = run_agent(req.code, req.language)
        return ReviewResponse(review=review, metrics=metrics, security=security)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scan")
def quick_scan(req: ReviewRequest):
    """Quick security scan without full AI review — instant response."""
    metrics = tool_analyze_complexity(req.code, req.language)
    security = tool_check_security_patterns(req.code)
    return {"metrics": metrics, "security": security}

# Code Review Agent — Complete Build Guide (Final)
### All Fixes Applied | Zero Broken Steps | Beautiful React UI

---

## Your Environment (Confirmed)
```
Python   : 3.11.15
Node.js  : v24.11.0
Git      : 2.51.2
OS       : macOS (Apple Silicon)
AWS Model: global.anthropic.claude-sonnet-4-6
```

---

## Phase Map
```
Phase 1 → Project Setup & Dependencies
Phase 2 → MCP Server + MCP Client
Phase 3 → Knowledge Bases + RAG Layer
Phase 4 → Code Review Agent Core
Phase 5 → FastAPI Backend
Phase 6 → Report Generator
Phase 7 → React + Vite Frontend (Beautiful UI)
Phase 8 → AWS Bedrock Integration
```

---

# PHASE 1 — Project Setup

## 1.1 Create Project

```bash
mkdir ~/Desktop/code-review-agent
cd ~/Desktop/code-review-agent
git init
echo ".venv/\n__pycache__/\n*.pyc\n.env\nvector_store/\nnode_modules/\ngenerated_reports/\nuploads/" > .gitignore
```

## 1.2 Create Full Folder Structure

```bash
mkdir -p \
  backend/agent \
  backend/mcp_server \
  backend/mcp_client \
  backend/rag \
  backend/knowledge_bases/cwe \
  backend/knowledge_bases/owasp \
  backend/knowledge_bases/fix_examples \
  backend/knowledge_bases/team_standards \
  backend/knowledge_bases/past_reviews \
  backend/api \
  backend/reports \
  backend/utils \
  scripts \
  vector_store \
  generated_reports \
  sample_code
```

## 1.3 Create All `__init__.py` Files (Required for Python imports)

```bash
touch backend/__init__.py
touch backend/agent/__init__.py
touch backend/mcp_server/__init__.py
touch backend/mcp_client/__init__.py
touch backend/rag/__init__.py
touch backend/api/__init__.py
touch backend/reports/__init__.py
touch backend/utils/__init__.py
touch scripts/__init__.py
```

## 1.4 Python Virtual Environment

```bash
cd ~/Desktop/code-review-agent
python3.11 -m venv backend/.venv
source backend/.venv/bin/activate
```

You will see `(.venv)` in your terminal prompt. Always activate this before running Python commands.

## 1.5 Create `backend/requirements.txt`

```bash
cat > backend/requirements.txt << 'EOF'
# LLM clients
anthropic==0.34.2
boto3>=1.35.0
botocore>=1.35.0

# MCP — Model Context Protocol
# mcp 1.0.0 needs starlette>=0.39
# fastapi 0.115.5 allows starlette up to <0.42 — DO NOT use 0.115.0
mcp==1.0.0
httpx==0.27.2

# RAG + Vector store
chromadb==0.5.15
sentence-transformers==3.1.1

# FastAPI backend
fastapi==0.115.5
uvicorn[standard]==0.30.6
python-multipart==0.0.12
aiofiles==24.1.0
websockets==13.1

# Report generation
jinja2==3.1.4
markdown2==2.5.0

# Utilities
python-dotenv==1.0.1
pydantic==2.9.2
loguru==0.7.2
tenacity==9.0.0
rich==13.8.1
pytest==8.3.3
EOF
```

## 1.6 Install Dependencies

```bash
pip install -r backend/requirements.txt
```

## 1.7 Create `backend/.env`

```bash
cat > backend/.env << 'EOF'
# ── AWS Bedrock ──────────────────────────────────────
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Global inference profile (routes across all AWS regions)
BEDROCK_MODEL_ID=global.anthropic.claude-sonnet-4-6

# Set to true to use Bedrock, false to use Anthropic API directly
USE_BEDROCK=true

# ── Anthropic API (fallback when USE_BEDROCK=false) ──
ANTHROPIC_API_KEY=your_anthropic_key_here
ANTHROPIC_MODEL=claude-sonnet-4-5

# ── RAG ──────────────────────────────────────────────
VECTOR_STORE_PATH=../vector_store
# Suppress ChromaDB telemetry noise
ANONYMIZED_TELEMETRY=False

# ── App settings ──────────────────────────────────────
MAX_FILE_SIZE_MB=10
LOG_LEVEL=INFO
UPLOAD_DIR=/tmp/code_uploads
REPORT_OUTPUT_DIR=../generated_reports
EOF
```

> **Replace** `your_access_key_here` and `your_secret_key_here` with your real AWS credentials.
> If you want to use Anthropic API instead of Bedrock, set `USE_BEDROCK=false` and add your `ANTHROPIC_API_KEY`.

---

# PHASE 2 — MCP Server + MCP Client

## 2.1 Create `backend/mcp_server/server.py`

```python
"""
MCP Server — exposes 4 tools the agent can call:
  read_file, list_files, detect_language, get_file_stats
"""
import os, json
from pathlib import Path
from typing import Any
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from loguru import logger

LANGUAGE_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
    ".java": "Java", ".c": "C", ".cpp": "C++", ".cs": "C#",
    ".go": "Go", ".rs": "Rust", ".rb": "Ruby", ".php": "PHP",
    ".swift": "Swift", ".kt": "Kotlin", ".sh": "Shell", ".sql": "SQL",
}

SAFE_BASE_DIR = Path(os.getenv("SAFE_BASE_DIR", "/tmp/code_uploads")).resolve()

def is_safe_path(path: Path) -> bool:
    try:
        path.resolve().relative_to(SAFE_BASE_DIR)
        return True
    except ValueError:
        return False

app = Server("code-review-mcp-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="read_file",
            description="Read full content of a code file.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
        types.Tool(
            name="list_files",
            description="List all files in a directory.",
            inputSchema={"type": "object", "properties": {
                "directory": {"type": "string"},
                "recursive": {"type": "boolean", "default": False}},
                "required": ["directory"]}
        ),
        types.Tool(
            name="detect_language",
            description="Detect programming language of a file.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
        types.Tool(
            name="get_file_stats",
            description="Get line count, blank lines, comments, language.",
            inputSchema={"type": "object", "properties": {
                "file_path": {"type": "string"}}, "required": ["file_path"]}
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "read_file":
        path = Path(arguments["file_path"]).resolve()
        if not is_safe_path(path):
            return [types.TextContent(type="text", text="ERROR: Access denied.")]
        if not path.exists():
            return [types.TextContent(type="text", text=f"ERROR: Not found: {path}")]
        return [types.TextContent(type="text", text=path.read_text(encoding="utf-8", errors="replace"))]

    elif name == "list_files":
        directory = Path(arguments["directory"]).resolve()
        pattern = "**/*" if arguments.get("recursive") else "*"
        files = [
            f"  {f.name} | {LANGUAGE_MAP.get(f.suffix.lower(),'Unknown')} | {f.stat().st_size/1024:.1f}KB"
            for f in directory.glob(pattern) if f.is_file()
        ]
        return [types.TextContent(type="text", text="\n".join(files) or "No files found.")]

    elif name == "detect_language":
        path = Path(arguments["file_path"])
        return [types.TextContent(type="text", text=LANGUAGE_MAP.get(path.suffix.lower(), "Unknown"))]

    elif name == "get_file_stats":
        path = Path(arguments["file_path"]).resolve()
        if not is_safe_path(path):
            return [types.TextContent(type="text", text="ERROR: Access denied.")]
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        total = len(lines)
        blank = sum(1 for l in lines if not l.strip())
        comments = sum(1 for l in lines if l.strip().startswith(("#","//","/*","*","--")))
        stats = {"total_lines": total, "code_lines": total-blank-comments,
                 "blank_lines": blank, "comment_lines": comments,
                 "language": LANGUAGE_MAP.get(path.suffix.lower(), "Unknown")}
        return [types.TextContent(type="text", text=json.dumps(stats, indent=2))]

    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 2.2 Create `backend/mcp_client/client.py`

```python
"""
MCP Client — connects the agent to the MCP Server tools.
"""
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from loguru import logger


class CodeReviewMCPClient:
    def __init__(self, server_script: str = "backend/mcp_server/server.py"):
        self.server_script = server_script
        self._session = None
        self._context = None

    async def __aenter__(self):
        server_params = StdioServerParameters(command="python", args=[self.server_script])
        self._context = stdio_client(server_params)
        read, write = await self._context.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        logger.info("MCP Client connected.")
        return self

    async def __aexit__(self, *args):
        if self._session:
            await self._session.__aexit__(*args)
        if self._context:
            await self._context.__aexit__(*args)

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        result = await self._session.call_tool(tool_name, arguments)
        return "\n".join(c.text for c in result.content if hasattr(c, "text"))

    async def list_available_tools(self) -> list[str]:
        tools = await self._session.list_tools()
        return [t.name for t in tools.tools]
```

## 2.3 Test MCP (optional verification step)

```bash
# Create a sample vulnerable file
mkdir -p /tmp/code_uploads
cat > /tmp/code_uploads/test_vuln.py << 'EOF'
def login(username, password):
    query = "SELECT * FROM users WHERE name='" + username + "'"
    return db.execute(query)
EOF

# Test MCP tools
python scripts/test_mcp.py
```

Create `scripts/test_mcp.py`:

```python
import asyncio, sys
sys.path.insert(0, ".")
from backend.mcp_client.client import CodeReviewMCPClient

async def main():
    async with CodeReviewMCPClient() as client:
        tools = await client.list_available_tools()
        print("Tools:", tools)
        lang = await client.call_tool("detect_language", {"file_path": "/tmp/code_uploads/test_vuln.py"})
        print("Language:", lang)
        stats = await client.call_tool("get_file_stats", {"file_path": "/tmp/code_uploads/test_vuln.py"})
        print("Stats:", stats)

asyncio.run(main())
```

---

# PHASE 3 — Knowledge Bases + RAG Layer

## 3.1 Create Knowledge Base Files

**`backend/knowledge_bases/cwe/cwe_top25.txt`**

```
CWE-89: SQL Injection
Description: Improper neutralization of special elements in SQL commands.
Languages: Python, Java, PHP, C#, JavaScript
Example bad code: query = "SELECT * FROM users WHERE name='" + username + "'"
Example fix: cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
Prevention: Always use parameterized queries. Never concatenate user input into SQL.
---
CWE-78: OS Command Injection
Description: Improper neutralization of special elements in OS commands.
Languages: Python, Java, PHP, C
Example bad code: subprocess.call(user_input, shell=True)
Example fix: subprocess.call(["ls", "-la", safe_dir])
Prevention: Avoid shell=True. Use list arguments. Validate and sanitize all input.
---
CWE-502: Deserialization of Untrusted Data
Description: Deserializing data from untrusted source allows code execution.
Languages: Python, Java, PHP
Example bad code: data = pickle.loads(user_input)
Example fix: data = json.loads(user_input)
Prevention: Never deserialize untrusted data. Use JSON or other safe formats.
---
CWE-22: Path Traversal
Description: Improper limitation of pathname to restricted directory.
Languages: Python, Java, C, C++
Example bad code: open("/var/data/" + user_input)
Example fix: safe = os.path.realpath(base + user_input); assert safe.startswith(base)
Prevention: Canonicalize paths and verify they are within the allowed base directory.
---
CWE-120: Buffer Overflow
Description: Copying data into buffer without checking size.
Languages: C, C++
Example bad code: char buf[10]; strcpy(buf, input);
Example fix: strncpy(buf, input, sizeof(buf) - 1);
Prevention: Always check buffer bounds. Use safe string functions.
---
CWE-476: NULL Pointer Dereference
Description: Dereferencing a NULL pointer causes crash.
Languages: C, C++, Java
Example bad code: char* p = getInput(); printf("%s", p);
Example fix: if (p != NULL) printf("%s", p);
Prevention: Always check pointers for NULL before dereferencing.
---
CWE-256: Plaintext Storage of Password
Description: Storing passwords in plaintext.
Example bad code: db.store(username, password)
Example fix: db.store(username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()))
Prevention: Always hash passwords with bcrypt, argon2, or scrypt. Never store plaintext.
---
CWE-20: Improper Input Validation
Description: Product does not validate or incorrectly validates input.
Prevention: Validate all inputs. Use allowlists. Check type, range, format, length.
---
CWE-208: Timing Attack
Description: Observable timing discrepancy allows information exposure.
Example bad code: if user["password"] == password:
Example fix: import hmac; hmac.compare_digest(user["password"], password)
Prevention: Use constant-time comparison functions for all secret comparisons.
```

**`backend/knowledge_bases/owasp/owasp_top10.txt`**

```
OWASP A01: Broken Access Control
Risk: Users act outside intended permissions.
Check for: Missing authorization, IDOR, privilege escalation.
Fix: Verify server-side that the current user owns the requested resource.
---
OWASP A02: Cryptographic Failures
Risk: Sensitive data exposed due to weak or missing encryption.
Check for: HTTP, MD5/SHA1 passwords, hardcoded keys, unencrypted storage.
Fix: Use bcrypt/argon2 for passwords. TLS 1.2+. Store secrets in env vars.
---
OWASP A03: Injection
Risk: Attacker sends malicious data interpreted as commands.
Check for: SQL injection, command injection, template injection.
Fix: Parameterized queries. Input validation. Never concatenate user input into queries.
---
OWASP A04: Insecure Design
Risk: Missing security controls at design level.
Check for: No rate limiting, no audit logs, no input validation architecture.
Fix: Threat modeling during design phase. Defense in depth.
---
OWASP A05: Security Misconfiguration
Risk: Default configs, verbose errors, missing patches.
Check for: Debug mode in production, default passwords, detailed error messages.
Fix: Disable debug mode. Remove defaults. Generic error messages to users.
---
OWASP A06: Vulnerable Components
Risk: Using libraries with known vulnerabilities.
Fix: Regularly audit and update dependencies. Use pip-audit, safety.
---
OWASP A07: Authentication Failures
Risk: Weak authentication allows account compromise.
Check for: Weak passwords accepted, no MFA, insecure session tokens.
Fix: Strong password policy, MFA, secure session management.
---
OWASP A08: Integrity Failures
Risk: Code or data assumed to be trusted without verification.
Check for: pickle.loads on untrusted data, unverified software updates.
Fix: Use digital signatures. Verify integrity of all external data.
---
OWASP A09: Logging Failures
Risk: Security events not logged, making incidents invisible.
Fix: Log all auth events, access denials, input validation failures.
---
OWASP A10: SSRF
Risk: Server makes requests to arbitrary URLs controlled by attacker.
Fix: Allowlist external services. Validate and sanitize all URLs. Disable redirects.
```

**`backend/knowledge_bases/fix_examples/python_fixes.txt`**

```
PATTERN: SQL Injection in Python
BEFORE:
    query = "SELECT * FROM users WHERE email='" + email + "'"
    cursor.execute(query)
AFTER:
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
WHY: Parameterized queries prevent user input from being interpreted as SQL.

PATTERN: Hardcoded Secret
BEFORE:
    API_KEY = "sk-abc123xyz"
AFTER:
    API_KEY = os.environ.get("API_KEY")
    if not API_KEY:
        raise RuntimeError("API_KEY environment variable is not set")
WHY: Secrets in code get committed to git. Use environment variables.

PATTERN: Unsafe deserialization
BEFORE:
    data = pickle.loads(user_input)
AFTER:
    data = json.loads(user_input)
WHY: pickle.loads on untrusted input allows arbitrary code execution.

PATTERN: Command injection
BEFORE:
    subprocess.call(user_cmd, shell=True)
AFTER:
    subprocess.call(["ls", "-la", validated_path])
WHY: shell=True with user input allows command injection.

PATTERN: Plaintext password comparison
BEFORE:
    if user["password"] == password:
AFTER:
    if bcrypt.checkpw(password.encode(), user["password_hash"]):
WHY: Plaintext passwords in database are catastrophic if leaked. Always hash.

PATTERN: Missing type hints
BEFORE:
    def process(data, config):
AFTER:
    def process(data: dict, config: AppConfig) -> ProcessResult:
WHY: Type hints catch bugs at development time and document intent.
```

**`backend/knowledge_bases/team_standards/standards.txt`**

```
RULE 1: All functions must have type hints in Python.
RULE 2: No bare except clauses. Always catch specific exceptions.
RULE 3: All public methods must have docstrings.
RULE 4: No print() calls in production code. Use logging module.
RULE 5: Never store passwords in plain text. Always hash with bcrypt.
RULE 6: Maximum function length is 50 lines. Split if longer.
RULE 7: All database queries must use parameterized statements.
RULE 8: Environment variables must be validated at startup.
RULE 9: All external inputs must be validated before use.
RULE 10: Security events must be logged with sufficient detail.
```

## 3.2 Create `scripts/ingest_knowledge_bases.py`

```python
"""
One-time script: Reads all knowledge base text files and stores them
as vector embeddings in ChromaDB using local SentenceTransformer model.
Run once before starting the server. Re-run after adding new KB files.
"""
import os, sys
sys.path.insert(0, ".")
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from pathlib import Path
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from loguru import logger

load_dotenv("backend/.env")

VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "vector_store")
KNOWLEDGE_BASE_DIR = Path("backend/knowledge_bases")

# Local embeddings — no API key needed
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)

COLLECTION_MAP = {
    "cwe": "cwe_database",
    "owasp": "owasp_rules",
    "fix_examples": "fix_examples",
    "team_standards": "team_standards",
    "past_reviews": "past_reviews",
}

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks

def ingest_directory(folder_name: str, collection_name: str):
    folder = KNOWLEDGE_BASE_DIR / folder_name
    if not folder.exists():
        logger.warning(f"Skipping '{folder_name}' — folder not found")
        return

    collection = client.get_or_create_collection(
        name=collection_name, embedding_function=embedding_fn
    )
    doc_id = 0
    for txt_file in folder.glob("*.txt"):
        logger.info(f"Ingesting {txt_file.name}...")
        text = txt_file.read_text(encoding="utf-8")
        for chunk in chunk_text(text):
            collection.upsert(
                documents=[chunk],
                ids=[f"{folder_name}_{doc_id}"],
                metadatas=[{"source": txt_file.name, "kb": folder_name}]
            )
            doc_id += 1
    logger.success(f"Ingested {doc_id} chunks into '{collection_name}'")

if __name__ == "__main__":
    for folder, coll in COLLECTION_MAP.items():
        ingest_directory(folder, coll)
    logger.success("All knowledge bases ingested into ChromaDB!")
```

Run it:
```bash
cd ~/Desktop/code-review-agent
source backend/.venv/bin/activate
python scripts/ingest_knowledge_bases.py
```

## 3.3 Create `backend/rag/retriever.py`

```python
"""
RAG Retrieval Layer — searches all knowledge bases for relevant context.
Fixes: empty collection guard, telemetry suppression, local embeddings.
"""
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from dataclasses import dataclass
from typing import Optional
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

@dataclass
class RetrievedChunk:
    source: str
    collection: str
    content: str
    distance: float

class RAGRetriever:
    COLLECTIONS = {
        "cwe_database": "CWE/CVE Database",
        "owasp_rules": "OWASP Security Rules",
        "fix_examples": "Fix Examples",
        "team_standards": "Team Coding Standards",
        "past_reviews": "Past Review History",
    }

    def __init__(self, vector_store_path: str = "vector_store"):
        self.embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=vector_store_path)
        self.collections: dict = {}
        self._load_collections()

    def _load_collections(self):
        try:
            existing = {c.name for c in self.client.list_collections()}
        except Exception as e:
            logger.error(f"Failed to list collections: {e}")
            return

        for name in self.COLLECTIONS:
            if name not in existing:
                logger.warning(f"Collection '{name}' not found — run ingest script first.")
                continue
            try:
                coll = self.client.get_collection(name=name, embedding_function=self.embedding_fn)
                count = coll.count()
                if count == 0:
                    logger.warning(f"Collection '{name}' has 0 documents — skipping.")
                    continue
                self.collections[name] = coll
                logger.info(f"Loaded '{name}' ({count} chunks).")
            except Exception as e:
                logger.error(f"Failed to load '{name}': {e}")

        logger.info(f"RAGRetriever ready — {len(self.collections)} collection(s) loaded.")

    def retrieve(self, query: str, top_k: int = 4,
                 collections: Optional[list[str]] = None) -> list[RetrievedChunk]:
        if not query or not query.strip():
            return []

        results = []
        for name in (collections or list(self.collections.keys())):
            coll = self.collections.get(name)
            if not coll:
                continue
            try:
                count = coll.count()
                if count == 0:
                    continue
                n = min(top_k, count)   # Never request more than available
                res = coll.query(query_texts=[query], n_results=n)
                for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
                    results.append(RetrievedChunk(
                        source=meta.get("kb", name),
                        collection=name, content=doc, distance=dist
                    ))
            except Exception as e:
                logger.error(f"RAG query failed for '{name}': {e}")

        results.sort(key=lambda x: x.distance)
        logger.info(f"RAG retrieved {len(results)} chunks.")
        return results

    def format_context_for_prompt(self, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "No additional context retrieved from knowledge bases."
        lines = ["=== RETRIEVED KNOWLEDGE BASE CONTEXT ==="]
        for i, c in enumerate(chunks, 1):
            lines.append(f"\n[{i}] Source: {c.source.upper()}")
            lines.append(c.content.strip())
        lines.append("\n=== END OF CONTEXT ===")
        return "\n".join(lines)

    def health_check(self) -> dict:
        status = {}
        for name, coll in self.collections.items():
            try:
                status[name] = {"count": coll.count(), "status": "ok"}
            except Exception as e:
                status[name] = {"count": 0, "status": f"error: {e}"}
        for name in self.COLLECTIONS:
            if name not in self.collections:
                status[name] = {"count": 0, "status": "not ingested"}
        return status
```

---

# PHASE 4 — Code Review Agent Core

## 4.1 Create `backend/agent/code_review_agent.py`

```python
"""
Code Review Agent Core
Supports two LLM backends:
  - USE_BEDROCK=true  → AWS Bedrock (global.anthropic.claude-sonnet-4-6)
  - USE_BEDROCK=false → Anthropic API directly
"""
import json, os, re
from dataclasses import dataclass, field, asdict
from typing import Optional

import anthropic
from dotenv import load_dotenv
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.rag.retriever import RAGRetriever
from backend.mcp_client.client import CodeReviewMCPClient

load_dotenv()

# ─── Data Models ─────────────────────────────────────

@dataclass
class ReviewIssue:
    priority: str
    category: str
    title: str
    description: str
    line_number: Optional[int]
    code_snippet: str
    cwe_reference: Optional[str]
    suggested_fix: str
    confidence: float

@dataclass
class CodeReviewResult:
    file_name: str
    language: str
    total_lines: int
    review_summary: str
    overall_score: int
    issues: list[ReviewIssue] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

# ─── System Prompt ────────────────────────────────────

SYSTEM_PROMPT = """You are an expert Code Review Agent with deep knowledge of:
- Security vulnerabilities (OWASP Top 10, CWE Top 25)
- Language-specific best practices (Python, Java, C/C++, JavaScript, etc.)
- Software design principles (SOLID, clean code)
- Performance anti-patterns

You will be given:
1. Code to review (with line numbers)
2. Retrieved knowledge base context (CWE entries, OWASP rules, fix examples)

Respond ONLY with valid JSON in this exact format:
{
  "review_summary": "2-3 sentence executive summary",
  "overall_score": <integer 0-100>,
  "issues": [
    {
      "priority": "P1|P2|P3|P4|P5",
      "category": "Security|Bug|Quality|Style|Performance",
      "title": "Short descriptive title",
      "description": "Clear explanation of the problem",
      "line_number": <integer or null>,
      "code_snippet": "the problematic code",
      "cwe_reference": "CWE-89 or null",
      "suggested_fix": "corrected code or approach",
      "confidence": <0.0 to 1.0>
    }
  ]
}

Priority rules:
P1 = Security vulnerabilities (injection, overflow, auth bypass, RCE)
P2 = Bugs causing incorrect behavior (NPE, logic error, race condition)
P3 = Bad practices (no error handling, resource leaks, magic numbers)
P4 = Style/readability (long methods, missing docs, naming)
P5 = Suggestions (minor perf, nice-to-haves)

Be specific. Use exact line numbers. Reference CWE IDs from the context when relevant.
"""

# ─── Agent ────────────────────────────────────────────

class CodeReviewAgent:

    def __init__(self):
        self.use_bedrock = os.getenv("USE_BEDROCK", "false").lower() == "true"

        if self.use_bedrock:
            import boto3
            self.bedrock = boto3.client(
                "bedrock-runtime",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
            self.model_id = os.getenv("BEDROCK_MODEL_ID", "global.anthropic.claude-sonnet-4-6")
            logger.info(f"Using Bedrock model: {self.model_id}")
        else:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY not set. Add it to backend/.env "
                    "or set USE_BEDROCK=true to use AWS Bedrock."
                )
            self.anthropic_client = anthropic.Anthropic(api_key=api_key)
            self.model_id = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
            logger.info(f"Using Anthropic API model: {self.model_id}")

        self.rag = RAGRetriever()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _call_claude(self, user_message: str) -> str:
        if self.use_bedrock:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 8192,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_message}]
            }
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
            result = json.loads(response["body"].read())
            return result["content"][0]["text"]
        else:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.anthropic_client.messages.create(
                    model=self.model_id,
                    max_tokens=8192,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_message}]
                )
            )
            return response.content[0].text

    async def review_code(self, code: str, file_name: str = "code.py",
                          language: Optional[str] = None) -> CodeReviewResult:
        lines = code.splitlines()
        total_lines = len(lines)

        if not language:
            ext_map = {".py": "Python", ".java": "Java", ".js": "JavaScript",
                       ".ts": "TypeScript", ".c": "C", ".cpp": "C++",
                       ".cs": "C#", ".go": "Go", ".rs": "Rust", ".rb": "Ruby"}
            suffix = "." + file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
            language = ext_map.get(suffix, "Unknown")

        logger.info("Running RAG retrieval...")
        chunks = self.rag.retrieve(
            f"Code review for {language}. File: {file_name}. Code:\n{code[:500]}", top_k=4
        )
        rag_context = self.rag.format_context_for_prompt(chunks)
        logger.info(f"Retrieved {len(chunks)} chunks from knowledge bases.")

        numbered = "\n".join(f"{i+1:4d} | {line}" for i, line in enumerate(lines))
        user_message = f"""Review this {language} code:

FILE: {file_name} ({total_lines} lines)

```{language.lower()}
{numbered}
```

{rag_context}

Respond with the JSON review."""

        logger.info("Calling Claude...")
        raw = await self._call_claude(user_message)
        return self._parse_response(raw, file_name, language, total_lines)

    async def review_file(self, file_path: str) -> CodeReviewResult:
        async with CodeReviewMCPClient() as mcp:
            content = await mcp.call_tool("read_file", {"file_path": file_path})
            language = await mcp.call_tool("detect_language", {"file_path": file_path})
        return await self.review_code(content, os.path.basename(file_path), language)

    def _parse_response(self, raw: str, file_name: str,
                        language: str, total_lines: int) -> CodeReviewResult:
        json_match = re.search(r"\{[\s\S]*\}", raw)
        if not json_match:
            logger.error("Non-JSON response from Claude")
            return CodeReviewResult(file_name=file_name, language=language,
                                    total_lines=total_lines,
                                    review_summary="Parse error.", overall_score=0)
        try:
            data = json.loads(json_match.group())
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            return CodeReviewResult(file_name=file_name, language=language,
                                    total_lines=total_lines,
                                    review_summary="Parse error.", overall_score=0)

        issues = [
            ReviewIssue(
                priority=i.get("priority", "P3"),
                category=i.get("category", "Quality"),
                title=i.get("title", ""),
                description=i.get("description", ""),
                line_number=i.get("line_number"),
                code_snippet=i.get("code_snippet", ""),
                cwe_reference=i.get("cwe_reference"),
                suggested_fix=i.get("suggested_fix", ""),
                confidence=float(i.get("confidence", 0.8)),
            )
            for i in data.get("issues", [])
        ]
        return CodeReviewResult(
            file_name=file_name, language=language, total_lines=total_lines,
            review_summary=data.get("review_summary", ""),
            overall_score=int(data.get("overall_score", 50)),
            issues=issues,
        )

    def to_dict(self, result: CodeReviewResult) -> dict:
        return asdict(result)
```

## 4.2 Create `scripts/test_agent.py`

```python
import asyncio, sys
sys.path.insert(0, ".")
from backend.agent.code_review_agent import CodeReviewAgent

SAMPLE_CODE = '''
import pickle, subprocess

def login(username, password):
    conn = get_db()
    query = "SELECT * FROM users WHERE name='" + username + "'"
    user = conn.execute(query).fetchone()
    if user and user["password"] == password:
        return True
    return False

def run_command(cmd):
    subprocess.call(cmd, shell=True)

def load_data(data):
    return pickle.loads(data)
'''

async def main():
    agent = CodeReviewAgent()
    result = await agent.review_code(SAMPLE_CODE, "login.py", "Python")
    print(f"\nScore: {result.overall_score}/100")
    print(f"Summary: {result.review_summary}")
    print(f"\nFound {len(result.issues)} issues:")
    for issue in result.issues:
        print(f"  [{issue.priority}] {issue.title} — {issue.cwe_reference or 'no CWE'}")

asyncio.run(main())
```

Run test:
```bash
python scripts/test_agent.py
```

---

# PHASE 5 — FastAPI Backend

## 5.1 Create `backend/api/main.py`

```python
"""
FastAPI backend for Code Review Agent.
Endpoints:
  GET  /health          — health check
  POST /review/code     — review pasted code
  POST /review/file     — review uploaded file
  GET  /report/{id}     — download HTML report
  WS   /ws/review       — streaming WebSocket review
"""
import asyncio, os, uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.agent.code_review_agent import CodeReviewAgent
from backend.reports.generator import ReportGenerator

app = FastAPI(title="Code Review Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CodeReviewAgent()
report_gen = ReportGenerator()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/code_uploads"))
REPORT_DIR = Path(os.getenv("REPORT_OUTPUT_DIR", "generated_reports"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

MAX_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
ALLOWED_EXT = {".py",".java",".js",".ts",".c",".cpp",".cs",".go",
               ".rs",".rb",".php",".swift",".kt",".sh",".sql"}

class CodeReviewRequest(BaseModel):
    code: str
    file_name: Optional[str] = "pasted_code.py"
    language: Optional[str] = None

@app.get("/health")
async def health():
    return {"status": "ok", "service": "code-review-agent"}

@app.post("/review/code")
async def review_pasted_code(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(400, "Code cannot be empty.")
    if len(request.code) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(413, f"Code too large. Max {MAX_SIZE_MB}MB.")

    review_id = str(uuid.uuid4())
    logger.info(f"[{review_id}] Reviewing pasted code: {request.file_name}")

    result = await agent.review_code(
        code=request.code,
        file_name=request.file_name or "pasted_code.py",
        language=request.language,
    )
    result_dict = agent.to_dict(result)
    report_gen.generate_html(result_dict, review_id, REPORT_DIR)

    return {"review_id": review_id, "result": result_dict,
            "report_url": f"/report/{review_id}.html"}

@app.post("/review/file")
async def review_uploaded_file(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported type: {suffix}. Allowed: {', '.join(ALLOWED_EXT)}")

    review_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{review_id}{suffix}"
    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(413, f"File too large. Max {MAX_SIZE_MB}MB.")

    save_path.write_bytes(content)
    logger.info(f"[{review_id}] Reviewing uploaded: {file.filename}")

    result = await agent.review_file(str(save_path))
    result.file_name = file.filename
    result_dict = agent.to_dict(result)
    report_gen.generate_html(result_dict, review_id, REPORT_DIR)

    return {"review_id": review_id, "result": result_dict,
            "report_url": f"/report/{review_id}.html"}

@app.get("/report/{filename}")
async def download_report(filename: str):
    path = REPORT_DIR / filename
    if not path.exists():
        raise HTTPException(404, "Report not found.")
    return FileResponse(path, media_type="text/html", filename=filename)

@app.websocket("/ws/review")
async def websocket_review(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        await websocket.send_json({"event": "started", "message": "Running analysis..."})
        result = await agent.review_code(
            code=data.get("code", ""),
            file_name=data.get("file_name", "code.py"),
            language=data.get("language"),
        )
        await websocket.send_json({"event": "completed", "result": agent.to_dict(result)})
    except Exception as e:
        logger.error(f"WS error: {e}")
        await websocket.send_json({"event": "error", "message": str(e)})
    finally:
        await websocket.close()
```

Start the API:
```bash
cd ~/Desktop/code-review-agent
source backend/.venv/bin/activate
uvicorn backend.api.main:app --reload --port 8000
```

Open: **http://localhost:8000/docs**

---

# PHASE 6 — Report Generator

## 6.1 Create `backend/reports/generator.py`

```python
"""Report Generator — converts CodeReviewResult dict into a styled HTML report."""

from pathlib import Path
from jinja2 import Environment, BaseLoader

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Code Review — {{ result.file_name }}</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f1f5f9;color:#1e293b;line-height:1.6}
  .wrap{max-width:960px;margin:40px auto;padding:0 20px 60px}
  header{background:linear-gradient(135deg,#1e293b,#0f172a);color:white;padding:32px;border-radius:12px;margin-bottom:20px}
  header h1{font-size:22px;font-weight:700;margin-bottom:4px}
  header .meta{color:#94a3b8;font-size:14px}
  .score-row{background:white;border-radius:12px;padding:28px 32px;margin-bottom:20px;display:flex;align-items:center;gap:28px;box-shadow:0 2px 8px rgba(0,0,0,.07)}
  .score-num{font-size:72px;font-weight:900;line-height:1;color:{{ score_color }}}
  .summary{color:#475569;font-size:15px;margin-top:8px;line-height:1.7}
  .stats{display:flex;gap:14px;margin-bottom:20px;flex-wrap:wrap}
  .stat{background:white;border-radius:10px;padding:16px 20px;flex:1;min-width:100px;text-align:center;box-shadow:0 1px 4px rgba(0,0,0,.06)}
  .stat .n{font-size:30px;font-weight:800}
  .stat .l{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.05em}
  .p1c{color:#ef4444}.p2c{color:#f97316}.p3c{color:#ca8a04}.p4c{color:#3b82f6}.p5c{color:#6b7280}
  h2{font-size:16px;font-weight:700;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
  .issue{background:white;border-radius:10px;padding:20px 24px;margin-bottom:12px;border-left:5px solid #e2e8f0;box-shadow:0 1px 4px rgba(0,0,0,.05)}
  .issue.P1{border-color:#ef4444}.issue.P2{border-color:#f97316}.issue.P3{border-color:#ca8a04}.issue.P4{border-color:#3b82f6}.issue.P5{border-color:#6b7280}
  .badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
  .badge{display:inline-block;padding:3px 10px;border-radius:5px;font-size:12px;font-weight:700;color:white}
  .bP1{background:#ef4444}.bP2{background:#f97316}.bP3{background:#ca8a04}.bP4{background:#3b82f6}.bP5{background:#6b7280}
  .bcat{background:#f1f5f9;color:#475569;font-weight:400}
  .bcwe{background:#fef3c7;color:#92400e;font-weight:600}
  .bline{background:#ede9fe;color:#5b21b6}
  .ititle{font-size:15px;font-weight:600;color:#1e293b;margin-bottom:6px}
  .idesc{color:#475569;font-size:14px;margin-bottom:10px}
  pre{background:#1e293b;color:#e2e8f0;padding:14px 16px;border-radius:7px;font-size:13px;overflow-x:auto;margin:10px 0;font-family:"Fira Code",monospace}
  .fix{background:#f0fdf4;border:1px solid #86efac;border-radius:7px;padding:12px 16px;margin-top:10px}
  .fix strong{color:#15803d;font-size:13px;display:block;margin-bottom:6px}
  .fix code{color:#166534;font-size:13px;white-space:pre-wrap;font-family:monospace}
  footer{text-align:center;color:#94a3b8;font-size:12px;margin-top:40px}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Code Review Report</h1>
    <div class="meta">
      File: <strong style="color:white">{{ result.file_name }}</strong> &nbsp;·&nbsp;
      Language: {{ result.language }} &nbsp;·&nbsp;
      {{ result.total_lines }} lines &nbsp;·&nbsp;
      ID: {{ review_id }}
    </div>
  </header>

  <div class="score-row">
    <div>
      <div class="score-num">{{ result.overall_score }}</div>
      <div style="color:#94a3b8;font-size:13px">/ 100</div>
    </div>
    <div>
      <div style="font-weight:700;font-size:17px;margin-bottom:6px">Overall Score</div>
      <div class="summary">{{ result.review_summary }}</div>
    </div>
  </div>

  {% set p1 = result.issues | selectattr('priority','equalto','P1') | list | length %}
  {% set p2 = result.issues | selectattr('priority','equalto','P2') | list | length %}
  {% set p3 = result.issues | selectattr('priority','equalto','P3') | list | length %}
  {% set p4 = result.issues | selectattr('priority','equalto','P4') | list | length %}
  {% set p5 = result.issues | selectattr('priority','equalto','P5') | list | length %}
  <div class="stats">
    <div class="stat"><div class="n p1c">{{ p1 }}</div><div class="l">P1 Critical</div></div>
    <div class="stat"><div class="n p2c">{{ p2 }}</div><div class="l">P2 High</div></div>
    <div class="stat"><div class="n p3c">{{ p3 }}</div><div class="l">P3 Medium</div></div>
    <div class="stat"><div class="n p4c">{{ p4 }}</div><div class="l">P4 Low</div></div>
    <div class="stat"><div class="n p5c">{{ p5 }}</div><div class="l">P5 Info</div></div>
    <div class="stat"><div class="n" style="color:#6366f1">{{ result.issues | length }}</div><div class="l">Total</div></div>
  </div>

  <h2>Issues Found ({{ result.issues | length }})</h2>
  {% for issue in result.issues %}
  <div class="issue {{ issue.priority }}">
    <div class="badges">
      <span class="badge b{{ issue.priority }}">{{ issue.priority }}</span>
      <span class="badge bcat">{{ issue.category }}</span>
      {% if issue.cwe_reference %}<span class="badge bcwe">{{ issue.cwe_reference }}</span>{% endif %}
      {% if issue.line_number %}<span class="badge bline">Line {{ issue.line_number }}</span>{% endif %}
    </div>
    <div class="ititle">{{ issue.title }}</div>
    <div class="idesc">{{ issue.description }}</div>
    {% if issue.code_snippet %}<pre>{{ issue.code_snippet }}</pre>{% endif %}
    {% if issue.suggested_fix %}
    <div class="fix">
      <strong>✅ Suggested Fix</strong>
      <code>{{ issue.suggested_fix }}</code>
    </div>
    {% endif %}
  </div>
  {% endfor %}

  <footer>Generated by Code Review Agent &nbsp;·&nbsp; {{ review_id }}</footer>
</div>
</body>
</html>"""


class ReportGenerator:
    def __init__(self):
        self.env = Environment(loader=BaseLoader())

    def generate_html(self, result: dict, review_id: str, output_dir: Path) -> Path:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        score = result.get("overall_score", 0)
        color = "#ef4444" if score < 40 else "#f97316" if score < 70 else "#22c55e"
        html = self.env.from_string(HTML_TEMPLATE).render(
            result=result, review_id=review_id, score_color=color
        )
        out = output_dir / f"{review_id}.html"
        out.write_text(html, encoding="utf-8")
        return out
```

---

# PHASE 7 — React + Vite Frontend (Beautiful UI)

## 7.1 Create the React App

```bash
cd ~/Desktop/code-review-agent
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install @monaco-editor/react axios react-dropzone
```

## 7.2 Replace `frontend/src/App.jsx` completely

```jsx
import { useState, useCallback } from 'react'
import Editor from '@monaco-editor/react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'

const API = 'http://localhost:8000'

const PRIORITIES = {
  P1: { color: '#ef4444', bg: '#fef2f2', border: '#fecaca', label: 'Critical' },
  P2: { color: '#f97316', bg: '#fff7ed', border: '#fed7aa', label: 'High' },
  P3: { color: '#ca8a04', bg: '#fefce8', border: '#fde68a', label: 'Medium' },
  P4: { color: '#3b82f6', bg: '#eff6ff', border: '#bfdbfe', label: 'Low' },
  P5: { color: '#6b7280', bg: '#f9fafb', border: '#e5e7eb', label: 'Info' },
}

const LANGUAGES = [
  { value: 'python', label: 'Python', ext: '.py' },
  { value: 'java', label: 'Java', ext: '.java' },
  { value: 'javascript', label: 'JavaScript', ext: '.js' },
  { value: 'typescript', label: 'TypeScript', ext: '.ts' },
  { value: 'c', label: 'C', ext: '.c' },
  { value: 'cpp', label: 'C++', ext: '.cpp' },
  { value: 'csharp', label: 'C#', ext: '.cs' },
  { value: 'go', label: 'Go', ext: '.go' },
  { value: 'rust', label: 'Rust', ext: '.rs' },
  { value: 'ruby', label: 'Ruby', ext: '.rb' },
  { value: 'shell', label: 'Shell', ext: '.sh' },
  { value: 'sql', label: 'SQL', ext: '.sql' },
]

const SAMPLE_CODE = `import pickle, subprocess

def login(username, password):
    conn = get_db()
    query = "SELECT * FROM users WHERE name='" + username + "'"
    user = conn.execute(query).fetchone()
    if user and user["password"] == password:
        return True
    return False

def run_command(cmd):
    subprocess.call(cmd, shell=True)

def load_data(data):
    return pickle.loads(data)
`

function ScoreRing({ score }) {
  const color = score < 40 ? '#ef4444' : score < 70 ? '#f97316' : '#22c55e'
  const label = score < 40 ? 'Critical Risk' : score < 70 ? 'Needs Work' : 'Good Quality'
  const r = 52, circ = 2 * Math.PI * r
  const offset = circ - (score / 100) * circ
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
      <svg width="124" height="124" viewBox="0 0 124 124">
        <circle cx="62" cy="62" r={r} fill="none" stroke="#e2e8f0" strokeWidth="10" />
        <circle cx="62" cy="62" r={r} fill="none" stroke={color} strokeWidth="10"
          strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
          transform="rotate(-90 62 62)" style={{ transition: 'stroke-dashoffset 1.2s ease' }} />
        <text x="62" y="57" textAnchor="middle" fontSize="26" fontWeight="900" fill={color}>{score}</text>
        <text x="62" y="74" textAnchor="middle" fontSize="11" fill="#94a3b8">/100</text>
      </svg>
      <div>
        <div style={{ fontSize: 18, fontWeight: 700, color, marginBottom: 4 }}>{label}</div>
        <div style={{ fontSize: 13, color: '#64748b' }}>Code Quality Score</div>
      </div>
    </div>
  )
}

function IssueCard({ issue, index }) {
  const [open, setOpen] = useState(index < 4)
  const p = PRIORITIES[issue.priority] || PRIORITIES.P5
  return (
    <div style={{
      borderRadius: 10, marginBottom: 10, overflow: 'hidden',
      border: `1px solid ${p.border}`, borderLeft: `5px solid ${p.color}`,
      background: 'white', boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    }}>
      <div onClick={() => setOpen(!open)} style={{
        padding: '13px 18px', cursor: 'pointer', display: 'flex',
        alignItems: 'center', gap: 8, background: open ? p.bg : 'white',
        transition: 'background 0.15s',
      }}>
        <span style={{ background: p.color, color: 'white', padding: '2px 9px', borderRadius: 5, fontSize: 11, fontWeight: 700, flexShrink: 0 }}>
          {issue.priority}
        </span>
        <span style={{ background: '#f1f5f9', color: '#475569', padding: '2px 9px', borderRadius: 5, fontSize: 11, flexShrink: 0 }}>
          {issue.category}
        </span>
        {issue.cwe_reference && (
          <span style={{ background: '#fef3c7', color: '#92400e', padding: '2px 9px', borderRadius: 5, fontSize: 11, fontWeight: 600, flexShrink: 0 }}>
            {issue.cwe_reference}
          </span>
        )}
        {issue.line_number && (
          <span style={{ color: '#94a3b8', fontSize: 11, flexShrink: 0 }}>Line {issue.line_number}</span>
        )}
        <span style={{ fontWeight: 600, fontSize: 14, color: '#1e293b', flex: 1, marginLeft: 2 }}>
          {issue.title}
        </span>
        <span style={{ color: '#cbd5e1', fontSize: 14, flexShrink: 0 }}>{open ? '▲' : '▼'}</span>
      </div>

      {open && (
        <div style={{ padding: '4px 18px 18px', borderTop: `1px solid ${p.border}` }}>
          <p style={{ color: '#475569', fontSize: 14, margin: '12px 0 10px' }}>{issue.description}</p>
          {issue.code_snippet && (
            <pre style={{
              background: '#0f172a', color: '#e2e8f0', padding: '13px 16px',
              borderRadius: 8, fontSize: 13, overflowX: 'auto', margin: '8px 0',
              fontFamily: "'Fira Code','Cascadia Code',monospace",
            }}>{issue.code_snippet}</pre>
          )}
          {issue.suggested_fix && (
            <div style={{ background: '#f0fdf4', border: '1px solid #86efac', borderRadius: 8, padding: '12px 16px', marginTop: 10 }}>
              <div style={{ color: '#15803d', fontWeight: 600, fontSize: 13, marginBottom: 6 }}>✅ Suggested Fix</div>
              <code style={{ color: '#166534', fontSize: 13, whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
                {issue.suggested_fix}
              </code>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [tab, setTab] = useState('editor')
  const [code, setCode] = useState(SAMPLE_CODE)
  const [fileName, setFileName] = useState('example.py')
  const [language, setLanguage] = useState('python')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [reportUrl, setReportUrl] = useState(null)
  const [reviewTime, setReviewTime] = useState(null)

  const onDrop = useCallback(async (files) => {
    const file = files[0]
    if (!file) return
    const text = await file.text()
    setCode(text)
    setFileName(file.name)
    const ext = '.' + file.name.split('.').pop().toLowerCase()
    const found = LANGUAGES.find(l => l.ext === ext)
    if (found) setLanguage(found.value)
    setTab('editor')
    setResult(null)
    setError(null)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/*': LANGUAGES.map(l => l.ext) },
    maxFiles: 1,
  })

  const reviewCode = async () => {
    if (!code.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    setReportUrl(null)
    const t0 = Date.now()
    try {
      const res = await axios.post(`${API}/review/code`, { code, file_name: fileName, language })
      setResult(res.data.result)
      setReportUrl(`${API}${res.data.report_url}`)
      setReviewTime(((Date.now() - t0) / 1000).toFixed(1))
    } catch (e) {
      setError(e.response?.data?.detail || e.message || 'Review failed')
    } finally {
      setLoading(false)
    }
  }

  const counts = result
    ? Object.fromEntries(['P1','P2','P3','P4','P5'].map(p => [p, result.issues.filter(i => i.priority === p).length]))
    : {}

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif', overflow: 'hidden' }}>

      {/* ── Header ─────────────────────────────────── */}
      <header style={{
        background: 'linear-gradient(135deg,#0f172a 0%,#1e293b 100%)',
        padding: '0 28px', height: 60, display: 'flex', alignItems: 'center',
        justifyContent: 'space-between', flexShrink: 0,
        boxShadow: '0 4px 20px rgba(0,0,0,0.4)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 9,
            background: 'linear-gradient(135deg,#3b82f6,#8b5cf6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 17,
          }}>🔍</div>
          <div>
            <div style={{ color: 'white', fontWeight: 700, fontSize: 15, lineHeight: 1.2 }}>Code Review Agent</div>
            <div style={{ color: '#64748b', fontSize: 11 }}>RAG · MCP · Claude AI · CWE/OWASP</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          {reviewTime && (
            <span style={{ color: '#64748b', fontSize: 12 }}>⏱ {reviewTime}s</span>
          )}
          <span style={{ background: 'rgba(99,102,241,0.2)', color: '#a5b4fc', padding: '4px 12px', borderRadius: 20, fontSize: 11, fontWeight: 500 }}>
            Claude Sonnet 4.6
          </span>
          <button onClick={reviewCode} disabled={loading || !code.trim()} style={{
            background: loading ? '#374151' : 'linear-gradient(135deg,#3b82f6,#6366f1)',
            color: 'white', border: 'none', borderRadius: 8,
            padding: '9px 22px', fontSize: 13, fontWeight: 600,
            cursor: loading ? 'not-allowed' : 'pointer',
            boxShadow: loading ? 'none' : '0 4px 14px rgba(99,102,241,0.45)',
            transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: 7,
          }}>
            <span style={loading ? { display: 'inline-block', animation: 'spin 1s linear infinite' } : {}}>
              {loading ? '⟳' : '🔍'}
            </span>
            {loading ? 'Analyzing...' : 'Review Code'}
          </button>
        </div>
      </header>

      {/* ── Main ───────────────────────────────────── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Left — Code Input */}
        <div style={{ width: '50%', display: 'flex', flexDirection: 'column', borderRight: '1px solid #e2e8f0', background: 'white' }}>

          {/* Toolbar */}
          <div style={{
            padding: '10px 14px', background: '#f8fafc', borderBottom: '1px solid #e2e8f0',
            display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', flexShrink: 0,
          }}>
            {/* Tab toggle */}
            <div style={{ display: 'flex', background: '#e2e8f0', borderRadius: 7, padding: 3 }}>
              {[['editor','✏️ Editor'],['upload','📁 Upload']].map(([id, lbl]) => (
                <button key={id} onClick={() => setTab(id)} style={{
                  padding: '5px 13px', borderRadius: 5, border: 'none',
                  background: tab === id ? 'white' : 'transparent',
                  color: tab === id ? '#1e293b' : '#64748b',
                  fontWeight: tab === id ? 600 : 400,
                  cursor: 'pointer', fontSize: 12,
                  boxShadow: tab === id ? '0 1px 3px rgba(0,0,0,0.1)' : 'none',
                  transition: 'all 0.15s',
                }}>{lbl}</button>
              ))}
            </div>

            <input value={fileName} onChange={e => setFileName(e.target.value)}
              placeholder="filename.py"
              style={{ flex: 1, minWidth: 110, padding: '6px 11px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12, outline: 'none', color: '#1e293b' }} />

            <select value={language} onChange={e => setLanguage(e.target.value)}
              style={{ padding: '6px 11px', border: '1px solid #e2e8f0', borderRadius: 6, fontSize: 12, color: '#1e293b', background: 'white', cursor: 'pointer', outline: 'none' }}>
              {LANGUAGES.map(l => <option key={l.value} value={l.value}>{l.label}</option>)}
            </select>
          </div>

          {/* Editor / Drop zone */}
          <div style={{ flex: 1, overflow: 'hidden' }}>
            {tab === 'editor' ? (
              <Editor height="100%" language={language} value={code}
                onChange={v => setCode(v || '')} theme="vs-dark"
                options={{
                  fontSize: 14, minimap: { enabled: false },
                  scrollBeyondLastLine: false, padding: { top: 14 },
                  fontFamily: "'Fira Code','Cascadia Code',monospace",
                  fontLigatures: true, lineNumbers: 'on',
                  renderLineHighlight: 'all', smoothScrolling: true,
                }} />
            ) : (
              <div {...getRootProps()} style={{
                height: '100%', display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center',
                background: isDragActive ? '#eff6ff' : '#f8fafc',
                border: `3px dashed ${isDragActive ? '#3b82f6' : '#e2e8f0'}`,
                cursor: 'pointer', transition: 'all 0.2s', padding: 40, textAlign: 'center',
              }}>
                <input {...getInputProps()} />
                <div style={{ fontSize: 52, marginBottom: 14 }}>{isDragActive ? '📂' : '📁'}</div>
                <div style={{ fontSize: 16, fontWeight: 600, color: '#1e293b', marginBottom: 6 }}>
                  {isDragActive ? 'Drop it here!' : 'Drag & drop a code file'}
                </div>
                <div style={{ color: '#94a3b8', fontSize: 13, marginBottom: 14 }}>or click to browse</div>
                <div style={{ background: '#e2e8f0', color: '#64748b', padding: '5px 16px', borderRadius: 20, fontSize: 11 }}>
                  .py .java .js .ts .c .cpp .cs .go .rs .rb .sh .sql
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right — Results */}
        <div style={{ width: '50%', overflow: 'auto', background: '#f1f5f9' }}>

          {/* Empty state */}
          {!loading && !result && !error && (
            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 40, textAlign: 'center' }}>
              <div style={{ fontSize: 60, marginBottom: 20 }}>🛡️</div>
              <div style={{ fontSize: 20, fontWeight: 700, color: '#1e293b', marginBottom: 10 }}>Ready to Review</div>
              <div style={{ color: '#64748b', fontSize: 14, maxWidth: 320, lineHeight: 1.7, marginBottom: 28 }}>
                A sample vulnerable Python file is already loaded.<br />
                Click <strong>Review Code</strong> to see it in action.
              </div>
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', justifyContent: 'center' }}>
                {[['🔍','CWE Detection'],['🛡️','OWASP Rules'],['🔧','Fix Suggestions'],['📊','P1–P5 Scoring'],['📝','HTML Report'],['⚡','RAG Context']].map(([icon,lbl]) => (
                  <div key={lbl} style={{ background: 'white', border: '1px solid #e2e8f0', borderRadius: 8, padding: '10px 16px', fontSize: 13, color: '#475569', display: 'flex', alignItems: 'center', gap: 6 }}>
                    {icon} {lbl}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', padding: 40 }}>
              <div style={{ fontSize: 52, marginBottom: 20, animation: 'spin 2s linear infinite', display: 'inline-block' }}>⚙️</div>
              <div style={{ fontSize: 17, fontWeight: 600, color: '#1e293b', marginBottom: 16 }}>Analyzing your code...</div>
              {['Querying CWE & OWASP knowledge bases via RAG','Embedding code and searching fix examples','Calling Claude AI for deep security analysis','Building structured P1–P5 review report'].map((s, i) => (
                <div key={i} style={{ color: '#64748b', fontSize: 13, margin: '3px 0', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ color: '#3b82f6' }}>▶</span> {s}
                </div>
              ))}
            </div>
          )}

          {/* Error */}
          {error && (
            <div style={{ padding: 24 }}>
              <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 10, padding: 20, color: '#dc2626' }}>
                <div style={{ fontWeight: 700, marginBottom: 8 }}>❌ Review Failed</div>
                <div style={{ fontSize: 14 }}>{error}</div>
              </div>
            </div>
          )}

          {/* Results */}
          {result && (
            <div style={{ padding: 22 }}>

              {/* Score card */}
              <div style={{ background: 'white', borderRadius: 14, padding: '24px 28px', marginBottom: 16, boxShadow: '0 2px 10px rgba(0,0,0,0.08)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
                  <ScoreRing score={result.overall_score} />
                  <div style={{ flex: 1, minWidth: 200 }}>
                    <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 3 }}>{result.file_name}</div>
                    <div style={{ color: '#64748b', fontSize: 13, marginBottom: 10 }}>
                      {result.language} · {result.total_lines} lines · {result.issues.length} issues
                      {reviewTime && <span> · {reviewTime}s</span>}
                    </div>
                    <div style={{ color: '#475569', fontSize: 14, lineHeight: 1.65 }}>{result.review_summary}</div>
                    {reportUrl && (
                      <a href={reportUrl} target="_blank" rel="noreferrer" style={{
                        display: 'inline-flex', alignItems: 'center', gap: 6,
                        marginTop: 14, background: '#eff6ff', color: '#3b82f6',
                        padding: '8px 16px', borderRadius: 8, fontSize: 13, fontWeight: 600,
                        textDecoration: 'none', border: '1px solid #bfdbfe',
                      }}>
                        📥 Download HTML Report
                      </a>
                    )}
                  </div>
                </div>
              </div>

              {/* Priority stats */}
              <div style={{ display: 'flex', gap: 10, marginBottom: 18, flexWrap: 'wrap' }}>
                {Object.entries(PRIORITIES).map(([p, cfg]) => (
                  <div key={p} style={{
                    background: 'white', borderRadius: 10, padding: '14px 16px',
                    flex: 1, minWidth: 80, textAlign: 'center',
                    boxShadow: '0 1px 4px rgba(0,0,0,0.06)',
                    borderTop: `3px solid ${cfg.color}`,
                  }}>
                    <div style={{ fontSize: 26, fontWeight: 800, color: cfg.color }}>{counts[p] || 0}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{p}</div>
                    <div style={{ fontSize: 11, color: '#94a3b8' }}>{cfg.label}</div>
                  </div>
                ))}
              </div>

              {/* Issue list */}
              <div style={{ fontWeight: 700, fontSize: 14, color: '#1e293b', marginBottom: 12 }}>
                Issues Found ({result.issues.length})
              </div>
              {result.issues.map((issue, i) => (
                <IssueCard key={i} issue={issue} index={i} />
              ))}
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg) } to { transform: rotate(360deg) } }
        * { box-sizing: border-box }
        ::-webkit-scrollbar { width: 6px; height: 6px }
        ::-webkit-scrollbar-track { background: #f1f5f9 }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px }
        ::-webkit-scrollbar-thumb:hover { background: #94a3b8 }
      `}</style>
    </div>
  )
}
```

## 7.3 Replace `frontend/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Code Review Agent</title>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body, #root { height: 100%; overflow: hidden; }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

## 7.4 Start the Frontend

```bash
cd ~/Desktop/code-review-agent/frontend
npm run dev
```

Open: **http://localhost:5173**

---

# PHASE 8 — AWS Bedrock

Your inference profile is already confirmed:
```
Inference Profile ID : global.anthropic.claude-sonnet-4-6
ARN                  : arn:aws:bedrock:us-east-1:...:inference-profile/global.anthropic.claude-sonnet-4-6
Status               : Active
Routes               : All Commercial AWS Regions
```

## 8.1 Update `backend/.env` for Bedrock

```bash
# Set these in backend/.env
USE_BEDROCK=true
BEDROCK_MODEL_ID=global.anthropic.claude-sonnet-4-6
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_real_key
AWS_SECRET_ACCESS_KEY=your_real_secret
```

## 8.2 Add Payment Method (Required for Bedrock)

```
AWS Console → your name (top right) → Billing and Cost Management
→ Payment methods → Add payment method → Add credit card → Save
→ Wait 2 minutes → retry
```

## 8.3 Test Bedrock Connection

```bash
cd ~/Desktop/code-review-agent
source backend/.venv/bin/activate
python scripts/test_agent.py
```

---

# Complete Execution — Run Everything

Open **3 terminal tabs** and run one command in each:

**Terminal 1 — Backend API:**
```bash
cd ~/Desktop/code-review-agent
source backend/.venv/bin/activate
uvicorn backend.api.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd ~/Desktop/code-review-agent/frontend
npm run dev
```

**Terminal 3 — (Optional) Test agent directly:**
```bash
cd ~/Desktop/code-review-agent
source backend/.venv/bin/activate
python scripts/test_agent.py
```

Open browser: **http://localhost:5173** ← Main UI
Open browser: **http://localhost:8000/docs** ← API Swagger

---

# Quick Reference

| Command | What it does |
|---------|-------------|
| `source backend/.venv/bin/activate` | Activate Python env (always first) |
| `pip install -r backend/requirements.txt` | Install Python packages |
| `python scripts/ingest_knowledge_bases.py` | Build ChromaDB from KB text files |
| `python scripts/test_mcp.py` | Verify MCP server tools |
| `python scripts/test_agent.py` | Run agent test (expects review output) |
| `uvicorn backend.api.main:app --reload --port 8000` | Start FastAPI |
| `cd frontend && npm run dev` | Start React UI |

| `.env` switch | Effect |
|---|---|
| `USE_BEDROCK=false` + `ANTHROPIC_API_KEY=...` | Use Anthropic API (works without AWS billing) |
| `USE_BEDROCK=true` + AWS keys | Use AWS Bedrock (`global.anthropic.claude-sonnet-4-6`) |

---

# All Fixes Applied in This Guide

| # | Fix | Why |
|---|-----|-----|
| 1 | `fastapi==0.115.5` | 0.115.0 conflicts with mcp on starlette version |
| 2 | `SentenceTransformerEmbeddingFunction` | No OpenAI API key needed for embeddings |
| 3 | `ANONYMIZED_TELEMETRY=False` in .env | Suppresses ChromaDB telemetry log noise |
| 4 | Empty collection guard in retriever | Prevents crash when past_reviews is empty |
| 5 | `global.anthropic.claude-sonnet-4-6` | Correct cross-region inference profile ID |
| 6 | `USE_BEDROCK` flag | Switch between Bedrock and Anthropic API in .env |
| 7 | All `__init__.py` files created | Python module imports work correctly |
| 8 | `weasyprint` removed | Heavy C deps not needed; Jinja2 HTML is sufficient |
| 9 | `boto3>=1.35.0` (not pinned exact) | Avoids version conflicts on upgrade |
| 10 | SAMPLE_CODE preloaded in React | Instant demo without user having to paste code |

---

*Guide v2.0 — All session fixes included | Python 3.11.15 | Node 24.11.0 | Claude Sonnet 4.6*

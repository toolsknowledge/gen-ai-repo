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
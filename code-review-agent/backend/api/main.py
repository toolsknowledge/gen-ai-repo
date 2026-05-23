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
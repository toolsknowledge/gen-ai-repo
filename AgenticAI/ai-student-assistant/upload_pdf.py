"""
upload_pdf.py
─────────────
CLI utility to ingest one or more PDF files into ChromaDB.

RUN THIS BEFORE asking questions about a document:

    python upload_pdf.py path/to/lecture_notes.pdf
    python upload_pdf.py data/pdfs/          # ingest entire directory
    python upload_pdf.py notes.pdf report.pdf   # multiple files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT THIS DOES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Loads the PDF(s) with PyMuPDF.
2. Splits text into 500-character overlapping chunks.
3. Embeds each chunk using the local sentence-transformers model.
4. Stores embeddings + text in ChromaDB at ./data/chroma_db.

After ingestion, main.py can answer questions about the PDF content.
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# Make sure project root is on the path when run directly
sys.path.insert(0, str(Path(__file__).parent))

from rag.pdf_loader import load_and_ingest_pdf, ingest_directory
from rag.document_store import document_store
from utils.logger import get_logger

console = Console()
log = get_logger(__name__)


def main():
    if len(sys.argv) < 2:
        console.print(Panel(
            "[bold]Usage:[/bold]\n"
            "  python upload_pdf.py [bold cyan]<path-to-pdf>[/bold cyan]\n"
            "  python upload_pdf.py [bold cyan]<directory>[/bold cyan]\n"
            "  python upload_pdf.py [bold cyan]file1.pdf file2.pdf ...[/bold cyan]",
            title="📄 PDF Uploader",
            border_style="blue",
        ))
        sys.exit(1)

    paths = [Path(p) for p in sys.argv[1:]]
    total_chunks = 0

    for path in paths:
        if path.is_dir():
            console.print(f"\n📁 Scanning directory: [cyan]{path}[/cyan]")
            results = ingest_directory(path)
            for filename, count in results.items():
                status = "✅" if count > 0 else "❌"
                console.print(f"  {status} {filename}: {count} chunks")
                total_chunks += count

        elif path.suffix.lower() == ".pdf":
            console.print(f"\n📄 Ingesting: [cyan]{path.name}[/cyan]")
            try:
                count = load_and_ingest_pdf(path)
                console.print(f"  ✅ {count} chunks stored")
                total_chunks += count
            except FileNotFoundError:
                console.print(f"  ❌ File not found: {path}")
            except Exception as exc:
                console.print(f"  ❌ Error: {exc}")

        else:
            console.print(f"  ⚠️  Skipping non-PDF file: {path}")

    # Summary
    db_size = document_store.collection_size()
    console.print(Panel(
        f"[bold green]Ingestion complete![/bold green]\n"
        f"Chunks added this session: [bold]{total_chunks}[/bold]\n"
        f"Total chunks in ChromaDB:  [bold]{db_size}[/bold]",
        title="✅ Done",
        border_style="green",
    ))


if __name__ == "__main__":
    main()

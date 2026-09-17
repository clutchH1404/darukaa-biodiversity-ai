import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.rag.vector_store import vector_store

def rebuild_index():
    print("Rebuilding ChromaDB vector index from processed chunks...")
    chunks_file = Path(settings.DATA_PROCESSED_DIR) / "knowledge_chunks.json"
    if not chunks_file.exists():
        print(f"Processed chunks not found at {chunks_file}. Run scripts/ingest_documents.py first.")
        return False

    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    vector_store.add_chunks(chunks)
    print(f"Successfully re-indexed {len(chunks)} chunks. Total in collection: {vector_store.count()}")
    return True

if __name__ == "__main__":
    rebuild_index()

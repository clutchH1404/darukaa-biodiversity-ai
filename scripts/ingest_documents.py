import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import settings
from app.rag.chunker import chunker
from app.rag.vector_store import vector_store
from app.services.db_service import db_service

def run_ingestion():
    print("=" * 60)
    print("DARUKAA.EARTH: SCIENTIFIC KNOWLEDGE INGESTION PIPELINE")
    print("=" * 60)

    seed_file = Path(settings.DATA_KNOWLEDGE_DIR) / "scientific_knowledge_seed.json"
    if not seed_file.exists():
        print(f"Error: Seed file {seed_file} does not exist.")
        return False

    with open(seed_file, "r", encoding="utf-8") as f:
        documents = json.load(f)

    print(f"Loaded {len(documents)} authoritative scientific documents.")

    all_chunks = []
    for doc in documents:
        # Register source in SQLite
        db_service.register_source(doc)

        # Chunk document
        doc_chunks = chunker.chunk_document(doc)
        all_chunks.extend(doc_chunks)
        print(f" -> Indexed [{doc['document_id']}] {doc['title'][:45]}... ({len(doc_chunks)} chunks)")

    # Save processed chunks to data/processed
    processed_path = Path(settings.DATA_PROCESSED_DIR) / "knowledge_chunks.json"
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
    print(f"\nSaved {len(all_chunks)} processed chunks to {processed_path}")

    # Upsert into ChromaDB vector store
    print(f"Upserting chunks into ChromaDB at {settings.CHROMA_PERSIST_DIR}...")
    vector_store.add_chunks(all_chunks)
    print(f"Vector store now contains {vector_store.count()} indexed chunks.")

    print("\nIngestion completed successfully.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_ingestion()

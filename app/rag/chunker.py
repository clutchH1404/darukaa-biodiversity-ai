import re
from typing import List, Dict, Any

class DocumentChunker:
    """
    Splits scientific documents into semantically coherent chunks
    while preserving all document metadata, domain labels, and citations.
    """

    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        # Split by paragraphs first
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks = []
        current_chunk = []
        current_length = 0

        for p in paragraphs:
            p_len = len(p.split())
            if current_length + p_len <= self.chunk_size:
                current_chunk.append(p)
                current_length += p_len
            else:
                if current_chunk:
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [p]
                current_length = p_len

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        if not chunks:
            chunks = [text]

        return chunks

    def chunk_document(self, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Takes a full KnowledgeDocument dictionary and returns chunk records.
        """
        raw_text = doc.get("text", "")
        text_chunks = self.split_text(raw_text)

        processed_chunks = []
        for idx, chunk_text in enumerate(text_chunks):
            chunk_id = f"{doc['document_id']}_c{idx+1}"
            processed_chunks.append({
                "chunk_id": chunk_id,
                "document_id": doc["document_id"],
                "title": doc["title"],
                "organization": doc["organization"],
                "publication_year": doc["publication_year"],
                "source_type": doc.get("source_type", "Scientific Assessment"),
                "environmental_domain": doc.get("environmental_domain", "Ecosystem"),
                "variables": doc.get("variables", []),
                "geographic_scope": doc.get("geographic_scope", "Global"),
                "text": chunk_text,
                "citation": doc["citation"],
                "url": doc["url"],
                "reliability_score": doc.get("reliability_score", 0.95)
            })

        return processed_chunks

chunker = DocumentChunker()

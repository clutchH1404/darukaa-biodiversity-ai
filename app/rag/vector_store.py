import os
import json
import chromadb
from typing import List, Dict, Any, Optional
from ..core.config import settings

class ChromaVectorStore:
    """
    ChromaDB-backed vector database for indexed environmental and biodiversity literature.
    """

    def __init__(self, persist_dir: Optional[str] = None):
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = "biodiversity_knowledge"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Add chunked documents to ChromaDB collection.
        """
        if not chunks:
            return

        ids = []
        documents = []
        metadatas = []

        for c in chunks:
            ids.append(c["chunk_id"])
            documents.append(c["text"])
            
            # Chroma metadata values must be str, int, float, or bool
            meta = {
                "document_id": c["document_id"],
                "title": c["title"],
                "organization": c["organization"],
                "publication_year": int(c["publication_year"]),
                "source_type": c.get("source_type", "Assessment"),
                "environmental_domain": c.get("environmental_domain", "General"),
                "variables_json": json.dumps(c.get("variables", [])),
                "geographic_scope": c.get("geographic_scope", "Global"),
                "citation": c["citation"],
                "url": c["url"],
                "reliability_score": float(c.get("reliability_score", 0.95))
            }
            metadatas.append(meta)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search(
        self,
        query: str,
        n_results: int = 5,
        domain_filter: Optional[str] = None,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs semantic vector retrieval against ChromaDB.
        """
        # Count available documents
        count = self.collection.count()
        if count == 0:
            return []

        actual_k = min(n_results, count)

        where = where_filter or {}
        if domain_filter and "environmental_domain" not in where:
            where["environmental_domain"] = domain_filter

        query_args = {
            "query_texts": [query],
            "n_results": actual_k
        }
        if where:
            query_args["where"] = where

        try:
            results = self.collection.query(**query_args)
        except Exception as e:
            # If where clause fails due to no match, retry without where
            query_args.pop("where", None)
            results = self.collection.query(**query_args)

        formatted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results.get("distances", [[0.5] * len(docs)])[0]
            ids = results["ids"][0]

            for i in range(len(docs)):
                dist = distances[i] if i < len(distances) else 0.5
                # Convert cosine distance to cosine similarity score [0, 1]
                similarity = max(0.0, min(1.0, 1.0 - (dist / 2.0)))
                
                meta = metas[i] if i < len(metas) else {}
                try:
                    vars_list = json.loads(meta.get("variables_json", "[]"))
                except Exception:
                    vars_list = []

                formatted_results.append({
                    "chunk_id": ids[i],
                    "document_id": meta.get("document_id", ""),
                    "title": meta.get("title", "Untitled Document"),
                    "organization": meta.get("organization", "Scientific Literature"),
                    "publication_year": meta.get("publication_year", 2021),
                    "environmental_domain": meta.get("environmental_domain", "General"),
                    "variables": vars_list,
                    "geographic_scope": meta.get("geographic_scope", "Global"),
                    "excerpt": docs[i],
                    "similarity_score": round(similarity, 4),
                    "citation": meta.get("citation", ""),
                    "url": meta.get("url", ""),
                    "reliability_score": meta.get("reliability_score", 0.95)
                })

        return formatted_results

    def count(self) -> int:
        return self.collection.count()

vector_store = ChromaVectorStore()

import re
from typing import List, Dict, Any

class SecurityGuard:
    """
    Guards against prompt injection and hallucinated scientific claims.
    """
    
    INJECTION_PATTERNS = [
        r"ignore (all )?previous instructions",
        r"disregard (all )?(system|prior) prompts",
        r"you are now a .* and not an environmental",
        r"forget your ethical guidelines",
        r"system override",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
    ]

    @classmethod
    def sanitize_user_input(cls, text: str) -> str:
        """
        Sanitize user queries and detect injection attempts.
        """
        if not text:
            return ""
        
        sanitized = text.strip()
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                # Neutralize injection attempt
                sanitized = re.sub(pattern, "[FILTERED_SECURITY_DIRECTIVE]", sanitized, flags=re.IGNORECASE)
        
        return sanitized

    @classmethod
    def wrap_rag_context_as_data(cls, document_texts: List[Dict[str, Any]]) -> str:
        """
        Wraps retrieved knowledge strictly as DATA inside protected delimiters
        to prevent indirect prompt injection from indexed content.
        """
        formatted = []
        for i, doc in enumerate(document_texts, 1):
            doc_id = doc.get("document_id", f"DOC-{i}")
            title = doc.get("title", "Untitled")
            text = doc.get("text", "").replace("```", "'''")
            formatted.append(
                f"<evidence_item id=\"{doc_id}\" title=\"{title}\">\n"
                f"{text}\n"
                f"</evidence_item>"
            )
        return "\n\n".join(formatted)

    @classmethod
    def verify_citation_grounding(cls, citation_source_id: str, valid_source_ids: List[str]) -> bool:
        """
        Ensures a cited document ID actually exists in the retrieved evidence set.
        """
        return citation_source_id in valid_source_ids

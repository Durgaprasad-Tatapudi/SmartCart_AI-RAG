import re

def sanitize_query(query: str) -> str:
    """Sanitize user search queries, limit length, strip dangerous characters."""
    if not query:
        return ""
    # Strip excessively long queries (max 500 chars)
    cleaned = query.strip()[:500]
    # Remove control characters
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned)
    return cleaned

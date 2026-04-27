import re

def normalize_query(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"[^a-z0-9\s]", "", q)
    return " ".join(sorted(q.split()))
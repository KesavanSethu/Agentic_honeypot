import re

KEYWORDS = [
    "blocked","urgent","verify","kyc","account","payment","transfer",
    "click","call","suspended","warning","final","now","immediately"
]

def is_scam(text: str) -> bool:
    t = text.lower()

    if any(k in t for k in KEYWORDS):
        return True

    if re.search(r"https?://", t):
        return True

    if re.search(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]{2,}", t):
        return True

    if re.search(r"(?:\+91[\s\-]?)?[6-9]\d{9}", t):
        return True

    if re.search(r"\b\d{9,18}\b", t) and any(word in t for word in ["transfer", "send", "pay", "deposit", "account"]):
        return True

    return False

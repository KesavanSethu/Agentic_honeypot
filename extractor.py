import re

def extract_intel(text: str):
    return {
        "upi": re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text),
        "links": re.findall(r"https?://\S+", text),
        "phones": re.findall(r"(?:\+91[\s\-]?)?[6-9]\d{9}", text),
        "bank_accounts": re.findall(r"\b\d{9,18}\b", text)
    }

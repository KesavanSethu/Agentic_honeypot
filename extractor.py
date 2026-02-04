import re

def extract_intel(text: str):
    phones = re.findall(r"(?:\+91[\s\-]?)?[6-9]\d{9}", text)
    upi = re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text)
    links = re.findall(r"https?://\S+", text)

    # First find all 9–18 digit numbers
    raw_accounts = re.findall(r"\b\d{9,18}\b", text)

    # REMOVE anything that is actually a phone number
    bank_accounts = [acc for acc in raw_accounts if acc not in phones]

    return {
        "upi": upi,
        "links": links,
        "phones": phones,
        "bank_accounts": bank_accounts
    }

def validate_extractions(extractions):
    """Keep only clean, meaningful fields"""

    clean = {}

    if extractions.get("upi"):
        clean["upi"] = extractions["upi"]

    if extractions.get("links"):
        clean["links"] = extractions["links"]

    if extractions.get("phones"):
        clean["phones"] = extractions["phones"]

    if extractions.get("bank_accounts"):
        clean["bank_accounts"] = extractions["bank_accounts"]

    return clean

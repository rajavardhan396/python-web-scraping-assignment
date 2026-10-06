import hashlib
import re

def _normalize(value):
    value = str(value or "").lower()
    value = re.sub(r"[^\w\s]", "", value)
    return " ".join(value.split())

def make_fingerprint(rec):
    if rec["source"] == "Books to Scrape":
        key = f'{rec["source"]} {rec.get("name_or_title")}'
    else:
        key = f'{rec["source"]} {rec.get("author")} {str(rec.get("name_or_title") or "")[:50]}'
    return hashlib.sha256(_normalize(key).encode("utf-8")).hexdigest()

def find_duplicates(records):
    seen, unique, duplicates = set(), [], []
    for rec in records:
        fp = make_fingerprint(rec)
        if fp in seen:
            duplicates.append(rec)
        else:
            seen.add(fp)
            unique.append(rec)
    return unique, duplicates

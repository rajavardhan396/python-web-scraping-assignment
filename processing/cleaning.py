import re
from urllib.parse import urlparse

RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

def clean_text(value):
    if value is None:
        return None
    value = value.replace("\xa0", " ")
    value = " ".join(value.split())
    return value or None

def strip_quotes(value):
    value = clean_text(value)
    if not value:
        return value
    return value.strip("“”\"'")

def clean_price(raw):
    if raw is None or raw == "":
        return None
    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", str(raw))
    return float(match.group().replace(",", "")) if match else None

def clean_rating(raw):
    for word in str(raw or "").lower().split():
        if word in RATING_MAP:
            return RATING_MAP[word]
    return None

def clean_tags(tags):
    if not tags:
        return None
    cleaned = sorted({clean_text(str(tag)).lower() for tag in tags if clean_text(str(tag))})
    return ";".join(cleaned) if cleaned else None

def normalize_url(url):
    if not url:
        return None
    url = str(url).strip()
    parsed = urlparse(url)
    return url if parsed.scheme in ("http", "https") and parsed.netloc else None

def clean_record(raw, scraped_at):
    rec = dict(raw)
    rec["name_or_title"] = strip_quotes(rec.get("name_or_title"))
    rec["source"] = clean_text(rec.get("source"))
    rec["source_url"] = normalize_url(rec.get("source_url"))
    rec["category"] = clean_text(rec.get("category"))
    rec["price"] = clean_price(rec.get("price"))
    rec["rating"] = clean_rating(rec.get("rating"))
    rec["author"] = clean_text(rec.get("author"))
    rec["tags"] = clean_tags(rec.get("tags"))
    rec["description"] = clean_text(rec.get("description"))
    rec["availability"] = clean_text(rec.get("availability"))
    rec["scraped_at"] = scraped_at
    return rec

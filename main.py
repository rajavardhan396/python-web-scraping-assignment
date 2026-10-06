import csv
import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import find_duplicates

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
LOGS = ROOT / "logs"
OUTPUT.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)
logger.handlers.clear()
fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler = logging.FileHandler(LOGS / "scraper.log", encoding="utf-8")
console_handler = logging.StreamHandler()
file_handler.setFormatter(fmt)
console_handler.setFormatter(fmt)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

COLUMNS = [
    "source", "source_url", "name_or_title", "category", "price", "rating",
    "author", "tags", "description", "availability", "scraped_at"
]

def process_source(name, raw_records, timestamp, report):
    report["sources"][name]["raw"] = len(raw_records)
    cleaned, rejected = [], Counter()
    for raw in raw_records:
        rec = clean_record(raw, timestamp)
        problems = validate_record(rec)
        if problems:
            for reason in problems:
                rejected[reason] += 1
            logger.warning("Rejected %s record %r: %s", name, rec.get("name_or_title"), problems)
            continue
        cleaned.append(rec)
    report["sources"][name]["cleaned"] = len(cleaned)
    report["sources"][name]["rejected"] = dict(rejected)
    return cleaned

def write_csv(records, path):
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for rec in records:
            writer.writerow({c: rec.get(c) for c in COLUMNS})

def main():
    start = datetime.now(timezone.utc)
    logger.info("Starting scraping assignment pipeline")
    report = {
        "started_at": start.isoformat(),
        "sources": {
            "Books to Scrape": {"raw": 0, "cleaned": 0, "rejected": {}},
            "Quotes to Scrape": {"raw": 0, "cleaned": 0, "rejected": {}},
        },
    }
    all_cleaned = []

    sources = [
        ("Books to Scrape", BooksScraper()),
        ("Quotes to Scrape", QuotesScraper()),
    ]

    for name, scraper in sources:
        try:
            raw = scraper.scrape()
            all_cleaned.extend(process_source(name, raw, start.isoformat(), report))
        except Exception as exc:
            logger.exception("Source %s failed unexpectedly: %s", name, exc)

    unique, duplicates = find_duplicates(all_cleaned)
    report["duplicates_found"] = len(duplicates)
    report["final_record_count"] = len(unique)
    report["raw_total"] = sum(v["raw"] for v in report["sources"].values())
    report["cleaned_total"] = sum(v["cleaned"] for v in report["sources"].values())
    report["ended_at"] = datetime.now(timezone.utc).isoformat()
    report["duration_seconds"] = round(time.time() - start.timestamp(), 2)

    write_csv(unique, OUTPUT / "final_dataset.csv")
    (OUTPUT / "summary_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Wrote %s", OUTPUT / "final_dataset.csv")
    logger.info("Wrote %s", OUTPUT / "summary_report.json")
    logger.info("Pipeline complete: %d final records, %d duplicates", len(unique), len(duplicates))

if __name__ == "__main__":
    main()

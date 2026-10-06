# Multi-Source Web Scraping & Data Consolidation

## Overview
This project implements the Realisieren Technologies Python web-scraping assignment. It collects public data from **Books to Scrape** and **Quotes to Scrape**, cleans and validates the records, detects duplicates, consolidates both sources into one schema, and writes a CSV plus JSON summary and execution log.

The required ETL flow is:

`Scrape -> Clean -> Validate -> Deduplicate -> Consolidate -> Save`

The assignment requires following each site's `next` link rather than hard-coding page numbers, preserving source URLs, handling missing fields, logging failures, and producing reproducible outputs.

## Python version
Python 3.10–3.12.

## Setup
Windows:
```powershell
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

The generated files are:
- `output/final_dataset.csv`
- `output/summary_report.json`
- `logs/scraper.log`

## Source exploration
### Books to Scrape
- Record selector: `article.product_pod`
- Title/link: `h3 > a`, with the full title in the `title` attribute
- Price: `p.price_color`
- Rating: class on `p.star-rating`
- Availability: `p.instock.availability`
- Pagination: `li.next > a`

### Quotes to Scrape
- Record selector: `div.quote`
- Quote text: `span.text`
- Author: `small.author`
- Tags: `a.tag`
- Author link: `a[href^="/author/"]`
- Pagination: `li.next > a`

Pagination is dynamic: after every successful page, the scraper reads `li.next > a`, resolves the relative URL with `urljoin`, and continues until the next link is absent.

## Data model
The consolidated CSV uses:
`source, source_url, name_or_title, category, price, rating, author, tags, description, availability, scraped_at`

Fields that do not apply to a source remain empty/NULL rather than receiving invented values. Book category and description are intentionally left empty because collecting them would require an additional request per book detail page; the assignment explicitly permits this limitation.

For Quotes, `source_url` is the page URL where the quote appeared. Tags are lowercased, deduplicated, sorted, and joined with `;`.

## Cleaning
- Collapse whitespace and non-breaking spaces.
- Remove surrounding curly/straight quotation marks from quote text.
- Convert currency text such as `£51.77` to `51.77`.
- Convert star-rating words such as `Three` to integer `3`.
- Normalize tags to lowercase, sorted, semicolon-separated text.
- Validate/normalize URLs so they have an HTTP(S) scheme.

Cleaning functions are isolated from network code so they can be unit-tested without internet access.

## Validation
A record is rejected when:
- its source is not one of the two allowed sources;
- its name/title is missing;
- its source URL is not an HTTP(S) URL;
- its price is present but not a non-negative number;
- its rating is present but not an integer from 1–5;
- a quote has no author.

Rejected records are counted by reason and logged as warnings.

## Deduplication
Duplicates are removed rather than flagged. A normalized fingerprint is hashed with SHA-256.

- Books: source + title.
- Quotes: source + author + first 50 characters of quote text.

Normalization lowercases text, removes punctuation, and collapses whitespace. Therefore capitalization and spacing differences do not create separate records.

## Error handling and reliability
The shared HTTP helper:
- uses a `requests.Session`;
- sends a descriptive User-Agent;
- uses a timeout;
- retries temporary HTTP failures (429, 500, 502, 503, 504) with backoff;
- pauses approximately 0.5 seconds between requests.

A failed page is logged and stops only that source. The other source still runs. Missing HTML fields are checked before access, and malformed individual records are skipped without terminating the whole pipeline.

## Tests
Run:
```bash
pytest -q
```

Tests cover text/price/rating/tag cleaning, URL normalization, validation, and duplicate detection.

## Outputs
`final_dataset.csv` contains one row per valid, unique record from both sources. `summary_report.json` records raw and cleaned counts per source, validation rejection reasons, duplicate count, final count, and execution timing. `logs/scraper.log` records requests, page progress, warnings, errors, and completion.

## Assumptions and limitations
1. Only the two public practice sites are scraped.
2. Book category and description are left empty to avoid approximately 1,000 additional detail-page requests; no values are guessed.
3. Quotes use the page URL as `source_url`.
4. The pipeline is intended as an educational take-home solution rather than a production crawler.
5. Network availability can affect live output; a failed source is isolated and logged.

## AI usage
AI assistance was used for initial project scaffolding, reviewing selectors, designing cleaning/validation/deduplication functions, generating unit-test ideas, and improving documentation. The final code was reviewed and tested locally with `pytest` and a complete pipeline run. See `AI_USAGE.md` for the required disclosure.

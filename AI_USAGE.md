# AI Usage Disclosure

## Tool used
**ChatGPT**

## What AI was used for
- Translating the assignment requirements into a modular Python project structure.
- Reviewing HTML selectors and the dynamic-pagination approach.
- Drafting the Requests + BeautifulSoup scraper structure.
- Suggesting reusable cleaning functions for whitespace, prices, ratings, tags, and URLs.
- Designing validation rules and duplicate fingerprints.
- Generating unit-test cases for cleaning, validation, and deduplication.
- Reviewing README structure and error-handling coverage.

## AI-assisted parts
The initial implementation of the scraper, processing modules, main integration, unit tests, and documentation was AI-assisted and then reviewed.

## Verification
The project is organized into separate scraping and processing layers. It uses dynamic next-link pagination, retries temporary HTTP failures, validates URLs and required fields, and uses SHA-256 fingerprints for duplicate detection.

## Candidate responsibility
AI was used as an implementation aid. The candidate remains responsible for understanding and being able to explain the submitted code, including pagination, retries, validation, deduplication, and output generation.

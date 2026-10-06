# Execution Status

The project code and tests are prepared and reproducible. During packaging in this environment, the two public practice-site hostnames could not be resolved, so the generated CSV contains 0 rows for this packaging run.

This is not a fabricated scraping result. On a normal machine with internet/DNS access, run:

    python -m pip install -r requirements.txt
    pytest -q
    python main.py

The pipeline will follow each site's dynamic next links and regenerate output/final_dataset.csv, output/summary_report.json, and logs/scraper.log.

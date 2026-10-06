import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class QuotesScraper(BaseScraper):
    START_URL = "https://quotes.toscrape.com/"

    def parse_page(self, soup, page_url):
        records = []
        for quote in soup.select("div.quote"):
            try:
                text = quote.select_one("span.text")
                author = quote.select_one("small.author")
                author_link = quote.select_one('a[href^="/author/"]')
                tags = [a.get_text(" ", strip=True) for a in quote.select("a.tag")]
                if not text or not author:
                    raise ValueError("missing quote text/author")
                records.append({
                    "source": "Quotes to Scrape",
                    "source_url": page_url,
                    "name_or_title": text.get_text(" ", strip=True),
                    "category": "Quotes",
                    "price": None,
                    "rating": None,
                    "author": author.get_text(" ", strip=True),
                    "tags": tags,
                    "description": None,
                    "availability": None,
                    "scraped_at": None,
                    "author_url": urljoin(page_url, author_link["href"]) if author_link else None,
                })
            except Exception as exc:
                logger.warning("Skipping malformed quote record on %s: %s", page_url, exc)
        return records

    def scrape(self):
        url = self.START_URL
        records, page = [], 1
        while url:
            logger.info("Quotes page %d: %s", page, url)
            response = self.get(url)
            if response is None:
                logger.error("Stopping Quotes source after failed page %s", url)
                break
            soup = BeautifulSoup(response.text, "lxml")
            records.extend(self.parse_page(soup, url))
            next_link = soup.select_one("li.next > a")
            url = urljoin(url, next_link["href"]) if next_link and next_link.get("href") else None
            page += 1
        logger.info("Quotes scraping complete: %d records", len(records))
        return records

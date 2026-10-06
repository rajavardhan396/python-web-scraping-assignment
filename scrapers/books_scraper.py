import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class BooksScraper(BaseScraper):
    START_URL = "https://books.toscrape.com/"

    def parse_page(self, soup, page_url):
        records = []
        for book in soup.select("article.product_pod"):
            try:
                title = book.select_one("h3 > a")
                price = book.select_one("p.price_color")
                rating = book.select_one("p.star-rating")
                availability = book.select_one("p.instock.availability")
                if not title or not price or not rating:
                    raise ValueError("missing required book fields")
                records.append({
                    "source": "Books to Scrape",
                    "source_url": page_url,
                    "name_or_title": title.get("title") or title.get_text(" ", strip=True),
                    "category": None,
                    "price": price.get_text(" ", strip=True),
                    "rating": " ".join(rating.get("class", [])),
                    "author": None,
                    "tags": None,
                    "description": None,
                    "availability": availability.get_text(" ", strip=True) if availability else None,
                    "scraped_at": None,
                })
            except Exception as exc:
                logger.warning("Skipping malformed book record on %s: %s", page_url, exc)
        return records

    def scrape(self):
        url = self.START_URL
        records, page = [], 1
        while url:
            logger.info("Books page %d: %s", page, url)
            response = self.get(url)
            if response is None:
                logger.error("Stopping Books source after failed page %s", url)
                break
            soup = BeautifulSoup(response.text, "lxml")
            records.extend(self.parse_page(soup, url))
            next_link = soup.select_one("li.next > a")
            url = urljoin(url, next_link["href"]) if next_link and next_link.get("href") else None
            page += 1
        logger.info("Books scraping complete: %d records", len(records))
        return records

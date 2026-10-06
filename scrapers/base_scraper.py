import logging
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class BaseScraper:
    TIMEOUT = 20

    def __init__(self):
        retry = Retry(
            total=3,
            backoff_factor=0.7,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
            raise_on_status=False,
        )
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Realisieren-Tech-Assignment-Scraper/1.0 (+educational)"
        })
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def get(self, url):
        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            time.sleep(0.5)
            return response
        except requests.RequestException as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return None

"""
Run this on your own machine (not in a sandboxed/no-network
environment) to test Scraper against the real, live category page.

Usage:
    python tests/test_live_scrape.py
"""

from core.scraper import Scraper
from config import settings
from .mock_server import run_server

TARGET_URL = "http://localhost:8765" # settings.BASE_URL 


def main():
    scraper = Scraper()

    html = scraper.fetch_page(TARGET_URL)

    if html is None:
        print("FAILED: could not fetch the page after all retries. Check the logs above.")
        return

    print(f"SUCCESS: fetched {len(html):,} characters of HTML.")
    print("First 300 characters:")
    print(html[:300])

    scraper.close()


if __name__ == "__main__":
    run_server()
    main()
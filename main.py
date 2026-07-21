from core.scraper import Scraper
import json

from config.logger import get_logger
from core.parser import NeweggParser

# scrap_obj = Scraper()

# #raw_html = scrap_obj.fetch_url("https://www.homehardware.ca/en/173cc-2-in-1-grasscycler-gas-lawn-mower-21/p/5124070?")

# # raw_html = scrap_obj.fetch_url("https://www.homehardware.ca/en/search?query=coffee+table")

# raw_html = scrap_obj.fetch_page("https://www.newegg.ca/Cell-Phones/Category/ID-450")

# with open("raw.json", "w") as f:
#     json.dump(raw_html, f)



logger = get_logger(__name__)


# Pagenation logic
def scrape_category(base_url: str, num_pages: int, scraper: Scraper, parser: NeweggParser) -> list[dict]:
    """
    Scrape the first `num_pages` of a Newegg category listing and
    return one combined list of product dicts.
    """
    all_products = []

    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}?Page={page_num}"
        html = scraper.fetch_page(page_url)

        if html is None:
            # fetch_page already retried internally and gave up —
            # log it and move to the next page rather than aborting
            # the whole run over one bad page.
            logger.warning("scrape_category: could not fetch page %d, skipping", page_num)
            continue

        products = parser.parse_product_list(html)

        if not products:
            # Two possibilities: this page genuinely has no products
            # (you've gone past the last real page), or parsing
            # failed silently. Either way, stopping here is safer
            # than continuing to request pages that don't exist.
            logger.info("scrape_category: page %d returned no products, stopping", page_num)
            break

        all_products.extend(products)

    logger.info("scrape_category: collected %d products across %d pages",
                len(all_products), page_num)
    return all_products
from core.scraper import Scraper
import json

scrap_obj = Scraper()

#raw_html = scrap_obj.fetch_url("https://www.homehardware.ca/en/173cc-2-in-1-grasscycler-gas-lawn-mower-21/p/5124070?")

# raw_html = scrap_obj.fetch_url("https://www.homehardware.ca/en/search?query=coffee+table")

raw_html = scrap_obj.fetch_page("https://www.newegg.ca/Cell-Phones/Category/ID-450")

with open("raw.json", "w") as f:
    json.dump(raw_html, f)
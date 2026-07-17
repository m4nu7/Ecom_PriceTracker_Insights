import json
from core.parser import NeweggParser

with open("raw.json", "r") as f:
    html = json.load(f)



newegg_parser = NeweggParser()

products = newegg_parser.parse_product_list(html)

print(products)


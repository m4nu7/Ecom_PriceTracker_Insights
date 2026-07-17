"""
Parser base class + site-specific subclasses

The base class defines the interface every site parser must 
implement. Each site (Newegg first, others added in Phase 9)
gets its own subclass that knows that site's HTML structure —
callers never need site-specific if/else logic.
"""
import re

from abc import ABC, abstractmethod
from typing import Optional, List

from bs4 import BeautifulSoup

from config.logger import get_logger


logger = get_logger(__name__)


class Parser(ABC):
    """
    Defines the contract every site-specific parser must follow.
    Scraper.fetch_page() hands raw HTML to these methods.
    """

    # @abstractmethod
    # def parse_price(self, html: str) -> Optional[float]:
    #     """Extract the current price from a product page's HTML."""
    #     raise NotImplementedError

    # @abstractmethod
    # def parse_name(self, html: str) -> Optional[str]:
    #     """Extract the product name/title from a product page's HTML."""
    #     raise NotImplementedError
    
    # @abstractmethod
    # def parse_in_stock(self, html: str) -> Optional[bool]:
    #     """ Determine whether the product is in stock"""
    #     raise NotImplementedError
    
    @abstractmethod
    def parse_product_list(self, html: str) -> List[dict]:
        """
        Extract every product on a category/listing page in one pass.
 
        Returns a list of dicts, each shaped like:
            {"name": str, "price": Optional[float], "in_stock": Optional[bool], "url": str}
 
        A single unparseable product on the page should be skipped
        (with a logged warning), not allowed to abort the whole page.
        """

        raise NotImplementedError
        
    

class NeweggParser(Parser):
    """
    Parser for Newegg product pages.
 
    Note ON SELECTORS: Newegg splits the displayed price across
    multiple elements — a whole-dollar figure (often bolded) and
    a cents figure (often a <sup>), inside a shared price
    container (commonly class "price-current"). The selectors
    below reflect that known layout, but Newegg (like any site)
    changes markup over time, so confirm current class names
    with browser dev tools before relying on this in production.
    Each method fails safe: returns None and logs a warning
    rather than raising, so one bad page doesn't crash a batch
    scrape (see Scraper/ThreadManager).
    """
     

    # def parse_price(self, html: str) -> Optional[float]:
    #     soup = BeautifulSoup(html, "html.parser")


    #     price_container = soup.select_one("price-current")
    #     if price_container is None:
    #         logger.warning("parse_price : no '.price-current' container found")
    #         return None
        

    #     # Dollars is usually the bolded figure, cents a superscript.
    #     dollars_tag = price_container.select_one("strong")
    #     cents_tag = price_container.select_one("sup")


    #     if dollars_tag is None:
    #         logger.warning("parse_price : o dollar amount found inside price container")
    #         return None
        

    #     dollars_text = dollars_tag.get_text(strip=True).replace(",", "")
    #     cents_text = cents_tag.get_text(strip=True).lstrip(".") if cents_tag else "00"


    #     try :
    #         return float(f"{dollars_text}.{cents_text}")
    #     except ValueError :
    #         logger.warning("parse_price: could not convert '%s.%s' to float", dollars_text, cents_text)
    #         return None
        



    # def parse_name(self, html: str) -> Optional[str]:
    #     soup = BeautifulSoup(html, "html.parser")
    #     title_tag = soup.select_one("a.item-title")
    #     if title_tag is None:
    #         logger.warning("parse_name: no '.item-title' container found")
    #         return None
        
    #     return title_tag.get_text(strip=True)
    


    
    # def parse_in_stock(self, html: str) -> Optional[bool]:
    #     soup = BeautifulSoup(html, "html.parser")

    #     # Two independent signals: an explicit "OUT OF STOCK" label,
    #     # or the presence/absence of a working "Add to cart" button.

    #     out_of_stock_text = soup.find(string=re.compile(r"out of stock", re.IGNORECASE))
    #     if out_of_stock_text:
    #         return False
        
    #     add_To_cart_button = soup.select_one("div.item-button-area button.btn-primary") or soup.find(
    #         "button", string=re.compile(r"add to cart", re.IGNORECASE)
    #     )
        

    #     if add_To_cart_button is not None:
    #         return True
        
    #     logger.warning("parse_in_stock: could not determine stock status")
    #     return None
        
        
        
    def parse_product_list(self, html: str) -> List[dict]:
        soup = BeautifulSoup(html, "html.parser")


        # Each product on a Newegg category page sits inside its own
        # container — commonly class "item-cell". We loop over every
        # one of these independently.

        product_cells = soup.select(".item-cell")

        if not product_cells:
            logger.warning("parse_product_list: no '.item-cell' elements found on page")
            return []
        
        products = []

        for cell in product_cells:
            try:
                product = self._parse_single_cell(cell)
                
                if product is not None:
                    products.append(product)

            except Exception as e:
                # A single malformed product block should never take
                # down the whole listing scrape.
                logger.warning(f"parse_product_list: skipping one product due to error: {e}")
                continue
        

        logger.info("parse_product_list: parsed %d/%d product cells successfully",
                    len(products), len(product_cells))


        return products





    def _parse_single_cell(self, cell : BeautifulSoup) -> Optional[dict]:
        """
        Parse one product "cell" (a single item on the listing page)
        into a dict. Returns None if this cell doesn't look like a
        real product (e.g. an ad slot with the same wrapper class).
        """


        # Name + URL usually live together on the same <a> tag.
        title_tag = cell.select_one("a.item-title")
        if title_tag is None:
            return None
        

        name = title_tag.get_text(strip=True)
        url =  title_tag.get("href")


        if not name or not url:
            return None
        
        # Price: dollars is usually the bolded figure, cents a
        # superscript, both inside a ".price-current" container.
        price = None
        price_container = cell.select_one(".price-current")

        dollars_tag = price_container.select_one("strong")
        cents_tag = price_container.select_one("sup")
        

        dollars_text = dollars_tag.get_text(strip=True).replace(",", "")
        cents_text = cents_tag.get_text(strip=True).lstrip(".") if cents_tag else "00"


        try :
            price = float(f"{dollars_text}.{cents_text}")
        except ValueError :
            price = None

        

        # Stock: two independent signals, checked in order —
        # explicit negative text ("out of stock" / "auto notify"),
        # or the presence of a working add-to-cart control.

        in_stock = None
        negative_text = cell.find(string=re.compile(r"out of stock|auto notify", re.IGNORECASE))

        if negative_text:
            in_stock = False
        else:
            add_to_cart = (
                cell.select_one(".btn-primary")
                or cell.find(["a", "button"], string=re.compile(r"add to cart", re.IGNORECASE))
                )
            
            if add_to_cart is not None:
                in_stock = True

        
        return {
            "name": name,
            "price": price,
            "in_stock": in_stock,
            "url": url,
        }
 





# Future site parsers (Phase 9) get added the same way, e.g.:
#
# class WalmartParser(Parser):
#     def parse_product_list(self, html): ...
 
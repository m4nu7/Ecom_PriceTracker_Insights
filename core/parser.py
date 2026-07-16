"""
Parser base class + site-specific subclasses

The base class defines the interface every site parser must 
implement. Each site (Newegg first, others added in Phase 9)
gets its own subclass that knows that site's HTML structure —
callers never need site-specific if/else logic.
"""

from abc import ABC, abstractmethod
from typing import Optional


class Parser(ABC):
    """
    Defines the contract every site-specific parser must follow.
    Scraper.fetch_page() hands raw HTML to these methods.
    """

    @abstractmethod
    def parse_price(self, html: str) -> Optional[float]:
        """Extract the current price from a product page's HTML."""
        raise NotImplementedError

    @abstractmethod
    def parse_name(self, html: str) -> Optional[str]:
        """Extract the product name/title from a product page's HTML."""
        raise NotImplementedError
    
    @abstractmethod
    def parse_in_stock(self, html: str) -> Optional[bool]:
        """ Determine whether the product is in stock"""
        raise NotImplementedError
    

class NeweggParser(Parser):
    """
    Parser for Newegg Product page

    Extracts price, name and stock status
    """

    def parse_price(self, html: str) -> Optional[float]:
        raise NotImplementedError

    def parse_name(self, html: str) -> Optional[str]:
        raise NotImplementedError
    
    def parse_in_stock(self, html: str) -> Optional[bool]:
        raise NotImplementedError


# Future site parsers (Phase 9) get added the same way, e.g.:
#
# class WalmartParser(Parser):
#     def parse_price(self, html): ...
#     def parse_name(self, html): ...
#     def parse_in_stock(self, html): ...

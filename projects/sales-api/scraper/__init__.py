"""Scraper module"""
from .kupi import scrape_shop, scrape_all_shops
from .fuzzy import fuzzy_match, normalize_product_name

__all__ = ["scrape_shop", "scrape_all_shops", "fuzzy_match", "normalize_product_name"]

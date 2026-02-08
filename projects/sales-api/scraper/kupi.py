"""Kupi.cz scraper (migrated from check-sales-improved.py)"""
import re
import asyncio
from typing import List, Dict, Optional
import httpx
from bs4 import BeautifulSoup

SHOPS = ["lidl", "penny-market", "billa", "kaufland"]
BASE_URL = "https://www.kupi.cz"

async def fetch_shop_products(shop: str) -> List[str]:
    """Fetch product slugs for a shop."""
    url = f"{BASE_URL}/slevy/{shop}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'},
                timeout=10.0
            )
            response.raise_for_status()
            html = response.text
            
            # Extract product links
            products = re.findall(r'/sleva/([a-z0-9-]+)', html)
            unique_products = list(set(products))
            return unique_products
        
        except Exception as e:
            print(f"❌ Error fetching {shop}: {e}")
            return []

async def fetch_product_details(product_slug: str) -> Optional[Dict]:
    """Fetch detailed information for a product."""
    url = f"{BASE_URL}/sleva/{product_slug}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'},
                timeout=10.0
            )
            response.raise_for_status()
            html = response.text
            
            # Parse with BeautifulSoup (TODO: improve parsing)
            soup = BeautifulSoup(html, 'lxml')
            
            # TODO: Extract structured data
            # - price
            # - original_price
            # - shop(s)
            # - validity dates
            # - product name
            
            return {
                "slug": product_slug,
                "name": product_slug.replace('-', ' ').title(),
                "price": None,
                "shops": [],
                "validity": None
            }
        
        except Exception as e:
            print(f"❌ Error fetching details for {product_slug}: {e}")
            return None

async def scrape_shop(shop: str) -> List[Dict]:
    """
    Scrape all products from a shop.
    Returns list of product dicts with details.
    """
    print(f"🛒 Scraping {shop}...")
    products_slugs = await fetch_shop_products(shop)
    
    # Fetch details for each product (with rate limiting)
    products = []
    for slug in products_slugs[:10]:  # Limit for testing
        details = await fetch_product_details(slug)
        if details:
            products.append(details)
        await asyncio.sleep(0.5)  # Be nice to the server
    
    return products

async def scrape_all_shops() -> Dict[str, List[Dict]]:
    """
    Scrape all shops concurrently.
    Returns dict: {shop_slug: [products]}
    """
    tasks = [scrape_shop(shop) for shop in SHOPS]
    results = await asyncio.gather(*tasks)
    
    return dict(zip(SHOPS, results))

if __name__ == "__main__":
    # Test scraping
    result = asyncio.run(scrape_all_shops())
    print(f"Scraped {sum(len(products) for products in result.values())} products")

"""Scraper extractors for Czech retail chains."""

import re
import urllib.request
from datetime import datetime
from typing import List, Dict, Any, Optional


SHOPS = {
    "penny": {"name": "Penny Market", "slug": "penny-market"},
    "lidl": {"name": "Lidl", "slug": "lidl"},
    "kaufland": {"name": "Kaufland", "slug": "kaufland"},
    "billa": {"name": "Billa", "slug": "billa"},
}

def get_current_leaflet_id(shop_slug: str) -> Optional[str]:
    """Get current leaflet ID from shop page."""
    try:
        url = f"https://www.akcniceny.cz/letaky/{shop_slug}/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Find leaflet links like /letak/penny-184570/strana-1/
            matches = re.findall(r'/letak/[^"\'>]+-(\d+)/strana', html)
            return matches[0] if matches else None
    except Exception as e:
        print(f"Error fetching leaflet ID for {shop_slug}: {e}")
        return None


def extract_deals_from_html(html: str) -> List[Dict[str, Any]]:
    """Extract product deals from HTML content."""
    deals = []
    
    # Pattern pro produkt s cenou
    pattern = r'<div[^>]*class="[^"]*deal[^"]*"[^>]*>.*?'
    pattern += r'<div[^>]*class="[^"]*name[^"]*"[^>]*>(.*?)</div>.*?'
    pattern += r'<div[^>]*class="[^"]*price[^"]*"[^>]*>(.*?)</div>.*?'
    pattern += r'<div[^>]*class="[^"]*unit-price[^"]*"[^>]*>(.*?)</div>.*?'
    pattern += r'<div[^>]*class="[^"]*validity[^"]*"[^>]*>(.*?)</div>'
    
    # Zkuste jednodušší pattern
    if 'class="deal"' in html:
        deals = []
        deal_pattern = r'class="deal"[^>]*>(.*?)</div>\s*</div>'
        matches = re.findall(deal_pattern, html, re.DOTALL)
        
        for deal_html in matches[:20]:  # Omezit na prvních 20
            product_match = re.search(r'class="name"[^>]*>(.*?)</div>', deal_html)
            price_match = re.search(r'class="price"[^>]*>(.*?)</div>', deal_html)
            
            if product_match and price_match:
                deals.append({
                    'product': product_match.group(1).strip(),
                    'price': price_match.group(1).strip(),
                    'extracted_at': datetime.now().isoformat()
                })
    
    return deals


class AkcnicenyExtractor:
    """Extractor for akcniceny.cz"""
    
    def __init__(self):
        self.base_url = "https://www.akcniceny.cz"
    
    async def fetch_shop_leaflet(self, shop_slug: str) -> Optional[str]:
        """Fetch leaflet HTML for a shop."""
        try:
            url = f"{self.base_url}/letaky/{shop_slug}/"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error fetching leaflet for {shop_slug}: {e}")
            return None
    
    async def extract_deals(self, shop_slug: str) -> List[Dict[str, Any]]:
        """Extract all deals from a shop."""
        shop_info = SHOPS.get(shop_slug)
        if not shop_info:
            return []
        
        leaflet_html = await self.fetch_shop_leaflet(shop_slug)
        if not leaflet_html:
            return []
        
        deals = extract_deals_from_html(leaflet_html)
        
        # Přidat metadata
        for deal in deals:
            deal['shop'] = shop_info['name']
            deal['shop_slug'] = shop_slug
            deal['extracted_at'] = datetime.now().isoformat()
        
        return deals
    
    async def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all configured shops."""
        all_deals = []
        
        for shop_slug in SHOPS.keys():
            shop_deals = await self.extract_deals(shop_slug)
            all_deals.extend(shop_deals)
        
        return all_deals

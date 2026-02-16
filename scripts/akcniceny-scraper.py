#!/usr/bin/env python3
"""
akcniceny-scraper.py — Scraping akcniceny.cz pro hledání produktů v akci

Usage: ./akcniceny-scraper.py "kiwi"
"""

import sys
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import urllib.parse


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
BASE_URL = "https://www.akcniceny.cz"


def search_product(query: str) -> List[Dict]:
    """
    Vyhledá produkt na akcniceny.cz
    
    Returns: List[{
        'title': str,
        'price': str,
        'original_price': str | None,
        'store': str,
        'url': str,
        'valid_until': str | None
    }]
    """
    search_url = f"{BASE_URL}/zbozi/?q={urllib.parse.quote(query)}"
    
    try:
        response = requests.get(
            search_url,
            headers={"User-Agent": USER_AGENT},
            timeout=15
        )
        response.raise_for_status()
        
    except requests.RequestException as e:
        print(f"ERROR: Failed to fetch {search_url}: {e}", file=sys.stderr)
        return []
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Najdi produkty (struktura může být různá)
    products = []
    
    # Pokusím se najít produktové bloky
    # Typicky mají class jako 'product', 'item', 'zbozi-item' apod.
    product_cards = soup.find_all(['article', 'div'], class_=lambda x: x and ('product' in x.lower() or 'item' in x.lower() or 'zbozi' in x.lower()))
    
    for card in product_cards[:10]:  # Max 10 výsledků
        try:
            # Extrahuj název
            title_elem = card.find(['h3', 'h4', 'h5', 'a'], class_=lambda x: x and ('title' in x.lower() or 'name' in x.lower()))
            if not title_elem:
                title_elem = card.find('a', href=lambda x: x and '/akce/' in x)
            
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Extrahuj cenu
            price_elem = card.find(['span', 'div'], class_=lambda x: x and ('price' in x.lower() or 'cena' in x.lower()))
            price = price_elem.get_text(strip=True) if price_elem else None
            
            # Extrahuj obchod
            store_elem = card.find(['span', 'div', 'a'], class_=lambda x: x and ('store' in x.lower() or 'retezec' in x.lower() or 'obchod' in x.lower()))
            store = store_elem.get_text(strip=True) if store_elem else None
            
            # URL
            link_elem = card.find('a', href=True)
            url = BASE_URL + link_elem['href'] if link_elem and not link_elem['href'].startswith('http') else (link_elem['href'] if link_elem else None)
            
            if title and price:
                products.append({
                    'title': title,
                    'price': price,
                    'store': store or 'N/A',
                    'url': url or search_url
                })
        
        except Exception as e:
            print(f"WARN: Failed to parse product card: {e}", file=sys.stderr)
            continue
    
    return products


def main():
    if len(sys.argv) < 2:
        print("Usage: akcniceny-scraper.py \"query\"", file=sys.stderr)
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"🔍 Searching for: {query}", file=sys.stderr)
    
    results = search_product(query)
    
    if not results:
        print(f"❌ No results found for '{query}'", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ Found {len(results)} results:", file=sys.stderr)
    
    for i, product in enumerate(results, 1):
        print(f"\n{i}. {product['title']}")
        print(f"   Price: {product['price']}")
        print(f"   Store: {product['store']}")
        print(f"   URL: {product['url']}")


if __name__ == "__main__":
    main()

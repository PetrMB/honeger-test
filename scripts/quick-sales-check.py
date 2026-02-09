#!/usr/bin/env python3
"""
Quick sales check without Reminders dependency.
Just fetches top deals from Kupi.cz and formats them.
"""

import re
import urllib.request
import json
from datetime import datetime

SHOPS = [
    ("Penny Market", "penny-market"),
    ("Kaufland", "kaufland"), 
    ("Lidl", "lidl"),
    ("Billa", "billa")
]

def fetch_sales(shop_id):
    """Fetch sales from Kupi.cz."""
    url = f"https://www.kupi.cz/letaky/{shop_id}"
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            return parse_sales(html)
    except Exception as e:
        return [f"Chyba: {str(e)[:50]}"]

def parse_sales(html):
    """Parse product sales from HTML."""
    sales = []
    
    # Look for product patterns with prices
    # Pattern like: product name - price Kč, shop, validity
    patterns = [
        r'<h3[^>]*>([^<]+)</h3>.*?([0-9]+[\s,]?[0-9]*)\s*K[cč]',  # h3 title with price
        r'class=["\'][^"\']*sale[^"\']*["\'][^>]*>([^<]+)</[^>]+>\s*([0-9]+)',  # sale class
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        for match in matches[:5]:  # limit per pattern
            if isinstance(match, tuple):
                name = re.sub(r'<[^>]+>', '', match[0]).strip()
                price = match[1] if len(match) > 1 else "?"
                if name and len(name) > 2:
                    sales.append(f"{name} - {price} Kč")
    
    return sales[:10]  # top 10

def main():
    print("🛒 Kontrola akčních letáků\n")
    print(f"📅 {datetime.now().strftime('%A %d.%m.%Y')}\n")
    
    all_results = []
    
    for shop_name, shop_id in SHOPS:
        print(f"🔍 {shop_name}...")
        sales = fetch_sales(shop_id)
        if sales and not sales[0].startswith("Chyba"):
            all_results.append((shop_name, sales))
            print(f"  ✅ {len(sales)} položek")
        else:
            print(f"  ⚠️ Nic nalezeno nebo chyba")
    
    print("\n" + "="*50)
    print("📊 VÝSLEDKY:\n")
    
    for shop_name, sales in all_results:
        print(f"🏪 {shop_name}:")
        for i, sale in enumerate(sales[:5], 1):
            print(f"  {i}. {sale}")
        print()
    
    print("="*50)
    print("💡 Tip: Pro detailní info navštiv kupi.cz")

if __name__ == "__main__":
    main()

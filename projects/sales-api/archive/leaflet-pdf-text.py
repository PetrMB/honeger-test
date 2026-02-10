#!/usr/bin/env python3
"""
Download leaflets and extract text directly from PDF (no OCR needed for many PDFs).
Faster and lighter than OCR version.
"""

import os
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime

SHOPS = {
    "penny": {
        "name": "Penny Market",
        "url": "https://www.penny.cz/akcni-letak",
    },
    "lidl": {
        "name": "Lidl", 
        "url": "https://www.lidl.cz/letaky",
    },
    "kaufland": {
        "name": "Kaufland",
        "url": "https://www.kaufland.cz/letak.html",
    },
    "billa": {
        "name": "Billa",
        "url": "https://www.billa.cz/akce",
    }
}

def extract_text_from_pdf(pdf_path):
    """Extract text using pdftotext (poppler)."""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', pdf_path, '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else ""
    except:
        return ""

def parse_deals(text):
    """Find product + price patterns in Czech."""
    deals = []
    
    # Lines with prices
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
            
        # Price patterns
        price_match = re.search(r'(\d+[.,]\d+)\s*K[cč]', line, re.IGNORECASE)
        if price_match:
            price = price_match.group(1).replace(',', '.')
            # Get text before price
            product = line[:price_match.start()].strip()
            product = re.sub(r'^[\d\s\-\.]+', '', product)
            
            if len(product) > 2 and len(product) < 80:
                deals.append({
                    'product': product,
                    'price': f"{price} Kč",
                    'raw': line
                })
    
    return deals[:10]  # Top 10

def quick_leaflet_check():
    """Quick version using web scraping of current deals pages."""
    print("🛒 Rychlá kontrola letáků (PDF text extrakce)\n")
    
    results = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for shop_id, shop in SHOPS.items():
            print(f"🔍 {shop['name']}...")
            
            try:
                # Simple approach: scrape web page for current deals
                req = urllib.request.Request(
                    shop['url'],
                    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
                )
                
                with urllib.request.urlopen(req, timeout=15) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')
                    
                    # Extract product entries (common patterns in shop websites)
                    # Look for product names and prices
                    deals = []
                    
                    # Pattern: product in title/alt/h3 with nearby price
                    product_patterns = [
                        r'<h[23][^>]*>([^<]+)</h[23]>',
                        r'title="([^"]{3,50})"[^>]*>[^<]*<[^>]*>([^<]*\d+[.,]\d+[^<]*)',
                        r'alt="([^"]{3,50})"',
                    ]
                    
                    for pattern in product_patterns:
                        matches = re.findall(pattern, html)
                        for match in matches[:5]:
                            if isinstance(match, tuple):
                                name, price_text = match
                            else:
                                name = match
                                price_text = ""
                            
                            # Clean up
                            name = re.sub(r'<[^>]+>', '', name).strip()
                            
                            # Look for price near this product in text
                            price_match = re.search(r'(\d+[.,]\d+)\s*K', html[:html.find(name)+len(name)+100]) if name in html else None
                            
                            if name and len(name) > 3:
                                deals.append({
                                    'product': name,
                                    'price': '? Kč',  # Would need better parsing
                                    'raw': name[:50]
                                })
                    
                    if deals:
                        results.append((shop['name'], deals[:5]))
                        print(f"  ✅ {len(deals[:5])} nalezeno")
                    else:
                        print(f"  ⚠️ Nic nebo anti-scraping")
                        
            except Exception as e:
                print(f"  ❌ Chyba: {str(e)[:40]}")
    
    # Output
    lines = [
        "🛒 Akční nabídky (rychlý text-only scan)",
        f"📅 {datetime.now().strftime('%A %d.%m.%Y %H:%M')}",
        "=" * 40,
        ""
    ]
    
    for shop_name, deals in results:
        lines.append(f"🏪 {shop_name}:")
        for i, d in enumerate(deals, 1):
            price = d['price'] if 'price' in d else '? Kč'
            lines.append(f"  {i}. {d['product'][:40]} - {price}")
        lines.append("")
    
    if not results:
        lines.append("⚠️ Nepodařilo se stáhnout data - obchody používají anti-scraping")
        lines.append("💡 Můžeš navštívit: penny.cz, lidl.cz, kaufland.cz, billa.cz")
    
    output = '\n'.join(lines)
    print('\n' + output)
    
    return output

if __name__ == "__main__":
    quick_leaflet_check()

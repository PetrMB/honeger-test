#!/usr/bin/env python3
"""
Scan leaflets from akcniceny.cz using OCR.
No Reminders dependency - sends results directly to iMessage.
"""

import os
import re
import subprocess
import tempfile
import urllib.request
from datetime import datetime

SHOPS = {
    "penny": {"name": "Penny Market", "slug": "penny-market"},
    "lidl": {"name": "Lidl", "slug": "lidl"},
    "kaufland": {"name": "Kaufland", "slug": "kaufland"},
    "billa": {"name": "Billa", "slug": "billa"},
}

def get_current_leaflet_id(shop_slug):
    """Get current leaflet ID from shop page."""
    try:
        url = f"https://www.akcniceny.cz/letaky/{shop_slug}/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Find leaflet links like /letak/penny-184570/strana-1/
            matches = re.findall(r'/letak/[^"\'>]+-(\d+)/strana', html)
            if matches:
                # Return most frequent (current) leaflet ID
                from collections import Counter
                return Counter(matches).most_common(1)[0][0]
    except Exception as e:
        print(f"Error getting leaflet ID for {shop_slug}: {e}")
    return None

def download_leaflet_image(shop_id, leaflet_id, page=1):
    """Download leaflet page image from staticac.cz CDN."""
    try:
        # CDN URLs: cz1-cz5.staticac.cz
        cdn_servers = [1, 2, 3, 4, 5]
        
        for cdn in cdn_servers:
            url = f"https://cz{cdn}.staticac.cz/foto/letaky/{leaflet_id}/l{leaflet_id}{page:02d}.jpg"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        return resp.read()
            except:
                continue
                
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None

def ocr_image(image_data):
    """Run OCR on image data using Tesseract."""
    try:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            f.write(image_data)
            temp_path = f.name
        
        # Run tesseract
        result = subprocess.run(
            ['tesseract', temp_path, 'stdout', '-l', 'ces+eng'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        os.unlink(temp_path)
        
        if result.returncode == 0:
            return result.stdout
        return ""
        
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def extract_deals(text):
    """Extract product names and prices from OCR text."""
    deals = []
    lines = text.split('\n')
    
    # Skip these as standalone product names (units, garbage)
    skip_patterns = [
        r'^(ml|ks|kg|g|l|cm|mm|m|pcs|pack|bal|ks=|kg=|g=|ml=|l=)$',
        r'^[\d\s\.,=\-]+$',  # Just numbers and symbols
        r'^(x\s*\d+|\d+\s*x)$',  # Multipliers like "x 2" or "2 x"
        r'^[=\-]{2,}$',  # Lines with just dashes/equals
    ]
    
    for line in lines:
        line = line.strip()
        if len(line) < 3:
            continue
            
        # Look for price patterns: 29,90 Kč, 29.90 Kč, etc.
        # Skip prices that look like "per unit" prices (e.g., "100g=7,90Kč")
        price_match = re.search(r'(\d+[.,]\d+)\s*K[cč]', line, re.IGNORECASE)
        if not price_match:
            continue
        
        price_str = price_match.group(1)
        price = price_str.replace(',', '.')
        
        # Accept prices from 5 to 999 Kč (skip per-unit prices like 0,79 Kč)
        try:
            price_val = float(price)
            if price_val < 5 or price_val > 999:  # Main product price range
                continue
        except:
            continue
        # Get text before price as product name
        product = line[:price_match.start()].strip()
        
        # Clean up
        product = re.sub(r'^[\d\s\.\-]+', '', product)  # Remove leading numbers/symbols
        product = re.sub(r'\s+', ' ', product)  # Normalize spaces
        product = re.sub(r'\s*=+\s*$', '', product)  # Remove trailing equals
        
        # Skip if matches garbage patterns
        if len(product) < 3 or len(product) > 60:
            continue
            
        skip = False
        for pattern in skip_patterns:
            if re.match(pattern, product, re.IGNORECASE):
                skip = True
                break
        
        if skip:
            continue
        
        # Must contain at least one letter
        if not re.search(r'[a-zA-ZáčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]', product):
            continue
            
        deals.append({
            'product': product,
            'price': f"{price} Kč",
            'raw': line
        })
    
    # Remove duplicates based on product name
    seen = set()
    unique_deals = []
    for d in deals:
        key = re.sub(r'[^a-zA-Z]', '', d['product'].lower())  # Normalize for dedup
        if key not in seen and len(unique_deals) < 10:
            seen.add(key)
            unique_deals.append(d)
    
    return unique_deals

def main():
    print("🛒 AkcniCeny.cz - OCR Scanner (všechny strany)")
    print(f"📅 {datetime.now().strftime('%A %d.%m.%Y')}\n")
    
    results = []
    MAX_PAGES = 4  # Limit to avoid too many requests
    
    for shop_id, shop_info in SHOPS.items():
        print(f"🔍 {shop_info['name']}...")
        
        # Get current leaflet ID
        leaflet_id = get_current_leaflet_id(shop_info['slug'])
        if not leaflet_id:
            print(f"  ⚠️ Leták nenalezen")
            continue
        
        print(f"  📄 Leták ID: {leaflet_id}")
        
        # Download multiple pages
        all_text = ""
        pages_found = 0
        
        for page in range(1, MAX_PAGES + 1):
            image_data = download_leaflet_image(shop_id, leaflet_id, page=page)
            if not image_data:
                if page == 1:
                    print(f"  ❌ Obrázek letáku není dostupný")
                break  # No more pages
            
            pages_found += 1
            print(f"  ✅ Strana {page}: {len(image_data)} bytes")
            
            # OCR
            text = ocr_image(image_data)
            if text:
                all_text += f"\n--- Strana {page} ---\n{text}\n"
        
        if pages_found == 0:
            print(f"  ❌ Žádné strany nenalezeny")
            continue
        
        print(f"  📄 Zpracováno {pages_found} stran")
        
        # Extract deals from all pages combined
        deals = extract_deals(all_text)
        if deals:
            results.append((shop_info['name'], deals, pages_found))
            print(f"  ✅ Celkem {len(deals)} unikátních produktů")
        else:
            print(f"  ⚠️ Žádné produkty extrahovány")
    
    # Format output
    lines = [
        "🛒 Akční letáky - akcniceny.cz + OCR",
        f"📅 {datetime.now().strftime('%A %d.%m.%Y')}",
        "=" * 40,
        ""
    ]
    
    for shop_name, deals, pages_found in results:
        lines.append(f"🏪 {shop_name} ({pages_found} str.):")
        for i, d in enumerate(deals, 1):
            lines.append(f"  {i}. {d['product']} - {d['price']}")
        lines.append("")
    
    total_products = sum(len(deals) for _, deals, _ in results)
    total_pages = sum(pages for _, _, pages in results)
    
    if not results:
        lines.append("⚠️ Žádné letáky nenalezeny nebo OCR selhalo")
        lines.append("💡 Zkus navštívit akcniceny.cz přímo")
    else:
        lines.append(f"📊 Celkem: {total_products} produktů z {total_pages} stran letáků")
    
    output = '\n'.join(lines)
    print("\n" + output)
    
    # Send via iMessage using osascript
    try:
        escaped = output.replace('"', '\\"').replace("'", "\\'")
        subprocess.run([
            'osascript', '-e',
            f'tell application "Messages" to send "{escaped[:4000]}" to buddy "czech@honeger.com"'
        ], timeout=15, capture_output=True)
        print("\n📱 Odesláno na iMessage")
    except Exception as e:
        print(f"\n⚠️ Chyba při odesílání iMessage: {e}")
    
    return output

if __name__ == "__main__":
    main()

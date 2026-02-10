#!/usr/bin/env python3
"""
Download leaflets from major Czech shops and extract products/prices via OCR.
No Reminders dependency - sends results directly to iMessage.
"""

import os
import re
import json
import subprocess
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path

# Shop configurations with their leaflet URLs
SHOPS = {
    "lidl": {
        "name": "Lidl",
        "leaflet_url": "https://www.lidl.cz/letaky",
        "pdf_pattern": r'href="([^"]+\.pdf)"',
    },
    "penny": {
        "name": "Penny Market", 
        "leaflet_url": "https://www.penny.cz/akcni-letak",
        "pdf_pattern": r'href="([^"]+\.pdf)"',
    },
    "kaufland": {
        "name": "Kaufland",
        "leaflet_url": "https://www.kaufland.cz/letak.html", 
        "pdf_pattern": r'href="([^"]+\.pdf)"',
    },
    "billa": {
        "name": "Billa",
        "leaflet_url": "https://www.billa.cz/akce",
        "pdf_pattern": r'href="([^"]+\.pdf)"',
    }
}

def download_leaflet_pdf(shop_id, temp_dir):
    """Download current leaflet PDF for a shop."""
    shop = SHOPS[shop_id]
    
    try:
        # First get the HTML page to find PDF link
        req = urllib.request.Request(
            shop["leaflet_url"],
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=20) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Find PDF links
            matches = re.findall(shop["pdf_pattern"], html)
            if not matches:
                return None
                
            # Take first PDF link
            pdf_url = matches[0]
            if not pdf_url.startswith('http'):
                # Relative URL, make absolute
                base = shop["leaflet_url"].split('/')[2]
                pdf_url = f"https://{base}{pdf_url if pdf_url.startswith('/') else '/' + pdf_url}"
            
            # Download PDF
            pdf_path = os.path.join(temp_dir, f"{shop_id}_letak.pdf")
            
            pdf_req = urllib.request.Request(
                pdf_url,
                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            )
            
            with urllib.request.urlopen(pdf_req, timeout=30) as pdf_response:
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_response.read())
            
            return pdf_path
            
    except Exception as e:
        print(f"Error downloading {shop_id}: {e}")
        return None

def extract_images_from_pdf(pdf_path, temp_dir):
    """Convert PDF pages to images for OCR."""
    try:
        # Use pdftoppm or sips to convert PDF to images
        base_name = os.path.basename(pdf_path).replace('.pdf', '')
        output_pattern = os.path.join(temp_dir, f"{base_name}_page")
        
        # pdftoppm is usually available on macOS
        result = subprocess.run(
            ['pdftoppm', '-jpeg', '-r', '150', pdf_path, output_pattern],
            capture_output=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return []
        
        # Find generated images
        images = []
        for f in os.listdir(temp_dir):
            if f.startswith(f"{base_name}_page") and f.endswith('.jpg'):
                images.append(os.path.join(temp_dir, f))
        
        return sorted(images)
        
    except Exception as e:
        print(f"PDF conversion error: {e}")
        return []

def ocr_image(image_path):
    """Run OCR on an image using macOS built-in Vision framework via shortctuts or tesseract."""
    try:
        # Try using macOS Vision framework via shortcuts command
        # First check if tesseract is available
        tesseract_check = subprocess.run(
            ['which', 'tesseract'],
            capture_output=True
        )
        
        if tesseract_check.returncode == 0:
            # Use Tesseract OCR
            result = subprocess.run(
                ['tesseract', image_path, 'stdout', '-l', 'ces'],
                capture_output=True,
                text=True,
                timeout=15
            )
            return result.stdout if result.returncode == 0 else ""
        else:
            # Fallback: use macOS built-in text recognition
            # This requires more complex AppleScript/shortcut setup
            return ""
            
    except Exception as e:
        print(f"OCR error: {e}")
        return ""

def parse_products(text):
    """Extract product names and prices from OCR text."""
    products = []
    
    # Pattern: product name followed by price
    # Czech price formats: 12,90 Kč, 12.90 Kč, 12,90Kč, etc.
    price_patterns = [
        r'([^\n]{3,50})\s+([0-9]+[.,][0-9]+)\s*K[cč]',
        r'([^\n]{3,50})\s+([0-9]+)\s*K[cč]',
    ]
    
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) < 3:
            continue
            
        # Check for price patterns
        for pattern in price_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                price = match.group(2).replace(',', '.')
                
                # Clean up name
                name = re.sub(r'^[0-9.,\s]+', '', name)  # Remove leading numbers
                name = re.sub(r'\s+', ' ', name)  # Normalize spaces
                
                if len(name) > 2 and len(name) < 60:
                    products.append({
                        'name': name,
                        'price': f"{price} Kč",
                        'raw': line
                    })
                break
    
    return products

def send_imessage(message, target="czech@honeger.com"):
    """Send message via iMessage."""
    try:
        subprocess.run(
            ['osascript', '-e',
             f'tell application "Messages" to send "{message.replace(chr(34), chr(92)+chr(34))}" to buddy "{target}"'],
            timeout=10
        )
    except Exception as e:
        print(f"Failed to send iMessage: {e}")

def main():
    print("🛒 Leaflet OCR Scanner")
    print(f"📅 {datetime.now().strftime('%A %d.%m.%Y %H:%M')}\n")
    
    all_results = {}
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for shop_id, shop_info in SHOPS.items():
            print(f"🔍 {shop_info['name']}...")
            
            # Download PDF
            pdf_path = download_leaflet_pdf(shop_id, temp_dir)
            if not pdf_path:
                print(f"  ❌ Nepodařilo se stáhnout leták")
                continue
            
            print(f"  ✅ PDF stažen")
            
            # Convert to images
            images = extract_images_from_pdf(pdf_path, temp_dir)
            if not images:
                print(f"  ❌ Konverze PDF selhala")
                continue
            
            print(f"  ✅ {len(images)} stránek k OCR")
            
            # OCR each image
            all_products = []
            for img_path in images[:3]:  # Limit to first 3 pages
                text = ocr_image(img_path)
                products = parse_products(text)
                all_products.extend(products)
            
            # Deduplicate and limit
            seen = set()
            unique_products = []
            for p in all_products:
                key = p['name'].lower()
                if key not in seen and len(unique_products) < 10:
                    seen.add(key)
                    unique_products.append(p)
            
            all_results[shop_id] = {
                'name': shop_info['name'],
                'products': unique_products
            }
            
            print(f"  ✅ Nalezeno {len(unique_products)} produktů")
    
    # Format output
    output_lines = [
        "🛒 Akční letáky - OCR scan",
        f"📅 {datetime.now().strftime('%A %d.%m.%Y')}",
        "=" * 40,
        ""
    ]
    
    for shop_id, data in all_results.items():
        if data['products']:
            output_lines.append(f"🏪 {data['name']}:")
            for i, p in enumerate(data['products'], 1):
                output_lines.append(f"  {i}. {p['name']} - {p['price']}")
            output_lines.append("")
    
    if not any(d['products'] for d in all_results.values()):
        output_lines.append("⚠️ Žádné produkty nenalezeny - pravděpodobně chybí OCR (tesseract)")
        output_lines.append("💡 Install: brew install tesseract tesseract-lang")
    
    output = "\n".join(output_lines)
    print("\n" + output)
    
    # Send via iMessage
    send_imessage(output)
    print("\n📱 Odesláno na iMessage")

if __name__ == "__main__":
    main()

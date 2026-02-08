#!/usr/bin/env python3
"""
Check grocery sales on Kupi.cz and update Apple Reminders notes.
Improved version with progress output and better error handling.
"""

import re
import subprocess
from datetime import datetime
from difflib import SequenceMatcher
import urllib.request
import time

# Shops to check
SHOPS = ["lidl", "penny-market", "billa", "kaufland"]

def get_reminders():
    """Get incomplete reminders from Nákupy list."""
    print("📝 Getting reminders from Apple Reminders...")
    result = subprocess.run(
        ["osascript", "-e", 
         'tell application "Reminders" to get name of reminders of list "Nákupy" whose completed is false'],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode != 0:
        print(f"❌ Error getting reminders: {result.stderr}")
        return []
    
    # Parse comma-separated list
    items = [item.strip() for item in result.stdout.split(',') if item.strip()]
    print(f"✅ Found {len(items)} items in Nákupy list")
    return items

def normalize_product_name(name):
    """Normalize product name for matching."""
    name_lower = name.lower()
    # Remove common suffixes
    suffixes = [' osivo', ' sazenice', ' pytlíčky', ' granule', ' krmivo', ' stelivo']
    for suffix in suffixes:
        if name_lower.endswith(suffix):
            name_lower = name_lower[:-len(suffix)].strip()
    return name_lower

def fuzzy_match(a, b):
    """Calculate similarity between two strings (0-1)."""
    a_norm = normalize_product_name(a)
    b_norm = normalize_product_name(b).replace('-', ' ')
    
    # Calculate base similarity
    base_score = SequenceMatcher(None, a_norm, b_norm).ratio()
    
    # Check for stem/prefix matching
    a_words = set(a_norm.split())
    b_words = set(b_norm.split())
    
    stem_match = False
    for a_word in a_words:
        if len(a_word) < 3:
            continue
        for b_word in b_words:
            if len(b_word) < 3:
                continue
            min_len = min(len(a_word), len(b_word), 4)
            if a_word[:min_len] == b_word[:min_len]:
                stem_match = True
                break
        if stem_match:
            break
    
    if stem_match:
        return min(1.0, base_score + 0.35)
    
    # Exact word match bonus
    common_words = a_words & b_words
    if common_words:
        boost = min(0.3, len(common_words) * 0.15)
        return min(1.0, base_score + boost)
    
    return base_score

def fetch_sales(shop):
    """Fetch sales for a shop from Kupi.cz."""
    url = f"https://www.kupi.cz/slevy/{shop}"
    print(f"🛒 Fetching {shop}...")
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # Extract product links
        products = re.findall(r'/sleva/([a-z0-9-]+)', html)
        unique_products = list(set(products))
        print(f"  → Found {len(unique_products)} products")
        return unique_products
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def get_product_details(product_slug):
    """Get product details from Kupi.cz."""
    url = f"https://www.kupi.cz/sleva/{product_slug}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        price = None
        shop_name = None
        validity = None
        
        # Find first shop link
        shop_match = re.search(r'<a href="/letaky/([^"]+)"[^>]*title="([^"]+)"', html)
        if shop_match:
            shop_slug = shop_match.group(1).strip()
            shop_name_raw = shop_match.group(2).strip()
            
            shop_map = {
                'lidl': 'Lidl',
                'penny-market': 'Penny Market',
                'billa': 'Billa',
                'albert': 'Albert',
                'tesco': 'Tesco',
                'kaufland': 'Kaufland'
            }
            shop_name = shop_map.get(shop_slug, shop_name_raw)
        
        # Find price
        price_match = re.search(r'discount_price_value[^>]*>([0-9,]+(?:&nbsp;|\s)*Kč)', html)
        if price_match:
            price = price_match.group(1).replace('&nbsp;', ' ').strip()
        
        # Find validity
        validity_match = re.search(r'((?:st|čt|pá|so|ne|po|út)\s+\d{1,2}\.\s*\d{1,2}\.\s*(?:&ndash;|[–-])\s*(?:st|čt|pá|so|ne|po|út)\s+\d{1,2}\.\s*\d{1,2}\.)', html)
        if validity_match:
            validity = validity_match.group(1).replace('&ndash;', '–').strip()
        
        shops = [shop_name] if shop_name else []
        
        return {
            "name": product_slug.replace('-', ' ').title(),
            "price": price,
            "validity": validity,
            "shops": list(set(shops))
        }
    
    except Exception as e:
        print(f"    ❌ Error getting details for {product_slug}: {e}")
        return None

def update_reminder_note(reminder_name, note_text):
    """Update notes for a reminder."""
    safe_name = reminder_name.replace('"', '\\"')
    safe_note = note_text.replace('"', '\\"').replace('\n', '\\n')
    
    script = f'''
    tell application "Reminders"
        set theList to list "Nákupy"
        set theReminders to reminders of theList whose name is "{safe_name}" and completed is false
        if (count of theReminders) > 0 then
            set body of item 1 of theReminders to "{safe_note}"
            return "Updated"
        else
            return "Not found"
        end if
    end tell
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"    ❌ Error updating {reminder_name}: {e}")
        return False

def main():
    print(f"\n🔍 Starting sales check at {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Get current reminders
    reminders = get_reminders()
    if not reminders:
        print("❌ No reminders found or error accessing Reminders")
        return
    
    print(f"\n📋 Active items:")
    for i, item in enumerate(reminders, 1):
        print(f"  {i}. {item}")
    
    # Collect all sales
    print(f"\n🛍️  Fetching sales from online stores...\n")
    all_sales = {}
    for shop in SHOPS:
        products = fetch_sales(shop)
        for product in products:
            if product not in all_sales:
                all_sales[product] = []
            all_sales[product].append(shop)
        time.sleep(0.5)  # Be nice to the server
    
    print(f"\n💰 Total products in sales: {len(all_sales)}")
    
    # Match reminders with sales
    print(f"\n🔎 Matching your items with sales...\n")
    matches = []
    for reminder in reminders:
        best_match = None
        best_score = 0.5  # Minimum threshold
        
        candidates = []
        for product_slug in all_sales.keys():
            product_name = product_slug.replace('-', ' ')
            score = fuzzy_match(reminder, product_name)
            if score > 0.3:  # Only show reasonable candidates
                candidates.append((product_slug, score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        if candidates:
            print(f"'{reminder}':")
            for slug, score in candidates[:3]:
                marker = "✅" if score > best_score else "  "
                print(f"  {marker} {score:.2f} → {slug}")
            
            if candidates[0][1] > best_score:
                best_match = candidates[0][0]
                best_score = candidates[0][1]
                matches.append((reminder, best_match, best_score))
        else:
            print(f"'{reminder}': ❌ No matches found")
        print()
    
    # Update reminders with sale info
    print(f"\n📝 Updating {len(matches)} matched items...\n")
    updated = 0
    for reminder, product_slug, score in matches:
        print(f"Updating '{reminder}'...")
        details = get_product_details(product_slug)
        if details:
            note_parts = []
            if details['price']:
                note_parts.append(f"💰 {details['price']}")
            if details['shops']:
                note_parts.append(f"🛒 {', '.join(details['shops'])}")
            if details['validity']:
                note_parts.append(f"📅 {details['validity']}")
            
            note_text = ' | '.join(note_parts)
            
            if update_reminder_note(reminder, note_text):
                print(f"  ✅ {note_text}")
                updated += 1
            else:
                print(f"  ❌ Failed to update")
        time.sleep(0.3)  # Be nice
    
    print(f"\n✨ Done! Updated {updated}/{len(matches)} items\n")

if __name__ == "__main__":
    main()

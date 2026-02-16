#!/usr/bin/env python3
"""
shopping-deals.py — Najde akční ceny pro položky v Apple Reminders "Nákupy"

Workflow:
1. Načte nekompletní položky ze seznamu "Nákupy"
2. Pro každou položku hledá akce na akcniceny.cz
3. Pošle notifikaci s nalezenými akcemi
"""

import json
import subprocess
import sys
from typing import List, Dict, Optional
import re


def get_shopping_list_items() -> List[str]:
    """Získá nekompletní položky ze seznamu Nákupy"""
    try:
        result = subprocess.run(
            ["remindctl", "list", "Nákupy", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        reminders = json.loads(result.stdout)
        items = [
            item["title"]
            for item in reminders
            if not item.get("isCompleted", False)
        ]
        
        return items
    
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to get reminders: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON: {e}", file=sys.stderr)
        return []


def normalize_item(item: str) -> str:
    """Normalizuje název položky pro vyhledávání"""
    # Odstraň množství (2x, 3x)
    item = re.sub(r'\s+\d+x$', '', item, flags=re.IGNORECASE)
    # Odstraň extra whitespace
    item = ' '.join(item.split())
    return item.strip()


def search_deals(item: str) -> Optional[Dict]:
    """
    Vyhledá akce pro položku přes Kupi.cz API
    """
    try:
        from kupiapi.scraper import KupiScraper
        import json
        
        scraper = KupiScraper()
        results_json = scraper.get_discounts_by_search(item)
        
        if not results_json:
            return None
        
        results = json.loads(results_json)
        
        if not results or len(results) == 0:
            return None
        
        # Vezmi první výsledek
        first = results[0]
        
        # Vrať první obchod a cenu
        shop = first.get('shops', ['N/A'])[0] if first.get('shops') else 'N/A'
        price = first.get('prices', ['N/A'])[0] if first.get('prices') else 'N/A'
        amount = first.get('amounts', [''])[0] if first.get('amounts') else ''
        validity = first.get('validities', [''])[0] if first.get('validities') else ''
        
        return {
            'item': first.get('name', item),
            'price': price,
            'amount': amount,
            'store': shop,
            'validity': validity
        }
        
    except Exception as e:
        print(f"ERROR: Failed to search {item}: {e}", file=sys.stderr)
        return None


def format_notification(deals: List[Dict]) -> str:
    """Vytvoří text notifikace s nalezenými akcemi"""
    if not deals:
        return "🛒 Žádné akce pro tvoje nákupy dnes nenalezeny."
    
    lines = ["🛒 **Tvoje nákupy v akci:**\n"]
    
    for deal in deals:
        item = deal["item"]
        price = deal["price"]
        amount = deal.get("amount", "")
        store = deal["store"]
        validity = deal.get("validity", "")
        
        # Format: Kiwi - 4,90 Kč/ks (Albert, končí dnes)
        price_str = f"{price}"
        if amount:
            price_str += f"/{amount}"
        
        extra = []
        if store:
            extra.append(store)
        if validity:
            extra.append(validity)
        
        extra_str = f" ({', '.join(extra)})" if extra else ""
        lines.append(f"• **{item}** - {price_str}{extra_str}")
    
    return "\n".join(lines)


def main():
    print("📋 Načítám nákupní seznam...", file=sys.stderr)
    items = get_shopping_list_items()
    
    if not items:
        print("⚠️  Nákupní seznam je prázdný nebo nedostupný", file=sys.stderr)
        return
    
    print(f"✅ Nalezeno {len(items)} položek", file=sys.stderr)
    
    # Normalizace a vyhledávání
    found_deals = []
    
    for item in items:
        normalized = normalize_item(item)
        print(f"🔍 Hledám: {normalized}", file=sys.stderr)
        
        deal = search_deals(normalized)
        if deal:
            found_deals.append(deal)
            print(f"  ✅ Nalezeno: {deal['price']} ({deal['store']})", file=sys.stderr)
        else:
            print(f"  ❌ Nenalezeno", file=sys.stderr)
    
    # Výstup
    notification = format_notification(found_deals)
    print(notification)
    
    if found_deals:
        print(f"\n✅ Nalezeno {len(found_deals)} akcí", file=sys.stderr)
    else:
        print("\n💡 Tip: Můžeš zkontrolovat akcniceny.cz ručně", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
update-reminders-with-prices.py

Získá nekompletní položky z "Nákupy", přidá ceny z akcí a aktualizuje reminder notes.

Workflow:
1. remindctl list Nákupy --json → nekompletní položky
2. Pro každou → vyhledá akce přes shopping-deals.py JSON
3. Update reminder notes s cenou + platností
"""

import json
import subprocess
import sys
import re
from typing import Optional
from pathlib import Path


def get_uncompleted_items() -> list:
    """Získá nekompletní položky ze seznamu Nákupy"""
    try:
        result = subprocess.run(
            ["remindctl", "list", "Nákupy", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        reminders = json.loads(result.stdout)
        return [r for r in reminders if not r.get("isCompleted", False)]
    except subprocess.CalledProcessError as e:
        print(f"ERROR: remindctl failed: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        return []


def load_deals_json() -> dict:
    """Načte výsledek shopping-deals.py jako JSON"""
    json_path = Path("~/.openclaw/workspace/data/shopping-deals.json").expanduser()
    if json_path.exists():
        try:
            with open(json_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"WARNING: Failed to load shopping-deals.json: {e}", file=sys.stderr)
    return {}


def normalize_title(title: str) -> str:
    """Normalizuje položku pro porovnání"""
    # Odstranit číslování [342] apod.
    title = re.sub(r"^\[\d+\]\s*\[\s*\]\s*", "", title)
    # Odstranit množství na konci (2x, 3x, 6 ks)
    title = re.sub(r"\s+\d+[xks]\s*$", "", title, flags=re.IGNORECASE)
    return title.strip().lower()


def find_deal(title: str, deals: dict) -> Optional[dict]:
    """Najde deal pro položku (fuzzy match)"""
    normalized = normalize_title(title)
    
    for key, deal in deals.items():
        deal_normalized = normalize_title(deal.get("title", ""))
        # Full match
        if normalized == deal_normalized:
            return deal
        # Contains match: reminder title je subset deal title
        if normalized in deal_normalized or deal_normalized in normalized:
            return deal
        # Partial match: nějaké slovo se shoduje
        title_words = normalized.split()
        deal_words = deal_normalized.split()
        if any(w in deal_words for w in title_words) or any(w in title_words for w in deal_words):
            return deal
    
    return None


def update_reminder_notes(reminder_id: str, price_info: dict) -> bool:
    """Update reminder notes s cenou a platností"""
    notes = []

    # Cena
    if price_info.get("price"):
        notes.append(f"💰 {price_info['price']} Kč")
    if price_info.get("store"):
        notes.append(f"🏪 {price_info['store']}")

    # Platnost (z validities: "čt 19. 2. – ne 22. 2.")
    validity = price_info.get("validity", "")
    if validity and "dnes končí" not in validity.lower():
        notes.append(f"📅 {validity}")
    elif validity and "dnes končí" in validity.lower():
        notes.append(f"🔥 {validity}")

    # Seznam notes oddělený \\n
    new_notes = "\\n".join(notes)

    try:
        result = subprocess.run(
            ["remindctl", "edit", reminder_id, "--notes", new_notes],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Cannot update {reminder_id}: {e.stderr}", file=sys.stderr)
        return False


def main():
    print("📋 Načítám nákupní seznam...")
    items = get_uncompleted_items()

    if not items:
        print("✅ Žádné nekompletní položky.")
        return 0

    print(f"✅ Nalezeno {len(items)} položek")

    # Načíst výsledek shopping-deals.py
    deals = load_deals_json()
    if not deals or "deals" not in deals:
        print("❌ Žádné dealy k dispozici.")
        return 1

    # Pro každou reminder položku zkus najít akci
    updated = 0
    not_found = []

    for item in items:
        title = item["title"]
        item_id = item["id"]

        # Najít deal (fuzzy match)
        deal = find_deal(title, {d.get("title", ""): d for d in deals["deals"]})

        if deal:
            # Update notes
            if update_reminder_notes(item_id, deal):
                updated += 1
                print(f"✅ {title} → {deal.get('price', '?')} Kč ({deal.get('store', '?')})")
            else:
                not_found.append(title)
        else:
            not_found.append(title)

    # Shrnutí
    print()
    print(f"📊 Hotovo: {updated} upraveno, {len(not_found)} nenalezeno")

    if not_found:
        print()
        print("❌ Položky bez akce:")
        for title in not_found:
            print(f"  - {title}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Seed shops into database."""

# Placeholder for manual seeding

SHOPS = [
    {"slug": "lidl", "name": "Lidl", "logo_url": None},
    {"slug": "penny", "name": "Penny Market", "logo_url": None},
    {"slug": "kaufland", "name": "Kaufland", "logo_url": None},
    {"slug": "billa", "name": "Billa", "logo_url": None},
]

print("Shops to seed:")
for shop in SHOPS:
    print(f"  - {shop['name']} ({shop['slug']})")

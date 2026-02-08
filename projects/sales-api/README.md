# 🛒 Sales API

**Databázová služba pro produkty v akci z českých obchodních řetězců**

## Status: 📋 Planning

Služba pro sledování a vyhledávání akčních cen produktů z:
- Lidl
- Penny Market  
- Billa
- Kaufland

## Quick Links

- 📋 **[PLAN.md](./PLAN.md)** - Kompletní plán implementace
- 🚀 **Tech Stack:** FastAPI + PostgreSQL + APScheduler
- 📊 **Data Source:** Kupi.cz scraping

## Features (Planned)

- ✅ Fuzzy search produktů
- ✅ Aktuální ceny a platnosti
- ✅ REST API
- 🔜 Price history tracking
- 🔜 Watchlisty + notifikace
- 🔜 Kategorizace produktů

## Development

```bash
# Setup (když bude ready)
cd projects/sales-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python -m uvicorn main:app --reload
```

## API Preview

```
GET /api/products/search?q=mleko
GET /api/products/{id}
GET /api/shops/{shop}/sales
GET /api/sales/recent
```

---

**Autor:** Otík 🦉  
**Vytvořeno:** 2026-02-08  
**Implementace:** WIP (work in progress během heartbeatů)

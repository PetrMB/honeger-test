# 🛒 Sales API - Služba pro produkty v akci

## Koncept

Veřejná API služba poskytující aktuální ceny produktů v akcích z českých řetězců.

## Co už máme

✅ **Existující kód:** `scripts/check-sales-improved.py`
- Scraping Kupi.cz (Lidl, Penny, Billa, Kaufland)
- Fuzzy matching produktů
- Parsing cen a platnosti
- Apple Reminders integrace

## Architektura služby

### 1. Backend Stack

**Varianta A: Python/FastAPI** ⭐ (preferuji)
```
FastAPI + SQLAlchemy + Pydantic
PostgreSQL (nebo SQLite pro start)
APScheduler pro periodické scrapování
```

**Varianta B: Node.js/Express**
```
Express + TypeScript
Prisma ORM
node-cron pro scraping
```

### 2. Databázové Schema

```sql
-- Obchody
CREATE TABLE shops (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,  -- 'lidl', 'penny-market'
    name VARCHAR(100) NOT NULL,         -- 'Lidl', 'Penny Market'
    logo_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Produkty (normalizované názvy)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    normalized_name VARCHAR(200) NOT NULL,  -- pro search
    category VARCHAR(100),                  -- 'mléko', 'pečivo'
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_normalized (normalized_name)
);

-- Akce (produkty v akci)
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    shop_id INTEGER REFERENCES shops(id),
    price DECIMAL(10,2),
    price_text VARCHAR(50),              -- "12,90 Kč"
    original_price DECIMAL(10,2),        -- pokud známe
    discount_percent INTEGER,            -- vypočítané procento
    valid_from DATE,
    valid_until DATE,
    validity_text VARCHAR(100),          -- "po 3.2. – ne 9.2."
    source_url TEXT,
    scraped_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_product_shop (product_id, shop_id),
    INDEX idx_valid_dates (valid_from, valid_until)
);

-- Historie cen (pro grafy a trendy)
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    shop_id INTEGER REFERENCES shops(id),
    price DECIMAL(10,2),
    recorded_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_product_time (product_id, recorded_at)
);

-- Uživatelské watchlisty (budoucí feature)
CREATE TABLE watchlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER REFERENCES products(id),
    notify_below_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. API Endpointy

#### Základní vyhledávání
```
GET /api/products/search?q=mleko&shop=lidl&limit=20
Response: [
  {
    "id": 123,
    "name": "Mléko trvanlivé 1.5%",
    "sales": [
      {
        "shop": "Lidl",
        "price": "12.90 Kč",
        "discount": "25%",
        "validUntil": "2026-02-15"
      }
    ]
  }
]
```

#### Detail produktu
```
GET /api/products/{id}
Response: {
  "id": 123,
  "name": "Mléko trvanlivé 1.5%",
  "category": "mléčné-výrobky",
  "currentSales": [...],
  "priceHistory": [...]
}
```

#### Akce v obchodě
```
GET /api/shops/{shop}/sales?category=mléčné-výrobky
Response: [...]
```

#### Poslední akce (feed)
```
GET /api/sales/recent?limit=50
Response: [...]
```

#### Statistiky
```
GET /api/stats
Response: {
  "totalProducts": 1234,
  "activeSales": 567,
  "shops": 4,
  "lastUpdate": "2026-02-08T20:00:00Z"
}
```

### 4. Scraping Worker

**Periodic Task:**
```python
@scheduler.scheduled_job('cron', hour='*/6')  # Každých 6 hodin
async def scrape_all_shops():
    for shop in SHOPS:
        products = await scrape_shop(shop)
        await save_to_database(products)
        await update_price_history()
```

**Rate limiting:**
- 0.5-1s delay mezi requesty
- Retry logic pro failed requests
- User-Agent rotation

### 5. Features Roadmap

**MVP (fáze 1):**
- ✅ Scraping 4 řetězců (Lidl, Penny, Billa, Kaufland)
- ✅ Fuzzy search produktů
- ✅ REST API pro vyhledávání
- ✅ Základní databáze (SQLite)
- ✅ Automatické updaty každých 6-12h

**Fáze 2:**
- Price history tracking
- Grafy cen v čase
- Kategorizace produktů
- Export API (CSV, JSON bulk)

**Fáze 3:**
- Uživatelské účty
- Watchlisty + notifikace
- Email/Telegram/WhatsApp alerts
- Mobile app API

**Fáze 4:**
- Více obchodů (Albert, Tesco, ...)
- ML pro predikci slev
- Price drop alerts
- Community features (upvote deals)

### 6. Deployment Options

**Option A: Self-hosted na Mac mini**
- Docker container
- Nginx reverse proxy
- Local PostgreSQL
- Exposing přes Tailscale nebo Cloudflare Tunnel

**Option B: Cloud (Fly.io / Railway)**
- Automatické scaling
- PostgreSQL hosting
- HTTPS out of the box
- ~$5-10/měsíc

**Option C: Serverless (Vercel/Cloudflare Workers)**
- API endpoints na edge
- Scheduled scraping přes cron
- Planetscale/Neon DB
- Free tier možný

### 7. Tech Stack (Recommended)

```
Backend:       FastAPI (Python 3.11+)
Database:      PostgreSQL 15 (nebo SQLite pro MVP)
ORM:           SQLAlchemy + Alembic migrations
Scheduler:     APScheduler nebo celery
API Docs:      OpenAPI/Swagger (built-in FastAPI)
Caching:       Redis (optional, pro performance)
Deployment:    Docker + docker-compose
Monitoring:    Sentry (error tracking)
```

### 8. Monetization (budoucnost)

- Free tier: 100 API calls/day
- Pro tier: Unlimited + webhooks ($5/měsíc)
- Enterprise: Custom scraping + SLA ($50/měsíc)
- Affiliate fees (když někdo koupí přes link)

### 9. Legal Considerations

⚠️ **Web scraping legal status:**
- Kupi.cz je agregátor, ne primární zdroj
- Respektovat robots.txt
- Rate limiting (být "nice" k serveru)
- Nezveřejňovat obrázky (copyright)
- Attribution link na Kupi.cz

**Safer approach:**
- Kontaktovat Kupi.cz pro API přístup
- Nebo použít oficiální API obchodů (pokud existuje)

---

## Next Steps

1. **MVP Implementation Plan**
   - [ ] Setup FastAPI + SQLAlchemy
   - [ ] Migrate scraping logic z check-sales-improved.py
   - [ ] Create database schema
   - [ ] Implement basic API endpoints
   - [ ] Add scheduler for scraping
   - [ ] Write tests
   - [ ] Deploy (Docker na Mac mini nebo Fly.io)

2. **Quick Start Command**
   ```bash
   # Vytvořit projekt strukturu
   mkdir -p sales-api/{api,scraper,models,tests}
   cd sales-api
   poetry init  # nebo python -m venv venv
   ```

3. **Frontend (optional)**
   - Simple SPA (Svelte/React)
   - Search interface
   - Price comparison view
   - Embeddable widget pro weby

---

Chceš, abych:
1. **Začal implementovat MVP** (FastAPI + SQLite + základní API)?
2. **Vytvořil project scaffold** (struktura + dependencies)?
3. **Nebo radši nejdřív diskutovat scope** (co přesně chceš v první verzi)?

🚀 Můžu to rozjet ve volných chvílích (heartbeats) a průběžně commutovat progress!

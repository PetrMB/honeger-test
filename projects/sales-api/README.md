# 🛒 Sales API

Veřejná API služba poskytující aktuální ceny produktů v akcích z českých řetězců.

## 🚀 Status

**MVP** — vývoj v progressu

## 📦 Instalace

```bash
cd projects/sales-api
pip install -r requirements.txt
```

## 🛠️ Použití

### 1. Inicializace databáze

```bash
python scripts/init_db.py
```

### 2. Skenování letáků

```bash
# ručně
python scripts/scan_sales.py

# nebo pomocí scheduleru
python scraper/scheduler.py
```

### 3. Spuštění API serveru

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. API endpoints

- `GET /api/products/search?q=mleko` — vyhledávání
- `GET /api/shops` — seznam obchodů
- `GET /api/stats` — statistiky
- `GET /health` — health check

## 📊 Data zdroje

- **akcniceny.cz** — OCR letáků (Lidl, Penny, Billa, Kaufland)
- **Scraping** — každých 6 hodin automaticky

## 🔐 Legální poznámky

- Respektovat robots.txt
- Rate limiting (být "nice" k serveru)
- Nezveřejňovat obrázky (copyright)
- Attribution na zdrojové stránky

## 📝 Vývoj

### Structure

```
sales-api/
├── api/              # FastAPI endpoints
├── models/           # SQLAlchemy models
├── scraper/          # Scraping worker
├── scripts/          # Database/seed scripts
└── tests/            # Test suite
```

### Roadmap

- [x] Base structure
- [ ] Fuzzy search
- [ ] Full scraping pipeline
- [ ] Database integration
- [ ] Tests
- [ ] Deployment (Fly.io/Cloudflare)

---

**Author:** Otík  
**License:** MIT ( TBD )

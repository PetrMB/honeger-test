# 📋 Sales API - TODO List

## MVP (Fáze 1) - Základní funkcionalita

### Database ✅
- [x] SQLAlchemy modely (Shop, Product, Sale, PriceHistory)
- [x] Database init script
- [ ] Alembic migrations setup
- [ ] Seed data (shops)

### Scraping 🚧
- [x] Basic scraper structure (kupi.py)
- [x] Fuzzy matching utilities
- [ ] Improve HTML parsing (BeautifulSoup)
- [ ] Extract price, validity, shop data properly
- [ ] Add retry logic + error handling
- [ ] Rate limiting per shop
- [ ] Save scraped data to database

### API Endpoints 🚧
- [x] Basic FastAPI app structure
- [x] Router placeholders (products, shops, sales, stats)
- [ ] Implement search with fuzzy matching
- [ ] Implement product detail endpoint
- [ ] Implement shop sales listing
- [ ] Implement recent sales feed
- [ ] Add pagination
- [ ] Add filtering (by price, shop, category)
- [ ] OpenAPI schema improvements

### Scheduler 📅
- [ ] APScheduler setup
- [ ] Periodic scraping job (every 6-12h)
- [ ] Update price history automatically
- [ ] Cleanup old sales data (>30 days)

### Testing 🧪
- [ ] Unit tests (models)
- [ ] Integration tests (API endpoints)
- [ ] Scraper tests (mock HTTP)
- [ ] Database tests

### Deployment 🚀
- [ ] Dockerfile
- [ ] docker-compose.yml (API + PostgreSQL)
- [ ] Environment variables (.env)
- [ ] README deploy instructions
- [ ] CI/CD (GitHub Actions)

---

## Fáze 2 - Price History & Categories

- [ ] Price history tracking per product
- [ ] Price charts API (data for graphs)
- [ ] Product categorization (ML or manual)
- [ ] Category-based search
- [ ] Price drop alerts (basic)

---

## Fáze 3 - User Features

- [ ] User authentication (JWT)
- [ ] Watchlists (save products)
- [ ] Notification system (email/Telegram)
- [ ] Personalized deals
- [ ] API rate limiting per user

---

## Fáze 4 - Advanced

- [ ] More shops (Albert, Tesco, Globus, ...)
- [ ] ML price prediction
- [ ] Community voting on deals
- [ ] Mobile app API
- [ ] GraphQL endpoint (optional)
- [ ] Affiliate links
- [ ] Admin dashboard

---

## Current Priority (Next Steps)

1. ✅ **Database setup** - `python database.py` to create tables
2. **Improve scraper** - properly extract price, shops, validity from HTML
3. **Save to DB** - write scraped products to database
4. **Implement search** - fuzzy matching against database
5. **Add scheduler** - run scraper every 6h automatically

---

## Notes

- Start with SQLite for simplicity
- Can migrate to PostgreSQL later
- Keep scraping respectful (rate limits, robots.txt)
- Consider legal implications (ToS of Kupi.cz)

---

**Last Updated:** 2026-02-08  
**Next Heartbeat Task:** Improve HTML parsing in `scraper/kupi.py`

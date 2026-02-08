# ☁️ Cloudflare Workers Deployment - Sales API

## Proč Cloudflare Workers?

✅ **Serverless** - žádná správa serverů  
✅ **Global edge** - rychlost po celém světě  
✅ **Free tier** - 100k requests/day zdarma  
✅ **Workers AI** - inference přímo na edge  
✅ **D1 Database** - SQLite na edge (perfect match!)  
✅ **Cron triggers** - nativní scheduling  

## Architecture

```
┌─────────────────────────────────────────┐
│  Cloudflare Workers (Edge)              │
│                                         │
│  ┌────────────────┐                    │
│  │  Sales API     │                    │
│  │  (Hono/itty)   │                    │
│  └────────┬───────┘                    │
│           │                             │
│  ┌────────▼───────┐  ┌──────────────┐ │
│  │  D1 Database   │  │  Cron Jobs   │ │
│  │  (SQLite)      │  │  (scraping)  │ │
│  └────────────────┘  └──────────────┘ │
└─────────────────────────────────────────┘
         │
         ▼
  ┌──────────────┐
  │  Kupi.cz     │  (external scraping)
  └──────────────┘
```

## Tech Stack (Cloudflare-native)

```typescript
Runtime:      Cloudflare Workers (V8 isolates)
Framework:    Hono (Express-like, CF-optimized)
Database:     D1 (SQLite on edge)
Scheduling:   Cron Triggers (built-in)
AI:           Workers AI (optional, pro fuzzy search)
Storage:      KV (pro caching, optional)
```

## Setup Steps

### 1. Install Wrangler CLI

```bash
npm install -g wrangler
wrangler login
```

### 2. Create D1 Database

```bash
wrangler d1 create sales-db

# Output:
# database_name = "sales-db"
# database_id = "xxxx-xxxx-xxxx"
```

### 3. Project Structure

```
sales-api-workers/
├── wrangler.toml           # CF config
├── src/
│   ├── index.ts            # Main worker
│   ├── routes/
│   │   ├── products.ts
│   │   ├── shops.ts
│   │   └── sales.ts
│   ├── scraper/
│   │   └── kupi.ts         # Scraping logic
│   └── db/
│       └── schema.sql      # D1 schema
└── package.json
```

### 4. wrangler.toml

```toml
name = "sales-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# D1 Database binding
[[d1_databases]]
binding = "DB"
database_name = "sales-db"
database_id = "your-database-id"

# Cron triggers (scraping)
[triggers]
crons = ["0 */6 * * *"]  # Every 6 hours

# Environment variables
[vars]
ENVIRONMENT = "production"

# Limits
workers_dev = true
route = { pattern = "api.sales.example.com/*", zone_name = "example.com" }
```

### 5. Database Schema (D1)

```sql
-- src/db/schema.sql

CREATE TABLE shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logo_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_normalized_name ON products(normalized_name);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    shop_id INTEGER NOT NULL,
    price REAL,
    price_text TEXT,
    original_price REAL,
    discount_percent INTEGER,
    valid_from DATE,
    valid_until DATE,
    validity_text TEXT,
    source_url TEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (shop_id) REFERENCES shops(id)
);

CREATE INDEX idx_product_shop ON sales(product_id, shop_id);
CREATE INDEX idx_valid_dates ON sales(valid_from, valid_until);

-- Seed shops
INSERT INTO shops (slug, name) VALUES
    ('lidl', 'Lidl'),
    ('penny-market', 'Penny Market'),
    ('billa', 'Billa'),
    ('kaufland', 'Kaufland');
```

Apply schema:
```bash
wrangler d1 execute sales-db --file=./src/db/schema.sql
```

## Code Example (Hono)

```typescript
// src/index.ts
import { Hono } from 'hono'
import { cors } from 'hono/cors'

type Bindings = {
  DB: D1Database
}

const app = new Hono<{ Bindings: Bindings }>()

app.use('/*', cors())

// Search products
app.get('/api/products/search', async (c) => {
  const query = c.req.query('q')
  const shop = c.req.query('shop')
  
  if (!query || query.length < 2) {
    return c.json({ error: 'Query too short' }, 400)
  }
  
  const normalized = query.toLowerCase()
  
  let sql = `
    SELECT p.*, s.name as sale_price, sh.name as shop_name
    FROM products p
    LEFT JOIN sales s ON p.id = s.product_id
    LEFT JOIN shops sh ON s.shop_id = sh.id
    WHERE p.normalized_name LIKE ?
  `
  
  const params = [`%${normalized}%`]
  
  if (shop) {
    sql += ' AND sh.slug = ?'
    params.push(shop)
  }
  
  const { results } = await c.env.DB.prepare(sql)
    .bind(...params)
    .all()
  
  return c.json({ results })
})

// Cron job (scraping)
export default {
  async fetch(request: Request, env: any) {
    return app.fetch(request, env)
  },
  
  async scheduled(event: ScheduledEvent, env: any) {
    console.log('Running scraper...')
    // TODO: Implement scraping logic
    // await scrapeAllShops(env.DB)
  }
}
```

## Deployment

```bash
# Deploy to Cloudflare
wrangler deploy

# Test locally
wrangler dev

# Tail logs
wrangler tail
```

## Cost Estimate (Free Tier)

| Service | Free Tier | Cost if exceeded |
|---------|-----------|------------------|
| Workers | 100k req/day | $0.50 per million |
| D1 Database | 100k reads/day | $0.001 per 1k reads |
| Cron Triggers | Included | Free |
| Workers AI (optional) | 10k neurons/day | Pay as you go |

**→ Likely FREE for MVP! 🎉**

## Advantages

✅ **Zero ops** - no server management  
✅ **Fast** - edge deployment, low latency  
✅ **Scalable** - auto-scales globally  
✅ **Cheap** - free tier je dost velkorysý  
✅ **Simple** - TypeScript, modern stack  

## Limitations

⚠️ **CPU time** - max 50ms per request (can be tight for scraping)  
⚠️ **Memory** - 128MB limit  
⚠️ **Scraping** - heavy scraping může být problém (use cron wisely)  
⚠️ **D1 writes** - 1MB max per transaction  

**Solution:** Scrape slowly over time (spread across multiple cron runs).

## Migration from FastAPI

Keep existing Python scraper:
- Run locally nebo jako GitHub Action
- Push scraped data to CF via API
- CF Workers pouze serve data

Or:
- Rewrite scraper in TypeScript (Cloudflare Workers compatible)
- Use `fetch()` for HTTP, Cheerio for parsing

---

## Next Steps

1. [ ] Setup Wrangler + CF account
2. [ ] Create D1 database
3. [ ] Port models to SQL schema
4. [ ] Implement Hono routes
5. [ ] Add scraper cron job
6. [ ] Deploy & test

**Estimated time:** 2-3 heartbeat sessions 🦉

-- Sales API Database Schema

-- Shops
CREATE TABLE IF NOT EXISTS shops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logo_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_normalized_name ON products(normalized_name);

-- Sales
CREATE TABLE IF NOT EXISTS sales (
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

CREATE INDEX IF NOT EXISTS idx_product_shop ON sales(product_id, shop_id);
CREATE INDEX IF NOT EXISTS idx_valid_dates ON sales(valid_from, valid_until);

-- Seed shops
INSERT OR IGNORE INTO shops (slug, name) VALUES
    ('lidl', 'Lidl'),
    ('penny-market', 'Penny Market'),
    ('billa', 'Billa'),
    ('kaufland', 'Kaufland');

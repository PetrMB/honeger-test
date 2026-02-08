import { Hono } from 'hono'
import { cors } from 'hono/cors'

const app = new Hono()

// CORS middleware
app.use('/*', cors())

// Root endpoint
app.get('/', (c) => {
  return c.json({
    service: 'Sales API',
    version: '0.1.0',
    status: 'ok',
    endpoints: {
      search: '/api/products/search?q=mleko',
      shops: '/api/shops',
      stats: '/api/stats'
    }
  })
})

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'healthy' })
})

// Stats endpoint
app.get('/api/stats', async (c) => {
  const db = c.env.DB
  
  try {
    const { results: productCount } = await db.prepare(
      'SELECT COUNT(*) as count FROM products'
    ).all()
    
    const { results: salesCount } = await db.prepare(
      'SELECT COUNT(*) as count FROM sales'
    ).all()
    
    const { results: shops } = await db.prepare(
      'SELECT * FROM shops'
    ).all()
    
    return c.json({
      totalProducts: productCount[0]?.count || 0,
      activeSales: salesCount[0]?.count || 0,
      shops: shops.length,
      shopsAvailable: shops.map(s => ({ slug: s.slug, name: s.name })),
      lastUpdate: new Date().toISOString()
    })
  } catch (err) {
    return c.json({ error: err.message }, 500)
  }
})

// List shops
app.get('/api/shops', async (c) => {
  const db = c.env.DB
  
  try {
    const { results } = await db.prepare(
      'SELECT * FROM shops ORDER BY name'
    ).all()
    
    return c.json({ shops: results })
  } catch (err) {
    return c.json({ error: err.message }, 500)
  }
})

// Search products
app.get('/api/products/search', async (c) => {
  const query = c.req.query('q')
  const shop = c.req.query('shop')
  const limit = parseInt(c.req.query('limit') || '20')
  
  if (!query || query.length < 2) {
    return c.json({ error: 'Query too short (min 2 chars)' }, 400)
  }
  
  const db = c.env.DB
  const normalized = query.toLowerCase()
  
  try {
    let sql = `
      SELECT 
        p.id, 
        p.name, 
        p.category,
        s.price,
        s.price_text,
        s.discount_percent,
        s.valid_until,
        sh.name as shop_name,
        sh.slug as shop_slug
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
    
    sql += ` LIMIT ${limit}`
    
    const { results } = await db.prepare(sql).bind(...params).all()
    
    return c.json({ 
      query,
      shop,
      results,
      count: results.length 
    })
  } catch (err) {
    return c.json({ error: err.message }, 500)
  }
})

// Cron trigger for scraping (scheduled event)
export default {
  async fetch(request, env, ctx) {
    return app.fetch(request, env, ctx)
  },
  
  async scheduled(event, env, ctx) {
    console.log('🕐 Cron trigger fired:', new Date().toISOString())
    // TODO: Implement scraping logic here
    // For now, just log
    console.log('Scraping would run here...')
  }
}

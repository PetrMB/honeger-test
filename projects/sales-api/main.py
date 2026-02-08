"""
Sales API - Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import products, shops, sales, stats

app = FastAPI(
    title="Sales API",
    description="API pro akční ceny produktů z českých obchodů",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (pro frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # V produkci změnit na konkrétní domény
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(shops.router, prefix="/api/shops", tags=["shops"])
app.include_router(sales.router, prefix="/api/sales", tags=["sales"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Sales API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Health check for monitoring"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

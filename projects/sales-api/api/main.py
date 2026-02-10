from fastapi import APIRouter

from api.routes import products, shops, stats

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(shops.router, prefix="/shops", tags=["shops"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])


@api_router.get("/")
async def root():
    return {"message": "Sales API", "version": "0.1.0"}


@api_router.get("/health")
async def health():
    return {"status": "ok"}

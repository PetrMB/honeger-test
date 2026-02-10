"""API routes package."""

from api.routes.products import router as products_router
from api.routes.shops import router as shops_router
from api.routes.stats import router as stats_router

__all__ = ["products_router", "shops_router", "stats_router"]

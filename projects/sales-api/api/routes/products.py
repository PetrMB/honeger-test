"""Sales API APIs for products."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import Product, Sale, Shop, PriceHistory

router = APIRouter()


@router.get("/search")
async def search_products(
    q: str = Query(..., description="Search query"),
    shop: Optional[str] = Query(None, description="Filter by shop slug"),
    limit: int = Query(20, le=50, description="Maximum results")
):
    """Search products by name with fuzzy matching."""
    # TODO: Implement fuzzy search
    return {
        "query": q,
        "shop": shop,
        "limit": limit,
        "results": []  # Placeholder
    }


@router.get("/{product_id}")
async def get_product(product_id: int):
    """Get product details with current sales."""
    return {
        "id": product_id,
        "name": "Product name",
        "sales": []
    }

"""Products API endpoints"""
from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter()

@router.get("/search")
async def search_products(
    q: str = Query(..., min_length=2, description="Search query"),
    shop: Optional[str] = Query(None, description="Filter by shop slug"),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Search for products by name (fuzzy matching)
    """
    # TODO: Implement fuzzy search
    return {
        "query": q,
        "shop": shop,
        "results": [],
        "count": 0
    }

@router.get("/{product_id}")
async def get_product(product_id: int):
    """
    Get product details with current sales
    """
    # TODO: Implement product detail
    return {
        "id": product_id,
        "name": "Example Product",
        "sales": []
    }

@router.get("/{product_id}/history")
async def get_price_history(product_id: int, days: int = Query(30, ge=1, le=365)):
    """
    Get price history for a product
    """
    # TODO: Implement price history
    return {
        "productId": product_id,
        "history": []
    }

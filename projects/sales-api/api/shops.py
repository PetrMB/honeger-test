"""Shops API endpoints"""
from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/")
async def list_shops():
    """
    List all available shops
    """
    # TODO: Implement shop listing
    return {
        "shops": [
            {"slug": "lidl", "name": "Lidl"},
            {"slug": "penny-market", "name": "Penny Market"},
            {"slug": "billa", "name": "Billa"},
            {"slug": "kaufland", "name": "Kaufland"}
        ]
    }

@router.get("/{shop_slug}/sales")
async def get_shop_sales(
    shop_slug: str,
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200)
):
    """
    Get all current sales for a shop
    """
    # TODO: Implement shop sales
    return {
        "shop": shop_slug,
        "category": category,
        "sales": []
    }

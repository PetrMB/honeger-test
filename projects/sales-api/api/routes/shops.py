"""Sales API APIs for shops."""

from fastapi import APIRouter
from typing import List

router = APIRouter()


@router.get("/")
async def list_shops():
    """List all supported shops."""
    return [
        {"slug": "lidl", "name": "Lidl"},
        {"slug": "penny", "name": "Penny Market"},
        {"slug": "kaufland", "name": "Kaufland"},
        {"slug": "billa", "name": "Billa"},
    ]


@router.get("/{shop_slug}")
async def get_shop(shop_slug: str):
    """Get shop details."""
    return {
        "slug": shop_slug,
        "name": "Shop name"
    }

"""Sales API APIs for statistics."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_stats():
    """Get API statistics."""
    return {
        "total_products": 0,
        "active_sales": 0,
        "shops": 4,
        "last_update": None
    }

"""Sales API endpoints"""
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/recent")
async def get_recent_sales(limit: int = Query(50, ge=1, le=200)):
    """
    Get recently added sales (feed)
    """
    # TODO: Implement recent sales feed
    return {
        "sales": [],
        "count": 0
    }

@router.get("/top-deals")
async def get_top_deals(limit: int = Query(20, ge=1, le=100)):
    """
    Get top deals by discount percentage
    """
    # TODO: Implement top deals
    return {
        "deals": []
    }

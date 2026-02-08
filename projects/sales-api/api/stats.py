"""Stats API endpoints"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_stats():
    """
    Get overall service statistics
    """
    # TODO: Implement real stats from database
    return {
        "totalProducts": 0,
        "activeSales": 0,
        "shops": 4,
        "lastUpdate": datetime.now().isoformat()
    }

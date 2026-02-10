"""Sales API Scheduler for scraping jobs."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import asyncio

scheduler = AsyncIOScheduler()


@scheduler.scheduled_job('interval', hours=6)
async def scrape_all_shops():
    """
    Scheduled job to scrape all configured shops.
    Runs every 6 hours.
    """
    from scraper.extractors.akcniceny import AkcnicenyExtractor
    
    print(f"[{datetime.now()}] Starting scheduled scrape...")
    
    extractor = AkcnicenyExtractor()
    all_deals = await extractor.scrape_all()
    
    print(f"[{datetime.now()}] Found {len(all_deals)} deals")
    
    # TODO: Save to database
    # await save_to_database(all_deals)


def start_scheduler():
    """Start the scheduler."""
    scheduler.start()
    print(f"[{datetime.now()}] Scheduler started")
    print("Next scrape in 6 hours")


def stop_scheduler():
    """Stop the scheduler."""
    scheduler.shutdown()
    print(f"[{datetime.now()}] Scheduler stopped")


if __name__ == "__main__":
    try:
        start_scheduler()
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        stop_scheduler()

#!/usr/bin/env python3
"""Initialize database and seed shops."""

import asyncio
import(asyncio)

from models.database import Base, Shop, SessionLocal, engine

# SQLite connection string
SQLITE_URL = "sqlite+aiosqlite:///sales.db"


async def init_db():
    """Create database tables."""
    from sqlalchemy.ext.asyncio import create_async_engine
    
    engine = create_async_engine(SQLITE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database initialized")


async def seed_shops():
    """Seed shops into database."""
    from sqlalchemy.ext.asyncio import AsyncSession
    
    shops = [
        {"slug": "lidl", "name": "Lidl", "logo_url": None},
        {"slug": "penny", "name": "Penny Market", "logo_url": None},
        {"slug": "kaufland", "name": "Kaufland", "logo_url": None},
        {"slug": "billa", "name": "Billa", "logo_url": None},
    ]
    
    # TODO: Implement async session
    print("Shops ready to seed")


async def main():
    """Main entry point."""
    await init_db()
    await seed_shops()
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())

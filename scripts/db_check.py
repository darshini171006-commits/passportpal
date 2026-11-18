"""Check that DATABASE_URL in .env works.

Run: uv run python scripts/db_check.py
"""

import asyncio

from sqlalchemy import text

from passportpal.config import get_settings
from passportpal.db.session import make_engine


async def main() -> None:
    engine = make_engine(get_settings())

    try:
        async with engine.connect() as conn:
            version = await conn.scalar(text("SELECT version()"))

            database = await conn.scalar(text("SELECT current_database()"))

        print("Database connection successful!")
        print(f"PostgreSQL version: {version}")
        print(f"Database name: {database}")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

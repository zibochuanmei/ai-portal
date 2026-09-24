import asyncio

from app.db.session import ping_database


def test_database_ping() -> None:
    asyncio.run(ping_database())

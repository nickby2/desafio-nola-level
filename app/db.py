import os
from databases import Database

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://challenge:challenge_2024@localhost:5432/challenge_db",
)

database = Database(DATABASE_URL)


async def connect():
    if not database.is_connected:
        await database.connect()


async def disconnect():
    if database.is_connected:
        await database.disconnect()

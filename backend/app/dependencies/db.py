from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.database import get_db

async def get_database() -> AsyncIOMotorDatabase:
    """
    FastAPI dependency that injects the active MongoDB database.

    Usage:
        @router.get("/example")
        async def example(db: AsyncIOMotorDatabase = Depends(get_database)):
            ...
    """
    return get_db()

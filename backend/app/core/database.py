from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Global client and db references
mongo_client: AsyncIOMotorClient = None
db = None

async def connect_db():
    """Create MongoDB Atlas connection on app startup."""
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
    db = mongo_client[settings.MONGO_DB_NAME]
    # Verify connection
    await mongo_client.admin.command("ping")
    print(f"✅ MongoDB Atlas connected → database: '{settings.MONGO_DB_NAME}'")

async def close_db():
    """Close MongoDB connection on app shutdown."""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("🔌 MongoDB connection closed.")

def get_db():
    """Return the active database instance."""
    return db
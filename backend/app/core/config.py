import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB_NAME: str = "aether_elearning"

    RAZORPAY_KEY_ID: str
    RAZORPAY_KEY_SECRET: str
    SENDGRID_API_KEY: str = ""

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        extra = "ignore"

settings = Settings()

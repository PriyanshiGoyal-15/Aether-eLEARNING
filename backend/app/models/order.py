from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class OrderDocument(BaseModel):
    """MongoDB document model for a Razorpay order."""
    id: str = Field(..., description="Razorpay order ID")
    courseId: str
    courseTitle: str
    userId: str
    userName: str
    amount: int
    currency: str = "INR"
    status: str = "created"  # created | paid | failed
    paidAt: Optional[str] = None
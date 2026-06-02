from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentDocument(BaseModel):
    """MongoDB document model for a captured Razorpay payment."""
    id: str = Field(..., description="Razorpay payment ID (e.g. pay_xxxxxxxx)")
    orderId: str
    courseId: str
    userId: str
    amount: int
    currency: str = "INR"
    status: str  # captured | failed | refunded
    method: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    teacherRevenue: int = 0
    adminRevenue: int = 0
    capturedAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
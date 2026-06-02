from pydantic import BaseModel
from typing import Optional

class CreateOrderRequest(BaseModel):
    courseId: str
    courseTitle: str
    userId: str
    userName: str
    amount: int       # in paise
    currency: str = "INR"

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    courseId: str
    userId: str

class CreateOrderResponse(BaseModel):
    orderId: str
    amount: int
    currency: str
    keyId: str

class PaymentVerifyResponse(BaseModel):
    success: bool
    message: str
    paymentId: Optional[str] = None
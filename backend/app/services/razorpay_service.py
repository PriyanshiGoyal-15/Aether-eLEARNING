import razorpay
 
from app.core.config import settings
 
 
class RazorpayService:
 
    def __init__(self):

        self.client = razorpay.Client(

            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )
 
    def create_order(
        self,
        amount: int
    ):
        return self.client.order.create(
            {
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            }
        )
 
    def verify_signature(
        self,
        payload: dict
    ):

        self.client.utility.verify_payment_signature(
            payload
        )
        return True
 
razorpay_service = RazorpayService()
 
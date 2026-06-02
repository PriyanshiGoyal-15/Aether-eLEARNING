from pydantic import BaseModel

class ReviewSubmitRequest(BaseModel):
    studentName: str
    rating: float
    comment: str

class NotificationRequest(BaseModel):
    userId: str
    title: str
    message: str
    type: str = "info"

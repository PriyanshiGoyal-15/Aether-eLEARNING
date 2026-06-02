import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

logger = logging.getLogger(__name__)

# Replace this with the verified sender identity from your SendGrid dashboard
SENDER_EMAIL = "genxLearning@gmail.com" 

async def send_email(
    db: AsyncIOMotorDatabase,
    to_email: str,
    subject: str,
    body: str,
    recipient_id: str = None
):
    """
    Sends a real email using SendGrid and logs it to the MongoDB 'emails' collection.
    """
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    
    status = "delivered_mock"
    try:
        # If API key is present, send via SendGrid
        if settings.SENDGRID_API_KEY:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(f"--- SENDGRID EMAIL SENT to {to_email} --- Status: {response.status_code}")
            status = "delivered"
        else:
            logger.info(f"--- MOCK EMAIL SENT to {to_email} --- (No API Key found)")
            
    except Exception as e:
        logger.error(f"Failed to send email via SendGrid: {e}")
        status = "failed"

    # Log to database
    email_doc = {
        "to": to_email,
        "subject": subject,
        "body": body,
        "userId": recipient_id,
        "sentAt": datetime.utcnow().isoformat(),
        "status": status
    }
    try:
        await db.emails.insert_one(email_doc)
    except Exception as e:
        logger.error(f"Failed to log email to DB: {e}")

async def send_welcome_email(db: AsyncIOMotorDatabase, student_email: str, student_name: str, course_title: str, student_id: str = None):
    subject = f"Welcome to {course_title}! 🎓"
    body = f"Hi {student_name},\n\nYou have successfully enrolled in '{course_title}'. We are excited to have you on board! You can start learning immediately from your dashboard.\n\nHappy Learning,\nThe Aether Team"
    
    await send_email(db, student_email, subject, body, student_id)

async def send_teacher_sale_notification(db: AsyncIOMotorDatabase, teacher_email: str, teacher_name: str, course_title: str, amount: int, teacher_id: str = None):
    subject = f"Cha-Ching! You made a sale for {course_title} 💰"
    body = f"Hi {teacher_name},\n\nGreat news! A student just purchased your premium course '{course_title}'.\nYour estimated revenue from this sale is ₹{amount / 100:.2f}.\n\nKeep up the great work,\nThe Aether Team"
    
    await send_email(db, teacher_email, subject, body, teacher_id)

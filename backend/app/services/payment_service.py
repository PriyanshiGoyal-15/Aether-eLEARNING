from datetime import datetime
from fastapi import HTTPException, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.order import OrderDocument
from app.models.payment import PaymentDocument
from app.schemas.payment import CreateOrderRequest, VerifyPaymentRequest
from app.services.razorpay_service import razorpay_service
from app.core.config import settings
from app.services.email_service import send_teacher_sale_notification

async def create_order(req: CreateOrderRequest, db: AsyncIOMotorDatabase) -> dict:
    rz_order = razorpay_service.create_order(req.amount)
    
    order_doc = OrderDocument(
        id=rz_order["id"],
        courseId=req.courseId,
        courseTitle=req.courseTitle,
        userId=req.userId,
        userName=req.userName,
        amount=req.amount,
        currency=req.currency,
        status="created",
    )
    await db.orders.insert_one(order_doc.model_dump())

    return {
        "orderId": rz_order["id"],
        "amount": req.amount,
        "currency": req.currency,
        "keyId": settings.RAZORPAY_KEY_ID,
    }

async def verify_and_capture_payment(req: VerifyPaymentRequest, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase) -> dict:
    is_valid = razorpay_service.verify_signature({
        "razorpay_order_id": req.razorpay_order_id,
        "razorpay_payment_id": req.razorpay_payment_id,
        "razorpay_signature": req.razorpay_signature
    })

    if not is_valid:
        await db.orders.update_one({"id": req.razorpay_order_id}, {"$set": {"status": "failed"}})
        raise HTTPException(status_code=400, detail="Invalid signature.")

    await db.orders.update_one(
        {"id": req.razorpay_order_id},
        {"$set": {"status": "paid", "paidAt": datetime.utcnow().isoformat()}}
    )

    order = await db.orders.find_one({"id": req.razorpay_order_id})
    amount = order["amount"] if order else 0
    admin_revenue = int(amount * 0.3)
    teacher_revenue = amount - admin_revenue

    payment_doc = PaymentDocument(
        id=req.razorpay_payment_id,
        orderId=req.razorpay_order_id,
        courseId=req.courseId,
        userId=req.userId,
        amount=amount,
        currency=order["currency"] if order else "INR",
        status="captured",
        adminRevenue=admin_revenue,
        teacherRevenue=teacher_revenue
    )
    await db.payments.insert_one(payment_doc.model_dump())

    # Send teacher email
    course = await db.courses.find_one({"id": req.courseId})
    if course:
        teacher_id = course.get("teacherId")
        teacher = await db.users.find_one({"id": teacher_id})
        if teacher:
            background_tasks.add_task(
                send_teacher_sale_notification,
                db,
                teacher["email"],
                teacher["name"],
                course["title"],
                teacher_revenue,
                teacher_id
            )

    return {
        "success": True,
        "message": "Payment verified and captured successfully.",
        "paymentId": req.razorpay_payment_id,
    }
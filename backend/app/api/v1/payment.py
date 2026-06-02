from fastapi import APIRouter, Depends, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.payment import CreateOrderRequest, CreateOrderResponse, VerifyPaymentRequest, PaymentVerifyResponse
from app.services.payment_service import create_order, verify_and_capture_payment
from app.dependencies.db import get_database

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/create-order", response_model=CreateOrderResponse)
async def create_payment_order(req: CreateOrderRequest, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await create_order(req, db)

@router.post("/verify", response_model=PaymentVerifyResponse)
async def verify_payment(req: VerifyPaymentRequest, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_database)):
    return await verify_and_capture_payment(req, background_tasks, db)
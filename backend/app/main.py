import os
import time
from datetime import datetime
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from app.core.database import connect_db, close_db, get_db
from app.api.v1.payment import router as payment_router

INITIAL_USERS = [
    {
        "id": "user-student",
        "email": "student@aether.edu",
        "password": "student123",
        "name": "Priyanshi Sharma",
        "role": "student",
        "suspended": False,
        "streakCount": 5,
        "joinedDate": "2026-01-15",
        "verificationStatus": "approved"
    },
    {
        "id": "user-teacher",
        "email": "teacher@aether.edu",
        "password": "teacher123",
        "name": "Dr. Sarah Jenkins",
        "role": "teacher",
        "suspended": False,
        "joinedDate": "2025-11-10",
        "verificationStatus": "approved"
    },
    {
        "id": "user-admin",
        "email": "admin@aether.edu",
        "password": "admin123",
        "name": "Chief Administrator",
        "role": "admin",
        "suspended": False,
        "joinedDate": "2025-09-01",
        "verificationStatus": "approved"
    }
]

INITIAL_COURSES = [
    {
        "id": "course-vue",
        "title": "Mastering Vue 3: From Zero to Hero",
        "description": "Learn Vue 3, Vue Router, Pinia, Composition API, and modern SPA design.",
        "shortDescription": "Master reactive SPA development with Vue 3.",
        "category": "Development",
        "difficulty": "Intermediate",
        "thumbnail": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=600&q=80",
        "teacherId": "user-teacher",
        "teacherName": "Dr. Sarah Jenkins",
        "status": "approved",
        "rating": 4.8,
        "reviewsCount": 2,
        "studentsCount": 1250,
        "duration": "4.5 Hours",
        "rejectionReason": "",
        "price": 49900,
        "modules": [],
        "learningOutcomes": [
            "Scaffold dynamic responsive layouts using Vue framework modules",
            "Understand responsive components, models, and data-flows",
            "Implement secure access configurations and routing limits",
            "Create full modular portfolios with clean, production code standards"
        ]
    }
]

INITIAL_ENROLLMENTS = []
INITIAL_REVIEWS = []
INITIAL_NOTIFS = []

def strip_id(doc: dict) -> dict:
    if doc:
        doc.pop("_id", None)
    return doc

def strip_ids(docs: list) -> list:
    return [strip_id(doc) for doc in docs]

async def seed_initial_data():
    db = get_db()
    if await db.users.count_documents({}) == 0:
        await db.users.insert_many([dict(u) for u in INITIAL_USERS])
    if await db.courses.count_documents({}) == 0:
        await db.courses.insert_many([dict(c) for c in INITIAL_COURSES])
    if await db.enrollments.count_documents({}) == 0 and INITIAL_ENROLLMENTS:
        await db.enrollments.insert_many([dict(e) for e in INITIAL_ENROLLMENTS])
    if await db.reviews.count_documents({}) == 0 and INITIAL_REVIEWS:
        await db.reviews.insert_many([dict(r) for r in INITIAL_REVIEWS])
    if await db.notifications.count_documents({}) == 0 and INITIAL_NOTIFS:
        await db.notifications.insert_many([dict(n) for n in INITIAL_NOTIFS])

async def add_notification_helper(user_id: str, title: str, message: str, type_str: str = "info"):
    db = get_db()
    await db.notifications.insert_one({
        "id": f"not-{int(time.time() * 1000)}",
        "userId": user_id,
        "title": title,
        "message": message,
        "type": type_str,
        "read": False,
        "date": datetime.today().strftime('%Y-%m-%d')
    })

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    await seed_initial_data()
    yield
    await close_db()

app = FastAPI(title="Aether E-Learning API", lifespan=lifespan)

import uuid
import shutil
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles

# Create upload directory inside backend/static/uploads
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
UPLOAD_DIR = os.path.join(STATIC_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    url = f"http://localhost:8000/static/uploads/{unique_filename}"
    return {"url": url, "filename": file.filename}

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://aether-elearning-1.onrender.com",
    "https://aether-elearning.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https://.*\\.onrender\\.com|http://localhost:.*|http://127\\.0\\.0\\.1:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payment_router, prefix="/api/v1")

from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.course import CreateCourseRequest, RejectCourseRequest, CreateModuleSchema, CreateLessonSchema
from app.schemas.common import ReviewSubmitRequest, NotificationRequest
from app.services.email_service import send_welcome_email

@app.get("/api/db")
async def get_entire_db():
    db = get_db()
    return {
        "users": strip_ids(await db.users.find().to_list(None)),
        "courses": strip_ids(await db.courses.find().to_list(None)),
        "enrollments": strip_ids(await db.enrollments.find().to_list(None)),
        "bookmarks": strip_ids(await db.bookmarks.find().to_list(None)),
        "reviews": strip_ids(await db.reviews.find(sort=[("_id", -1)]).to_list(None)),
        "notifications": strip_ids(await db.notifications.find(sort=[("_id", -1)]).to_list(None)),
        "payments": strip_ids(await db.payments.find().to_list(None)),
        "emails": strip_ids(await db.emails.find(sort=[("_id", -1)]).to_list(None)),
    }

@app.post("/api/auth/login")
async def login(req: LoginRequest):
    db = get_db()
    user = strip_id(await db.users.find_one({"email": req.email.lower()}))
    if not user or user.get("password") != req.password:
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    return user

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    db = get_db()
    exists = await db.users.find_one({"email": req.email.lower()})
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists.")
    new_user = {
        "id": f"user-{int(time.time() * 1000)}",
        "name": req.name,
        "email": req.email.lower(),
        "password": req.password,
        "role": req.role,
        "suspended": False,
        "joinedDate": datetime.today().strftime('%Y-%m-%d'),
        "verificationStatus": "pending" if req.role == "teacher" else "approved"
    }
    await db.users.insert_one(new_user)
    return strip_id(new_user)

@app.post("/api/users/{user_id}/suspend")
async def toggle_suspension(user_id: str):
    db = get_db()
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404)
    new_suspended = not user.get("suspended", False)
    await db.users.update_one({"id": user_id}, {"$set": {"suspended": new_suspended}})
    return {"status": "success", "suspended": new_suspended}

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str):
    db = get_db()
    await db.users.delete_one({"id": user_id})
    return {"status": "success"}

@app.post("/api/courses")
async def create_course(req: CreateCourseRequest):
    db = get_db()
    new_course = {
        "id": f"course-{int(time.time() * 1000)}",
        "title": req.title,
        "description": req.description,
        "shortDescription": req.description[:80] + "...",
        "category": req.category,
        "difficulty": req.difficulty,
        "thumbnail": req.thumbnail,
        "teacherId": req.teacherId,
        "teacherName": req.teacherName,
        "status": "pending",
        "rating": 5.0,
        "reviewsCount": 0,
        "studentsCount": 0,
        "duration": "Flexible",
        "rejectionReason": "",
        "price": req.price or 0,
        "modules": [mod.model_dump() for mod in req.modules],
        "learningOutcomes": req.learningOutcomes or []
    }
    await db.courses.insert_one(new_course)
    return strip_id(new_course)

@app.put("/api/courses/{course_id}")
async def update_course(course_id: str, req: CreateCourseRequest):
    db = get_db()
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = {
        "title": req.title,
        "description": req.description,
        "shortDescription": req.description[:80] + "...",
        "category": req.category,
        "difficulty": req.difficulty,
        "thumbnail": req.thumbnail,
        "price": req.price or 0,
        "modules": [mod.model_dump() for mod in req.modules],
        "learningOutcomes": req.learningOutcomes or [],
        "status": "pending",
        "rejectionReason": ""
    }
    
    await db.courses.update_one({"id": course_id}, {"$set": update_data})
    updated_course = await db.courses.find_one({"id": course_id})
    return strip_id(updated_course)

@app.post("/api/courses/{course_id}/approve")
async def approve_course(course_id: str):
    db = get_db()
    await db.courses.update_one({"id": course_id}, {"$set": {"status": "approved", "rejectionReason": ""}})
    return {"status": "approved"}

@app.post("/api/courses/{course_id}/reject")
async def reject_course(course_id: str, req: RejectCourseRequest):
    db = get_db()
    await db.courses.update_one({"id": course_id}, {"$set": {"status": "rejected", "rejectionReason": req.reason}})
    return {"status": "rejected"}

@app.post("/api/courses/{course_id}/enroll")
async def enroll_in_course(course_id: str, studentId: str, background_tasks: BackgroundTasks):
    db = get_db()
    
    # Need student and course info for email
    student = await db.users.find_one({"id": studentId})
    course = await db.courses.find_one({"id": course_id})
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
        
    exists = await db.enrollments.find_one({"studentId": studentId, "courseId": course_id})
    if exists:
        return {"status": "already_enrolled"}
    new_enroll = {
        "id": f"enroll-{int(time.time() * 1000)}",
        "studentId": studentId,
        "courseId": course_id,
        "completedLessons": [],
        "progressPercent": 0,
        "enrolledDate": datetime.today().strftime('%Y-%m-%d')
    }
    await db.courses.update_one({"id": course_id}, {"$inc": {"studentsCount": 1}})
    await db.enrollments.insert_one(new_enroll)
    
    # Trigger background email
    background_tasks.add_task(
        send_welcome_email, 
        db, 
        student["email"], 
        student["name"], 
        course["title"], 
        studentId
    )
    
    return strip_id(new_enroll)

@app.post("/api/courses/{course_id}/lesson-toggle")
async def toggle_lesson(course_id: str, studentId: str, lessonId: str):
    db = get_db()
    course = await db.courses.find_one({"id": course_id})
    enrollment = await db.enrollments.find_one({"studentId": studentId, "courseId": course_id})
    
    total_lessons = sum(len(module["lessons"]) for module in course["modules"])
    completed = list(enrollment.get("completedLessons", []))
    
    if lessonId in completed:
        completed.remove(lessonId)
    else:
        completed.append(lessonId)
        
    progress = int(round((len(completed) / total_lessons) * 100)) if total_lessons > 0 else 0
    update_op = {"$set": {"completedLessons": completed, "progressPercent": progress}}
    if progress == 100:
        update_op["$set"]["completedDate"] = datetime.today().strftime('%Y-%m-%d')
    else:
        update_op["$unset"] = {"completedDate": ""}
        
    await db.enrollments.update_one({"studentId": studentId, "courseId": course_id}, update_op)
    return strip_id(await db.enrollments.find_one({"studentId": studentId, "courseId": course_id}))

@app.post("/api/courses/{course_id}/auto-complete")
async def auto_complete_course(course_id: str, studentId: str):
    db = get_db()
    course = await db.courses.find_one({"id": course_id})
    all_lessons = [les["id"] for mod in course["modules"] for les in mod["lessons"]]
    await db.enrollments.update_one(
        {"studentId": studentId, "courseId": course_id},
        {"$set": {"completedLessons": all_lessons, "progressPercent": 100, "completedDate": datetime.today().strftime('%Y-%m-%d')}}
    )
    return strip_id(await db.enrollments.find_one({"studentId": studentId, "courseId": course_id}))

@app.post("/api/courses/{course_id}/bookmark")
async def toggle_bookmark(course_id: str, studentId: str):
    db = get_db()
    existing = await db.bookmarks.find_one({"studentId": studentId, "courseId": course_id})
    if existing:
        await db.bookmarks.delete_one({"studentId": studentId, "courseId": course_id})
        return {"status": "success", "action": "removed"}
    await db.bookmarks.insert_one({"studentId": studentId, "courseId": course_id})
    return {"status": "success", "action": "added"}

@app.post("/api/courses/{course_id}/reviews")
async def submit_review(course_id: str, req: ReviewSubmitRequest):
    db = get_db()
    new_rev = {"id": f"rev-{int(time.time() * 1000)}", "courseId": course_id, "studentName": req.studentName, "rating": float(req.rating), "comment": req.comment, "date": datetime.today().strftime('%Y-%m-%d')}
    await db.reviews.insert_one(new_rev)
    
    all_reviews = await db.reviews.find({"courseId": course_id}).to_list(None)
    new_avg = round(sum(r["rating"] for r in all_reviews) / len(all_reviews), 1)
    await db.courses.update_one({"id": course_id}, {"$set": {"rating": new_avg, "reviewsCount": len(all_reviews)}})
    return strip_id(new_rev)

@app.post("/api/notifications/read")
async def read_notifications(userId: str):
    db = get_db()
    await db.notifications.update_many({"userId": userId}, {"$set": {"read": True}})
    return {"status": "success"}

@app.post("/api/notifications")
async def add_notification(req: NotificationRequest):
    await add_notification_helper(req.userId, req.title, req.message, req.type)
    return {"status": "success"}

@app.post("/api/system/reset")
async def reset_database():
    db = get_db()
    for col in ["users", "courses", "enrollments", "bookmarks", "reviews", "notifications", "emails", "orders", "payments"]:
        await db[col].drop()
    await seed_initial_data()
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
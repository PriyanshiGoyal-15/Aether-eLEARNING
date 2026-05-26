import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI App
app = FastAPI(title="Aether E-Learning Backend API", version="1.0.0")

# Enable CORS for Vue Frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = os.path.join(os.path.dirname(__file__), "db.json")

# Initial Mock Data
INITIAL_USERS = [
    {
        "id": "user-student",
        "email": "student@aether.edu",
        "password": "student123",
        "name": "Priyanshi Sharma",
        "role": "student",
        "suspended": False,
        "streakCount": 5,
        "joinedDate": "2026-01-15"
    },
    {
        "id": "user-teacher",
        "email": "teacher@aether.edu",
        "password": "teacher123",
        "name": "Dr. Sarah Jenkins",
        "role": "teacher",
        "suspended": False,
        "joinedDate": "2025-11-10"
    },
    {
        "id": "user-admin",
        "email": "admin@aether.edu",
        "password": "admin123",
        "name": "Chief Administrator",
        "role": "admin",
        "suspended": False,
        "joinedDate": "2025-09-01"
    }
]

INITIAL_COURSES = [
    {
        "id": "course-vue",
        "title": "Mastering Vue 3: From Zero to Hero",
        "description": "Learn Vue 3, Vue Router, Pinia, Composition API, and modern SPA design using Tailwind CSS. Create beautiful dynamic user interfaces and scale them efficiently.",
        "shortDescription": "Master reactive SPA development with Vue 3 and modern design systems.",
        "category": "Development",
        "difficulty": "Intermediate",
        "thumbnail": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?auto=format&fit=crop&w=600&q=80",
        "teacherId": "user-teacher",
        "teacherName": "Dr. Sarah Jenkins",
        "status": "approved",
        "rating": 4.8,
        "reviewsCount": 124,
        "studentsCount": 1250,
        "duration": "4.5 Hours",
        "rejectionReason": "",
        "modules": [
            {
                "id": "mod-vue-1",
                "title": "Module 1: Introduction & App Setup",
                "lessons": [
                    {
                        "id": "vue-1-1",
                        "title": "1. Welcome & Scaffold Vite Project",
                        "type": "video",
                        "url": "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
                        "duration": "10:15",
                        "completed": False
                    },
                    {
                        "id": "vue-1-2",
                        "title": "2. Setting up Tailwind CSS & Google Fonts",
                        "type": "pdf",
                        "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                        "duration": "Reading Guide (5 mins)",
                        "completed": False
                    }
                ]
            },
            {
                "id": "mod-vue-2",
                "title": "Module 2: Reactivity & Composition API",
                "lessons": [
                    {
                        "id": "vue-2-1",
                        "title": "3. Understanding ref(), reactive(), and computed()",
                        "type": "video",
                        "url": "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
                        "duration": "18:42",
                        "completed": False
                    },
                    {
                        "id": "vue-2-2",
                        "title": "4. Component Props, Emits & Custom Events",
                        "type": "video",
                        "url": "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
                        "duration": "15:20",
                        "completed": False
                    }
                ]
            }
        ]
    },
    {
        "id": "course-fastapi",
        "title": "Full-Stack Backend Development with FastAPI",
        "description": "Deep dive into synchronous and asynchronous web services using Python, FastAPI, and MongoDB Atlas. Learn modern RESTful designs, token auth, and route protections.",
        "shortDescription": "Build ultra-fast, production-ready Python backend APIs.",
        "category": "Backend",
        "difficulty": "Advanced",
        "thumbnail": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
        "teacherId": "user-teacher",
        "teacherName": "Dr. Sarah Jenkins",
        "status": "pending",
        "rating": 4.7,
        "reviewsCount": 42,
        "studentsCount": 380,
        "duration": "6 Hours",
        "rejectionReason": "",
        "modules": [
            {
                "id": "mod-api-1",
                "title": "Module 1: Scaffolding FastAPI & Async Core",
                "lessons": [
                    {
                        "id": "api-1-1",
                        "title": "1. Python Async/Await Foundations",
                        "type": "video",
                        "url": "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
                        "duration": "12:05",
                        "completed": False
                    },
                    {
                        "id": "api-1-2",
                        "title": "2. Setting up Uvicorn & MongoDB Atlas Cloud",
                        "type": "pdf",
                        "url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                        "duration": "Atlas Setup PDF",
                        "completed": False
                    }
                ]
            }
        ]
    },
    {
        "id": "course-design",
        "title": "UI/UX Foundations: Designing High-End Dashboards",
        "description": "Create breathtaking digital products. Learn how to master glassmorphism, tailwind variables, micro-animations, typography layouts, and HSL custom colors.",
        "shortDescription": "Design high-fidelity user experiences that wow clients.",
        "category": "Design",
        "difficulty": "Beginner",
        "thumbnail": "https://images.unsplash.com/photo-1541462608143-67571c6738dd?auto=format&fit=crop&w=600&q=80",
        "teacherId": "user-other-teacher",
        "teacherName": "Alex Mercer",
        "status": "approved",
        "rating": 4.9,
        "reviewsCount": 88,
        "studentsCount": 920,
        "duration": "3.5 Hours",
        "rejectionReason": "",
        "modules": [
            {
                "id": "mod-design-1",
                "title": "Module 1: Layout, Contrast & Colors",
                "lessons": [
                    {
                        "id": "design-1-1",
                        "title": "1. Selecting Dark Mode Palettes",
                        "type": "video",
                        "url": "https://res.cloudinary.com/demo/video/upload/elephants.mp4",
                        "duration": "15:40",
                        "completed": False
                    }
                ]
            }
        ]
    }
]

INITIAL_ENROLLMENTS = [
    {
        "id": "enroll-1",
        "studentId": "user-student",
        "courseId": "course-vue",
        "completedLessons": ["vue-1-1"],
        "progressPercent": 25,
        "enrolledDate": "2026-05-10"
    }
]

INITIAL_REVIEWS = [
    { "id": "rev-1", "courseId": "course-vue", "studentName": "Alex Mercer", "rating": 5, "comment": "Excellent structured explanation of refs and computed properties. Extremely easy to digest!", "date": "2026-05-15" },
    { "id": "rev-2", "courseId": "course-vue", "studentName": "Emma Watson", "rating": 4.5, "comment": "Very clean custom CSS layouts, highly legible.", "date": "2026-05-18" }
]

INITIAL_NOTIFS = [
    { "id": "not-1", "userId": "user-student", "title": "Welcome to Aether!", "message": "Explore dynamic programs in your Home catalog and start learning today.", "type": "info", "read": False, "date": "2026-05-26" },
    { "id": "not-2", "userId": "user-student", "title": "Resume Your Vue 3 Training", "message": "You have completed 25% of Mastering Vue 3! Continue modules.", "type": "success", "read": False, "date": "2026-05-26" }
]

def load_db() -> Dict[str, Any]:
    if not os.path.exists(DB_FILE):
        db = {
            "users": INITIAL_USERS,
            "courses": INITIAL_COURSES,
            "enrollments": INITIAL_ENROLLMENTS,
            "bookmarks": [],
            "reviews": INITIAL_REVIEWS,
            "notifications": INITIAL_NOTIFS
        }
        save_db(db)
        return db
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        # Fallback if corrupted
        db = {
            "users": INITIAL_USERS,
            "courses": INITIAL_COURSES,
            "enrollments": INITIAL_ENROLLMENTS,
            "bookmarks": [],
            "reviews": INITIAL_REVIEWS,
            "notifications": INITIAL_NOTIFS
        }
        save_db(db)
        return db

def save_db(data: Dict[str, Any]):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Helper function to add notification
def add_notification_helper(db: Dict[str, Any], user_id: str, title: str, message: str, type_str: str = "info"):
    new_notif = {
        "id": f"not-{int(time.time() * 1000)}",
        "userId": user_id,
        "title": title,
        "message": message,
        "type": type_str,
        "read": False,
        "date": datetime.today().strftime('%Y-%m-%d')
    }
    db["notifications"].insert(0, new_notif)

# --- REQUEST / RESPONSE SCHEMAS ---

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class CreateLessonSchema(BaseModel):
    title: str
    type: str  # video or pdf
    url: Optional[str] = None
    duration: Optional[str] = None

class CreateModuleSchema(BaseModel):
    title: str
    lessons: List[CreateLessonSchema]

class CreateCourseRequest(BaseModel):
    teacherId: str
    teacherName: str
    title: str
    description: str
    category: str
    difficulty: str
    thumbnail: Optional[str] = None
    modules: List[CreateModuleSchema]

class RejectCourseRequest(BaseModel):
    reason: str

class ReviewSubmitRequest(BaseModel):
    studentName: str
    rating: float
    comment: str

# --- ENDPOINTS ---

@app.get("/api/db")
def get_entire_db():
    """Returns the full database state so client store can hydrate itself seamlessly."""
    return load_db()

# AUTH & USERS
@app.post("/api/auth/login")
def login(req: LoginRequest):
    db = load_db()
    user = next((u for u in db["users"] if u["email"].lower() == req.email.lower()), None)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    if user["password"] != req.password:
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    if user.get("suspended", False):
        raise HTTPException(status_code=400, detail="Your account has been suspended by the administrator. Contact support.")
    return user

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    db = load_db()
    exists = any(u["email"].lower() == req.email.lower() for u in db["users"])
    if exists:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    new_user = {
        "id": f"user-{int(time.time() * 1000)}",
        "name": req.name,
        "email": req.email.lower(),
        "password": req.password,
        "role": req.role,
        "suspended": False,
        "joinedDate": datetime.today().strftime('%Y-%m-%d')
    }
    if req.role == "student":
        new_user["streakCount"] = 1
        
    db["users"].append(new_user)
    save_db(db)
    return new_user

@app.post("/api/users/{user_id}/suspend")
def toggle_suspension(user_id: str):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user["role"] == "admin":
        raise HTTPException(status_code=400, detail="Cannot suspend an Administrator account!")
    
    user["suspended"] = not user.get("suspended", False)
    save_db(db)
    return {"status": "success", "suspended": user["suspended"]}

@app.delete("/api/users/{user_id}")
def delete_user(user_id: str):
    db = load_db()
    user = next((u for u in db["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user["role"] == "admin":
        raise HTTPException(status_code=400, detail="Cannot delete an Administrator account!")
    
    db["users"] = [u for u in db["users"] if u["id"] != user_id]
    save_db(db)
    return {"status": "success", "message": "User deleted."}


# COURSES & MODULES
@app.post("/api/courses")
def create_course(req: CreateCourseRequest):
    db = load_db()
    new_course = {
        "id": f"course-{int(time.time() * 1000)}",
        "title": req.title,
        "description": req.description,
        "shortDescription": req.description[:80] + "..." if len(req.description) > 80 else req.description,
        "category": req.category,
        "difficulty": req.difficulty,
        "thumbnail": req.thumbnail or "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=600&q=80",
        "teacherId": req.teacherId,
        "teacherName": req.teacherName,
        "status": "pending",
        "rating": 5.0,
        "reviewsCount": 0,
        "studentsCount": 0,
        "duration": "Flexible",
        "rejectionReason": "",
        "modules": []
    }
    
    for mod_idx, mod in enumerate(req.modules):
        lessons_list = []
        for les_idx, les in enumerate(mod.lessons):
            lessons_list.append({
                "id": f"les-{int(time.time() * 1000)}-{mod_idx}-{les_idx}",
                "title": les.title,
                "type": les.type,
                "url": les.url or ("https://res.cloudinary.com/demo/video/upload/elephants.mp4" if les.type == "video" else "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"),
                "duration": les.duration or ("12:00" if les.type == "video" else "Reading Guide (5 mins)"),
                "completed": False
            })
        new_course["modules"].append({
            "id": f"mod-{int(time.time() * 1000)}-{mod_idx}",
            "title": mod.title,
            "lessons": lessons_list
        })
        
    db["courses"].append(new_course)
    
    # Notify Admin
    admin_users = [u for u in db["users"] if u["role"] == "admin"]
    for admin in admin_users:
        add_notification_helper(db, admin["id"], "Moderate New Course Proposal", f'"{req.title}" has been submitted by {req.teacherName} and is awaiting review.', "warning")
        
    save_db(db)
    return new_course

@app.post("/api/courses/{course_id}/approve")
def approve_course(course_id: str):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    
    course["status"] = "approved"
    course["rejectionReason"] = ""
    
    # Notify Teacher
    add_notification_helper(db, course["teacherId"], "Course Proposal Approved! 🎉", f'Your program "{course["title"]}" has been approved by the Admin and is now live!', "success")
    
    save_db(db)
    return course

@app.post("/api/courses/{course_id}/reject")
def reject_course(course_id: str, req: RejectCourseRequest):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    
    course["status"] = "rejected"
    course["rejectionReason"] = req.reason or "Does not meet course formatting standards."
    
    # Notify Teacher
    add_notification_helper(db, course["teacherId"], "Course Proposal Returned", f'Your program "{course["title"]}" requires revisions: "{req.reason}"', "danger")
    
    save_db(db)
    return course


# ENROLLMENTS & LESSON TRACKING
@app.post("/api/courses/{course_id}/enroll")
def enroll_in_course(course_id: str, studentId: str):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
        
    exists = any(e["studentId"] == studentId and e["courseId"] == course_id for e in db["enrollments"])
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
    
    # Increment student count of the course
    course["studentsCount"] = course.get("studentsCount", 0) + 1
    
    db["enrollments"].append(new_enroll)
    
    # Notify student
    add_notification_helper(db, studentId, "Enrolled Successfully!", f'You have enrolled in "{course["title"]}". Start learning today!', "success")
    
    save_db(db)
    return new_enroll

@app.post("/api/courses/{course_id}/lesson-toggle")
def toggle_lesson(course_id: str, studentId: str, lessonId: str):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    enrollment = next((e for e in db["enrollments"] if e["studentId"] == studentId and e["courseId"] == course_id), None)
    
    if not course or not enrollment:
        raise HTTPException(status_code=404, detail="Course or enrollment not found.")
        
    # Count total lessons
    total_lessons = sum(len(module["lessons"]) for module in course["modules"])
    if total_lessons == 0:
        raise HTTPException(status_code=400, detail="Course has no lessons.")
        
    completed = enrollment.get("completedLessons", [])
    if lessonId in completed:
        completed.remove(lessonId)
    else:
        completed.append(lessonId)
        
    enrollment["completedLessons"] = completed
    progress = int(round((len(completed) / total_lessons) * 100))
    enrollment["progressPercent"] = progress
    
    if progress == 100:
        enrollment["completedDate"] = datetime.today().strftime('%Y-%m-%d')
        add_notification_helper(db, studentId, "Course Completed! 🎓", f'Congratulations! You have completed 100% of "{course["title"]}". Claim your verified certificate now!', "success")
    else:
        enrollment.pop("completedDate", None)
        
    save_db(db)
    return enrollment

@app.post("/api/courses/{course_id}/auto-complete")
def auto_complete_course(course_id: str, studentId: str):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    enrollment = next((e for e in db["enrollments"] if e["studentId"] == studentId and e["courseId"] == course_id), None)
    
    if not course or not enrollment:
        raise HTTPException(status_code=404, detail="Course or enrollment not found.")
        
    all_lessons = []
    for mod in course["modules"]:
        for les in mod["lessons"]:
            all_lessons.append(les["id"])
            
    enrollment["completedLessons"] = all_lessons
    enrollment["progressPercent"] = 100
    enrollment["completedDate"] = datetime.today().strftime('%Y-%m-%d')
    
    add_notification_helper(db, studentId, "Program Completed! 🎓", f'You completed 100% of "{course["title"]}". Verified certificate unlocked!', "success")
    
    save_db(db)
    return enrollment


# BOOKMARKS
@app.post("/api/courses/{course_id}/bookmark")
def toggle_bookmark(course_id: str, studentId: str):
    db = load_db()
    bookmarks = db.get("bookmarks", [])
    
    existing = next((b for b in bookmarks if b["studentId"] == studentId and b["courseId"] == course_id), None)
    if existing:
        bookmarks.remove(existing)
        status_action = "removed"
    else:
        bookmarks.append({"studentId": studentId, "courseId": course_id})
        status_action = "added"
        
    db["bookmarks"] = bookmarks
    save_db(db)
    return {"status": "success", "action": status_action}


# REVIEWS
@app.post("/api/courses/{course_id}/reviews")
def submit_review(course_id: str, req: ReviewSubmitRequest):
    db = load_db()
    course = next((c for c in db["courses"] if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
        
    new_rev = {
        "id": f"rev-{int(time.time() * 1000)}",
        "courseId": course_id,
        "studentName": req.studentName,
        "rating": float(req.rating),
        "comment": req.comment,
        "date": datetime.today().strftime('%Y-%m-%d')
    }
    
    db["reviews"].insert(0, new_rev)
    
    # Recalculate average course rating
    course_reviews = [r for r in db["reviews"] if r["courseId"] == course_id]
    total_rating = sum(r["rating"] for r in course_reviews)
    course["rating"] = round(total_rating / len(course_reviews), 1)
    course["reviewsCount"] = len(course_reviews)
    
    # Notify Teacher
    add_notification_helper(db, course["teacherId"], "New Student Review", f'A student posted a {req.rating}★ review on your course "{course["title"]}".', "info")
    
    save_db(db)
    return new_rev


# NOTIFICATIONS
@app.post("/api/notifications/read")
def read_notifications(userId: str):
    db = load_db()
    for n in db["notifications"]:
        if n["userId"] == userId:
            n["read"] = True
    save_db(db)
    return {"status": "success"}


class NotificationRequest(BaseModel):
    userId: str
    title: str
    message: str
    type: str = "info"

@app.post("/api/notifications")
def add_notification(req: NotificationRequest):
    db = load_db()
    add_notification_helper(db, req.userId, req.title, req.message, req.type)
    save_db(db)
    return {"status": "success"}


# SYSTEM CONTROLS
@app.post("/api/system/reset")
def reset_database():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    load_db()
    return {"status": "success", "message": "Database reset to mock state."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from pydantic import BaseModel
from typing import List, Optional

class CreateLessonSchema(BaseModel):
    id: Optional[str] = None
    title: str
    type: str
    url: Optional[str] = None
    duration: Optional[str] = None

class CreateModuleSchema(BaseModel):
    id: Optional[str] = None
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
    price: Optional[int] = 0
    modules: List[CreateModuleSchema]
    learningOutcomes: Optional[List[str]] = None

class RejectCourseRequest(BaseModel):
    reason: str

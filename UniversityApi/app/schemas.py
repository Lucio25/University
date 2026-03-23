from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    phone: Optional[str] = None
    registration_number: Optional[str] = None 

class StudentCreate(StudentBase):
    pass  # POST

class StudentRead(StudentBase):
    id: int
    class Config:
        from_attributes = True

class CourseRead(BaseModel):
    name: str
    capacity: int
    study_year: str
    study_plan_id: int

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    career_id: int
    study_plan_id: int
    year: str

class EnrollmentResponse(BaseModel):
    line_id: int
    materia: str
    materia_id: int
    inscripcion_id: int

    class Config:
        from_attributes = True
from fastapi import APIRouter, HTTPException, status
from typing import List
from .schemas import (
    StudentCreate, StudentRead,
    CourseRead,
    EnrollmentCreate, EnrollmentResponse
)
from .services import UniversityService

router = APIRouter()


@router.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(payload: StudentCreate):
    try:
        student_data = UniversityService.create_student(payload.model_dump())
        return student_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/courses", status_code=status.HTTP_201_CREATED)
async def create_course(payload: CourseRead):
    try:
        course_data = UniversityService.create_course(payload.model_dump())
        return course_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/enrollments")
async def enroll_student(payload: EnrollmentCreate):
    try:
        result = UniversityService.enroll_student(payload.model_dump())
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/students/{id}/enrollments", response_model=List[EnrollmentResponse])
async def get_student_enrollments(id: int):
    try:
        enrollments = UniversityService.get_enrollments_by_student(id)
        return enrollments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
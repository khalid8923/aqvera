from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db_session, get_current_user
from app.models.course import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseRead
from app.services import course as course_service

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return course_service.create_course(db, course_in, current_user.id)


@router.get("", response_model=List[CourseRead])
def list_courses(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    include_archived: bool = Query(False),
):
    return course_service.get_courses(
        db, current_user.id, skip=skip, limit=limit, include_archived=include_archived
    )


@router.get("/{course_id}", response_model=CourseRead)
def get_course(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    db_course = course_service.get_course(db, course_id, current_user.id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.put("/{course_id}", response_model=CourseRead)
def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    db_course = course_service.update_course(db, course_id, course_in, current_user.id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.patch("/{course_id}/archive", response_model=CourseRead)
def archive_course(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    db_course = course_service.archive_course(db, course_id, current_user.id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    success = course_service.delete_course(db, course_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return None

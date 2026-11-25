from typing import Optional
from sqlalchemy.orm import Session
from app.models.course import User, Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int, owner_id: int) -> Optional[Course]:
    return (
        db.query(Course)
        .filter(Course.id == course_id, Course.owner_id == owner_id)
        .first()
    )


def get_courses(
    db: Session, owner_id: int, skip: int = 0, limit: int = 100, include_archived: bool = False
) -> list[Course]:
    query = db.query(Course).filter(Course.owner_id == owner_id)
    if not include_archived:
        query = query.filter(Course.is_archived == False)  # noqa: E712
    return query.offset(skip).limit(limit).all()


def create_course(db: Session, course_in: CourseCreate, owner_id: int) -> Course:
    db_course = Course(**course_in.model_dump(), owner_id=owner_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course_in: CourseUpdate, owner_id: int) -> Optional[Course]:
    db_course = get_course(db, course_id, owner_id)
    if not db_course:
        return None
    update_data = course_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def archive_course(db: Session, course_id: int, owner_id: int) -> Optional[Course]:
    db_course = get_course(db, course_id, owner_id)
    if not db_course:
        return None
    db_course.is_archived = True
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int, owner_id: int) -> bool:
    db_course = get_course(db, course_id, owner_id)
    if not db_course:
        return False
    db.delete(db_course)
    db.commit()
    return True

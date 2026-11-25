from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    university: Optional[str] = None
    department: Optional[str] = None
    course_code: Optional[str] = None
    semester: Optional[str] = None
    description: Optional[str] = None
    primary_language: Optional[str] = "en"
    subject_domain: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    university: Optional[str] = None
    department: Optional[str] = None
    course_code: Optional[str] = None
    semester: Optional[str] = None
    description: Optional[str] = None
    primary_language: Optional[str] = None
    subject_domain: Optional[str] = None
    is_archived: Optional[bool] = None


class CourseRead(CourseBase):
    id: int
    owner_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ErrorResponse(BaseModel):
    detail: str

"""Extended authentication schemas: register, login, logout, password, profile, preferences."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ErrorResponse(BaseModel):
    detail: str


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class UserProfile(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None
    is_active: bool
    email_verified: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    language: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class EmailVerifyRequest(BaseModel):
    token: str


class SessionInfo(BaseModel):
    id: int
    user_agent: Optional[str] = None
    ip_address: Optional[str] = None
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PreferenceRead(BaseModel):
    language: str
    theme: str
    email_notifications: bool
    study_reminders: bool

    class Config:
        from_attributes = True


class PreferenceUpdate(BaseModel):
    language: Optional[str] = None
    theme: Optional[str] = None
    email_notifications: Optional[bool] = None
    study_reminders: Optional[bool] = None


class OnboardingStatus(BaseModel):
    welcome_seen: bool
    language_selected: bool
    interests_selected: bool
    first_course_created: bool
    first_material_uploaded: bool
    tutor_introduced: bool
    completed: bool

    class Config:
        from_attributes = True


class OnboardingStep(BaseModel):
    step: str
    completed: bool

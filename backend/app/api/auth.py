"""Authentication API routes: register, login, logout, password, profile, sessions."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db_session, get_current_user
from app.services import auth as auth_service
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    UserRead,
    Token,
    TokenResponse,
    RefreshRequest,
    LogoutRequest,
    PasswordChange,
    PasswordResetRequest,
    PasswordResetConfirm,
    EmailVerifyRequest,
    ProfileUpdate,
    UserProfile,
    PreferenceRead,
    PreferenceUpdate,
    SessionInfo,
    OnboardingStatus,
)
from app.models.course import User
from app.core.security import create_refresh_token, create_access_token
from app.core.config import settings
from app.services.email import email_service
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

ALGORITHM = "HS256"


def _issue_tokens(user: User) -> TokenResponse:
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db_session)):
    try:
        user = auth_service.create_user(db, user_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user


@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db_session)):
    user = auth_service.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return _issue_tokens(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    logout_in: LogoutRequest,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    # Revoke the session identified by the refresh token.
    sessions = auth_service.list_sessions(db, current_user.id)
    for s in sessions:
        from app.core.security import verify_password

        if verify_password(logout_in.refresh_token, s.refresh_token_hash):
            auth_service.revoke_session(db, s.id, current_user.id)
            break
    return None


@router.post("/refresh", response_model=TokenResponse)
def refresh(
    refresh_in: RefreshRequest,
    db: Session = Depends(get_db_session),
):
    session = auth_service.get_session_by_refresh_hash(db, refresh_in.refresh_token)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    user = auth_service.get_user_by_id(db, session.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    # Rotate: revoke old session, create new one.
    auth_service.revoke_session(db, session.id, session.user_id)
    auth_service.create_session(
        db,
        session.user_id,
        refresh_in.refresh_token,
        user_agent=None,
        ip_address=None,
    )
    return _issue_tokens(user)


@router.post("/password/change", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    change: PasswordChange,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    if not auth_service.change_password(db, current_user.id, change):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    # Revoke all sessions on password change.
    auth_service.revoke_all_sessions(db, current_user.id)
    return None


@router.post("/password/reset/request", status_code=status.HTTP_204_NO_CONTENT)
def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db_session),
):
    user = auth_service.get_user_by_email(db, request.email)
    if not user:
        # Do not reveal whether the email exists.
        return None
    token = auth_service.create_password_reset_token(db, user)
    # Email delivery: in production, send token via configured SMTP.
    # If SMTP is not configured, the token is not returned to the client
    # (to avoid leaking it). Local testing can inspect the server logs.
    return None


@router.post("/password/reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_password_reset(
    confirm: PasswordResetConfirm,
    db: Session = Depends(get_db_session),
):
    if not auth_service.consume_password_reset_token(
        db, confirm.token, confirm.new_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    return None


@router.post("/email/verify", status_code=status.HTTP_204_NO_CONTENT)
def verify_email(
    request: EmailVerifyRequest,
    db: Session = Depends(get_db_session),
):
    if not auth_service.verify_email_token(db, request.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )
    return None


@router.get("/profile", response_model=UserProfile)
def get_profile(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        email_verified=current_user.email_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.patch("/profile", response_model=UserProfile)
def update_profile(
    update: ProfileUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    user = auth_service.update_profile(db, current_user.id, update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Update language preference if provided
    if update.language is not None:
        prefs = auth_service.get_or_create_preferences(db, current_user.id)
        prefs.language = update.language
        db.add(prefs)
        db.commit()
    return UserProfile(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        email_verified=user.email_verified,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get("/sessions", response_model=list[SessionInfo])
def list_sessions(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    sessions = auth_service.list_sessions(db, current_user.id)
    return sessions


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_session(
    session_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    if not auth_service.revoke_session(db, session_id, current_user.id):
        raise HTTPException(status_code=404, detail="Session not found")
    return None


@router.delete("/sessions", status_code=status.HTTP_204_NO_CONTENT)
def revoke_all_sessions(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    auth_service.revoke_all_sessions(db, current_user.id)
    return None


@router.get("/preferences", response_model=PreferenceRead)
def get_preferences(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    prefs = auth_service.get_or_create_preferences(db, current_user.id)
    return prefs


@router.patch("/preferences", response_model=PreferenceRead)
def update_preferences(
    update: PreferenceUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    prefs = auth_service.update_preferences(db, current_user.id, update)
    if not prefs:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return prefs


@router.get("/onboarding", response_model=OnboardingStatus)
def get_onboarding(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    record = auth_service.get_onboarding_status(db, current_user.id)
    if not record:
        return OnboardingStatus(
            welcome_seen=False,
            language_selected=False,
            interests_selected=False,
            first_course_created=False,
            first_material_uploaded=False,
            tutor_introduced=False,
            completed=False,
        )
    return OnboardingStatus(
        welcome_seen=record.welcome_seen,
        language_selected=record.language_selected,
        interests_selected=record.interests_selected,
        first_course_created=record.first_course_created,
        first_material_uploaded=record.first_material_uploaded,
        tutor_introduced=record.tutor_introduced,
        completed=record.completed_at is not None,
    )


@router.post("/onboarding/{step}", status_code=status.HTTP_204_NO_CONTENT)
def complete_onboarding_step(
    step: str,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    valid_steps = {
        "welcome_seen",
        "language_selected",
        "interests_selected",
        "first_course_created",
        "first_material_uploaded",
        "tutor_introduced",
    }
    if step not in valid_steps:
        raise HTTPException(status_code=400, detail="Invalid onboarding step")
    auth_service.update_onboarding_step(db, current_user.id, step, True)
    return None


@router.get("/email/config", response_model=dict)
def email_config_status():
    """Return the email service configuration state.

    Never exposes SMTP credentials. Clients use this to determine whether
    password-reset and verification emails can actually be delivered.
    """
    return email_service.config_state()

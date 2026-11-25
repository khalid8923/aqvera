"""Authentication service: register, login, password hashing, sessions, profile, preferences, onboarding."""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session

from app.models.course import User
from app.models.auth import (
    UserSession,
    PasswordReset,
    EmailVerification,
    UserPreference,
    OnboardingRecord,
)
from app.schemas.auth import UserRegister, UserLogin, ProfileUpdate, PasswordChange
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user_in: UserRegister) -> User:
    """Create a new user with hashed password."""
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")
    db_user = User(
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create default preferences
    prefs = UserPreference(user_id=db_user.id)
    db.add(prefs)

    # Create onboarding record
    onboarding = OnboardingRecord(user_id=db_user.id)
    db.add(onboarding)

    db.commit()
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Verify credentials; return user or None."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def change_password(db: Session, user_id: int, change: PasswordChange) -> bool:
    """Change a user's password after verifying the current password."""
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    if not verify_password(change.current_password, user.password_hash):
        return False
    user.password_hash = get_password_hash(change.new_password)
    db.add(user)
    db.commit()
    return True


def create_password_reset_token(db: Session, user: User) -> str:
    """Create a password reset token for a user."""
    token = secrets.token_urlsafe(32)
    token_hash = get_password_hash(token)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    db.add(
        PasswordReset(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
    )
    db.commit()
    return token


def verify_password_reset_token(
    db: Session, token: str
) -> Optional[User]:
    """Validate a password reset token; return the user if valid and unused."""
    token_hash = get_password_hash(token)
    reset = (
        db.query(PasswordReset)
        .filter(PasswordReset.token_hash == token_hash, PasswordReset.used_at.is_(None))
        .first()
    )
    if not reset:
        return None
    if reset.expires_at < datetime.now(timezone.utc):
        return None
    return get_user_by_id(db, reset.user_id)


def consume_password_reset_token(
    db: Session, token: str, new_password: str
) -> bool:
    """Consume a password reset token and set the new password."""
    token_hash = get_password_hash(token)
    reset = (
        db.query(PasswordReset)
        .filter(PasswordReset.token_hash == token_hash, PasswordReset.used_at.is_(None))
        .first()
    )
    if not reset:
        return False
    if reset.expires_at < datetime.now(timezone.utc):
        return False
    user = get_user_by_id(db, reset.user_id)
    if not user:
        return False
    user.password_hash = get_password_hash(new_password)
    reset.used_at = datetime.now(timezone.utc)
    db.add(user)
    db.add(reset)
    db.commit()
    return True


def create_email_verification_token(db: Session, user: User) -> str:
    """Create an email verification token for a user."""
    token = secrets.token_urlsafe(32)
    token_hash = get_password_hash(token)
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    db.add(
        EmailVerification(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
    )
    db.commit()
    return token


def verify_email_token(db: Session, token: str) -> bool:
    """Verify an email verification token."""
    token_hash = get_password_hash(token)
    verification = (
        db.query(EmailVerification)
        .filter(
            EmailVerification.token_hash == token_hash,
            EmailVerification.verified_at.is_(None),
        )
        .first()
    )
    if not verification:
        return False
    if verification.expires_at < datetime.now(timezone.utc):
        return False
    user = get_user_by_id(db, verification.user_id)
    if not user:
        return False
    verification.verified_at = datetime.now(timezone.utc)
    user.email_verified = True
    db.add(verification)
    db.add(user)
    db.commit()
    return True


def create_session(
    db: Session,
    user_id: int,
    refresh_token: str,
    user_agent: Optional[str] = None,
    ip_address: Optional[str] = None,
    ttl_minutes: int = 30,
) -> UserSession:
    """Create a user session with a hashed refresh token."""
    token_hash = get_password_hash(refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=ttl_minutes)
    session = UserSession(
        user_id=user_id,
        refresh_token_hash=token_hash,
        user_agent=user_agent,
        ip_address=ip_address,
        expires_at=expires_at,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session_by_refresh_hash(
    db: Session, refresh_token: str
) -> Optional[UserSession]:
    """Look up a session by its refresh token hash."""
    token_hash = get_password_hash(refresh_token)
    return (
        db.query(UserSession)
        .filter(
            UserSession.refresh_token_hash == token_hash,
            UserSession.revoked_at.is_(None),
            UserSession.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )


def revoke_session(db: Session, session_id: int, user_id: int) -> bool:
    """Revoke a user's session by ID."""
    session = (
        db.query(UserSession)
        .filter(UserSession.id == session_id, UserSession.user_id == user_id)
        .first()
    )
    if not session:
        return False
    session.revoked_at = datetime.now(timezone.utc)
    db.add(session)
    db.commit()
    return True


def revoke_all_sessions(db: Session, user_id: int) -> int:
    """Revoke all sessions for a user. Returns count revoked."""
    sessions = (
        db.query(UserSession)
        .filter(UserSession.user_id == user_id, UserSession.revoked_at.is_(None))
        .all()
    )
    now = datetime.now(timezone.utc)
    for s in sessions:
        s.revoked_at = now
    db.commit()
    return len(sessions)


def list_sessions(db: Session, user_id: int) -> list[UserSession]:
    """List all sessions for a user (active and revoked)."""
    return (
        db.query(UserSession)
        .filter(UserSession.user_id == user_id)
        .order_by(UserSession.created_at.desc())
        .all()
    )


def update_profile(
    db: Session, user_id: int, update: ProfileUpdate
) -> Optional[User]:
    """Update a user's profile fields."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    if update.full_name is not None:
        user.full_name = update.full_name
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_preferences(db: Session, user_id: int) -> UserPreference:
    """Get or create user preferences."""
    prefs = (
        db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
    )
    if not prefs:
        prefs = UserPreference(user_id=user_id)
        db.add(prefs)
        db.commit()
        db.refresh(prefs)
    return prefs


def update_preferences(
    db: Session, user_id: int, update
) -> Optional[UserPreference]:
    """Update user preferences."""
    prefs = get_or_create_preferences(db, user_id)
    data = update.model_dump(exclude_unset=True) if hasattr(update, "model_dump") else update
    for field, value in data.items():
        if value is not None:
            setattr(prefs, field, value)
    prefs.updated_at = datetime.now(timezone.utc)
    db.add(prefs)
    db.commit()
    db.refresh(prefs)
    return prefs


def get_onboarding_status(db: Session, user_id: int) -> Optional[OnboardingRecord]:
    """Get the onboarding record for a user."""
    return (
        db.query(OnboardingRecord).filter(OnboardingRecord.user_id == user_id).first()
    )


def update_onboarding_step(
    db: Session, user_id: int, step: str, completed: bool = True
) -> OnboardingRecord:
    """Mark an onboarding step as completed."""
    record = get_onboarding_status(db, user_id)
    if not record:
        record = OnboardingRecord(user_id=user_id)
        db.add(record)
        db.commit()
        db.refresh(record)
    setattr(record, step, completed)
    # Check if all steps are done
    all_done = all(
        [
            record.welcome_seen,
            record.language_selected,
            record.interests_selected,
            record.first_course_created,
            record.first_material_uploaded,
            record.tutor_introduced,
        ]
    )
    if all_done and not record.completed_at:
        record.completed_at = datetime.now(timezone.utc)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def ensure_course_ownership(db: Session, course_id: int, owner_id: int) -> bool:
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.owner_id == owner_id)
        .first()
    )
    return course is not None


# Import Course here to avoid circular import issues at module load
from app.models.course import Course  # noqa: E402

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str = "AQVERA"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./aqvera.db"
    SECRET_KEY: str = "dev-secret-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # --- Email / SMTP Configuration ---
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASS: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    SMTP_USE_TLS: bool = True

    @property
    def email_configured(self) -> bool:
        """Return True if SMTP is fully configured."""
        return all(
            [
                self.SMTP_HOST,
                self.SMTP_PORT,
                self.SMTP_USER,
                self.SMTP_PASS,
                self.SMTP_FROM,
            ]
        )

    class Config:
        env_file = ".env"


settings = Settings()

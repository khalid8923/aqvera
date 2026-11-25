import sys
import os

# Make the project-root `ai/` package importable from the backend.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import courses
from app.api import chat
from app.api import auth
from app.api import materials
from app.api import tutor
from app.api import study
from app.db.session import engine
import app.models  # noqa: F401  register all models with Base metadata
from app.models import base as models_base

models_base.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(chat.router)
app.include_router(auth.router)
app.include_router(materials.router)
app.include_router(tutor.router)
app.include_router(study.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.APP_ENV}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

from app.core.config import settings
from app.core.db import SessionLocal
from app.models.models import Character
from app.routers import auth, voice
from app.scripts.seed_characters import seed as seed_characters
from app.verticals.kids.router import router as kids_router
from app.verticals.english.router import router as english_router
from app.verticals.interview.router import router as interview_router

app = FastAPI(title="Multi-Vertical AI Platform")

# CORS: only the deployed web frontend(s) may call this API from a browser.
# CORS_ALLOWED_ORIGINS is a comma-separated list; falls back to localhost for local dev.
_allowed_origins = [
    o.strip() for o in getattr(settings, "cors_allowed_origins", "http://localhost:3000").split(",") if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(voice.router)
app.include_router(kids_router, prefix="/api/kids")
app.include_router(english_router, prefix="/api/english")
app.include_router(interview_router, prefix="/api/interview")


@app.on_event("startup")
async def auto_seed_characters():
    """Idempotent: only seeds if the characters table is empty. Safe to run on every boot."""
    async with SessionLocal() as db:
        count = await db.scalar(select(func.count()).select_from(Character))
        if count == 0:
            await seed_characters()


@app.get("/health")
async def health():
    return {"status": "ok"}

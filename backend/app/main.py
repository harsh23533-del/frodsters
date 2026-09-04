from fastapi import FastAPI

from app.routers import auth, voice
from app.verticals.kids.router import router as kids_router
from app.verticals.english.router import router as english_router
from app.verticals.interview.router import router as interview_router

app = FastAPI(title="Multi-Vertical AI Platform")

app.include_router(auth.router)
app.include_router(voice.router)
app.include_router(kids_router, prefix="/api/kids")
app.include_router(english_router, prefix="/api/english")
app.include_router(interview_router, prefix="/api/interview")


@app.get("/health")
async def health():
    return {"status": "ok"}

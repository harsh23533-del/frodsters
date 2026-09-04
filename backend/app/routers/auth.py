from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Header
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.models.models import User

router = APIRouter(tags=["auth"])

ALGORITHM = "HS256"


def hash_password(pw: str) -> str:
    return bcrypt.hash(pw)


def verify_password(pw: str, pw_hash: str) -> bool:
    return bcrypt.verify(pw, pw_hash)


def create_token(user_id: str) -> str:
    payload = {"sub": user_id, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")


@router.post("/api/auth/signup")
async def signup(email: str, password: str, name: str, vertical: str, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Email already registered")

    user = User(email=email, name=name, vertical=vertical, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"token": create_token(str(user.id))}


@router.post("/api/auth/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    return {"token": create_token(str(user.id))}

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.models import AuthSession, PrivacySettings, Profile, User
from app.api.deps import get_current_user
from app.schemas.auth import RefreshRequest, TokenPair, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=TokenPair)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter((User.email == payload.email) | (User.username == payload.username)).first():
        raise HTTPException(status_code=400, detail="Email or username already exists")

    user = User(username=payload.username, email=payload.email, hashed_password=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.add(Profile(user_id=user.id, display_name=user.username))
    db.add(PrivacySettings(user_id=user.id))
    db.commit()
    return _issue_token_pair(db, user.id)


@router.post("/login", response_model=TokenPair)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return _issue_token_pair(db, user.id)


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(payload.refresh_token, settings.jwt_secret_key, algorithms=[settings.algorithm])
        if decoded.get("type") != "refresh":
            raise ValueError("wrong token")
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(decoded["sub"])
    return _issue_token_pair(db, user_id)


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


def _issue_token_pair(db: Session, user_id: int) -> TokenPair:
    access = create_access_token(str(user_id))
    refresh = create_refresh_token(str(user_id))
    db.add(
        AuthSession(
            user_id=user_id,
            refresh_token_hash=refresh[-30:],
            expires_at=datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes),
        )
    )
    db.commit()
    return TokenPair(access_token=access, refresh_token=refresh)

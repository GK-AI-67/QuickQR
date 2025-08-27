from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.lost_and_found_qr.models.user_dtls_db import UserDtlsDB
from app.models.user_models import User
from datetime import datetime
import uuid
from typing import Optional
import requests


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GoogleLoginRequest(BaseModel):
    id_token: str


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(UserDtlsDB).filter(UserDtlsDB.gmail == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Treat None as active (for backward compatibility)
    if user.active_status is False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


@router.post("/register", response_model=TokenResponse)
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=body.email, hashed_password=hash_password(body.password), provider="local")
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.email)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(user.email)
    return TokenResponse(access_token=token)


@router.post("/google", response_model=TokenResponse)
def google_login(body: GoogleLoginRequest, db: Session = Depends(get_db)):
    # Verify with Google tokeninfo endpoint (server-side validation)
    r = requests.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": body.id_token}, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google token")
    payload = r.json()
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not present in Google token")
    
    # Extract additional user information from Google token
    first_name = payload.get("given_name", "")
    last_name = payload.get("family_name", "")
    # Note: Google token doesn't include phone number, so we'll leave it as None
    
    user = db.query(UserDtlsDB).filter(UserDtlsDB.gmail == email).first()
    if not user:
        user = UserDtlsDB(
            userid=str(uuid.uuid4()),
            gmail=email,
            first_name=first_name,
            last_name=last_name,
            password="",  # Empty for Google users
            provider="google",
            active_status=True,
            created_date=datetime.now()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # Update existing user's name if it was empty or different
        if not user.first_name and first_name:
            user.first_name = first_name
        if not user.last_name and last_name:
            user.last_name = last_name
        # Ensure existing user is active
        if not user.active_status:
            user.active_status = True
        db.commit()
        db.refresh(user)
    token = create_access_token(email)
    return TokenResponse(access_token=token)

@router.get("/debug/user")
def debug_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Debug endpoint to check user status"""
    try:
        email = decode_token(token)
        if not email:
            return {"error": "Invalid token"}
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"error": "User not found"}
        return {
            "email": user.email,
            "is_active": user.is_active,
            "provider": user.provider,
            "created_at": user.created_at
        }
    except Exception as e:
        return {"error": str(e)}



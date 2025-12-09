from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from auth import token_expires
from database import get_db
from model import UserT
from schema.user import UserResponse, UserCreate, UserAUthCreate, UserAuthLogin
from Service.auth_service import auth
import uuid
from schema.auth_schema import Token

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(UserAuthLogin(email=form_data.username, hashed_password =form_data.password), db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=token_expires)
    access_token = auth.create_access_token(user.email, user.id, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/user", response_model=UserResponse)
def logged_in_user(user: UserT = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    return user
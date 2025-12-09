from passlib.context import CryptContext
from datetime import timedelta, datetime
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from model import UserT
from schema.user import UserResponse, UserCreate, UserLogin, UserAUthCreate
import uuid
from auth import secret_key, algorithm, jwt, JWTError, oauth2_scheme
from auth import get_pwd_hash, authenticate_user, token_expires, pwd_context

class AuthService:
    @staticmethod
    def register_user(user: UserAUthCreate, db: Session):
        details = db.query(UserT).filter(UserT.email == user.email).first()
        if details:
            return UserResponse(message="Email already exists")
        hash_password = get_pwd_hash(user.hashed_password)
        new_user = UserT(id = str(uuid.uuid4()), email = user.email, hashed_password = hash_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def login_user(user: UserLogin, db: Session):
        details = auth.authenticate_user(user, db)
        if not details:
            return {"error": "Invalid credentials"}
        access_token = auth.create_access_token(details.email, details.id, expires_delta=token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    
    @staticmethod
    def authenticate_user(user: UserCreate, db: Session = Depends(get_db)):
        details = db.query(UserT).filter(UserT.email == user.email).first()
        if not details:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        if not pwd_context.verify(user.hashed_password, details.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return details

    @staticmethod
    def create_access_token(email: EmailStr, user_id: str, expires_delta:timedelta):
        encode = {"email": email, "id": user_id}
        expire = datetime.utcnow() + expires_delta
        encode.update({"exp": expire})
        encoded_jwt = jwt.encode(encode, secret_key, algorithm=algorithm)
        return encoded_jwt

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            print(payload)
            email: str = payload.get("email")
            user_id: str = payload.get("id")
            print(email, user_id)
            if email is None or user_id is None:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials1")
            user = db.query(UserT).filter(UserT.id == user_id).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User no longer exists"
                )
            return user
        except JWTError:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials2")

auth = AuthService()

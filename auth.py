from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timedelta
from database import get_db
from model import UserT
from typing import Optional
from schema.auth_schema import TokenData
# from Service.user import user_service
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
token_expires = int(os.getenv("TOKEN_EXPIRES", 30))
algorithm = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hash_password: str) -> bool:
    pwd = pwd_context.verify(plain_password, hash_password)
    return pwd

def get_pwd_hash(password: str) -> str:
    pwd = pwd_context.hash(password)
    return pwd

def create_access_token(data: dict, expires_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=token_expires)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
    

def verify_token(token: str) -> TokenData:
    """Verify JWT token and return token data"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject"
            )
        return TokenData(email=email)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserT).filter(UserT.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(UserT).filter(UserT.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
    
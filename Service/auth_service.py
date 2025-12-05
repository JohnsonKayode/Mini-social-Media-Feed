from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException
import datetime
from sqlalchemy.orm import Session
from database import get_db
from model import UserT
from schema.user import UserResponse, UserCreate, UserAUthCreate, UserAuthLogin
import uuid
from auth import get_pwd_hash, authenticate_user, create_access_token, token_expires, pwd_context

class AuthService:
    @staticmethod
    def register_user(user: UserAUthCreate, db: Session) -> UserResponse:
        details = db.query(UserT).filter(UserT.email == user.email).first()
        if details:
            return UserResponse(message="User already exists")
        hash_password = get_pwd_hash(user.hashed_password)
        new_user = UserT(id = str(uuid.uuid4()), **user.model_dump(), hashed_password=hash_password)
        db.add(new_user)
        db.flush()
        db.refresh(new_user)
        return new_user
    
    @staticmethod
    def login_user(user: UserAuthLogin, db: Session):
        details = authenticate_user(db, user.email, user.hashed_password)
        if not details:
            return {"error": "Invalid credentials"}
        access_token = create_access_token(data={"sub": details.email}, expires_delta=token_expires)
        return access_token
    

    def authenticate_user(user: UserCreate, db: Session = Depends(get_db)):
        details = db.query(UserT).filter(UserT.email == user.email).first()
        if not details:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        if not pwd_context.verify(user.password, details.password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return details


    def create_access_token(email: EmailStr, user_id: str, expires_delta:timedelta):
        encode = {"email": email, "id": user_id}
        expire = datetime.utcnow() + expires_delta
        encode.update({"exp": expire})
        encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
            email: str = payload.get("email")
            user_id: str = payload.get("id")
            print(email, user_id)
            if email is None or user_id is None:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials1")
            user = db.query(User).filter(User.id == user_id).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User no longer exists"
                )
            return user
        except JWTError:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials2")

auth = AuthService()

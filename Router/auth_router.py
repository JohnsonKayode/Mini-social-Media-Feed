from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from model import UserT
from schema.user import UserResponse, UserCreate, UserAuthLogin
from Service.auth_service import auth
import uuid


auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse, status_code=201)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     try:
#         details = auth.register_user(user, db)
#         if not details:
#             raise HTTPException(status_code=400, detail="User Already exists")
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
#     return details

def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # The service should handle the commit internally
        result = auth.register_user(user, db)
        return result
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@auth_router.post("/login")

# def login(user: UserAuthLogin, db: Session = Depends(get_db)):  # Use proper login schema
#     try:
#         access_token = auth.login_user(user, db)
#         if not access_token:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#         return access_token
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Login failed: {str(e)}"
        # )

    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(UserCreate(email=form_data.username, password=form_data.password), db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, user.id, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
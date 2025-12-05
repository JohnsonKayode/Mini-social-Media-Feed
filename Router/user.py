from fastapi import APIRouter, Depends
from database import user_db
import uuid
from database import get_db, engine, Base
from sqlalchemy.orm import Session
from uuid import UUID
from schema.user import User, UserCreate, UserUpdate
from Service.user import user_service


Base.metadata.create_all(bind=engine)

user_router = APIRouter()

@user_router.get("/users")
def get_all_users(user_db: Session = Depends(get_db)):
    user = user_service.get_all_users(user_db)
    return user

@user_router.get("/users/{user_id}")
def get_user_by_id(user_id: UUID, user_db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(user_id, user_db)
    if user:
        return user
    return {"error": "User not found"}

@user_router.post("/users")
def create_user(Createuser: UserCreate, user_db: Session = Depends(get_db)):
    details = user_service.create_user(Createuser, user_db)
    return details

@user_router.patch("/users/{user_id}")
def update_user(user_id: UUID, Updateuser: UserUpdate,  user_db: Session = Depends(get_db)):
    details = user_service.update_user(user_id, Updateuser, user_db)
    return details


@user_router.delete("/users/{user_id}")
def delete_user(user_id: UUID, user_db: Session = Depends(get_db)):
    details = user_service.delete_user(user_id, user_db)
    return details
            
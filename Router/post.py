from fastapi import APIRouter, Depends
from database import post_db, user_db, get_db, engine, Base
from sqlalchemy.orm import Session
from uuid import UUID
from schema.user import UserResponse
from schema.post import post, postcreate, postupdate, postresponse
import uuid
from Service.post import post_service

Base.metadata.create_all(bind=engine)

post_router = APIRouter()

@post_router.get("/posts")
def get_all_posts(post_db: Session = Depends(get_db)):
    post = post_service.get_all_post(post_db)
    return post

@post_router.get("/posts/{post_id}")
def get_post_by_id(post_id: UUID, post_db : Session = Depends(get_db)):
    post = post_service.get_post_by_id(post_id, post_db)
    return post

@post_router.post("/posts/{user_id}", response_model=postresponse)
def create_post(post: postcreate, user_id: UUID, post_db: Session = Depends(get_db), user_db: Session = Depends(get_db)):
    post = post_service.create_post(user_id, post, post_db, user_db)
    return post

@post_router.patch("/posts/{post_id}")
def update_post(post_id: UUID, updatepost: postupdate, post_db: Session = Depends(get_db)):
    details = post_service.update_post(post_id, updatepost, post_db)
    return details

@post_router.delete("/posts/{post_id}")
def delete_post(post_id: UUID, post_db: Session = Depends(get_db)):
    details = post_service.delete_post(post_id, post_db)
    return details

@post_router.get("/posts/user/{user_id}")
def get_posts_by_user_id(user_id: UUID, post_db: Session = Depends(get_db)):
    posts = post_service.get_posts_by_user_id(user_id, post_db)
    return posts

@post_router.get("/user/posts{user_id}")
def get_user_details_and_posts(user_id: UUID, db: Session = Depends(get_db)):
    details = post_service.get_user_and_posts(user_id, db)
    return details
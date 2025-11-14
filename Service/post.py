import uuid
from schema.post import postcreate, postupdate, post, postbase
from uuid import UUID, uuid4
from model import UserT, PostT
from sqlalchemy.orm import Session
from fastapi import status
from Service.user import user_service



class PostService:
    @staticmethod
    def get_all_post(user_db = Session):
        posts = user_db.query(PostT).all()
        return posts
    
    @staticmethod
    def get_post_by_id(post_id: uuid, post_db: Session):
        post = post_db.query(PostT).filter(PostT.id == str(post_id)).first()
        return post
    

    @staticmethod
    def create_post(id: UUID, createPost: postcreate, post_db: Session, user_db: Session):
        user = user_service.get_user_by_id(id, user_db)
        if user:
            post = PostT(id=str(uuid.uuid4()), user_id=user.id, **createPost.model_dump())
            post_db.add(post)
            post_db.commit()
            post_db.refresh(post)
            return {
                'message': 'Post Created Successfully',
                'details': post
            }
        return {"error": "User not found"}

    @staticmethod
    def update_post(post_id: UUID, updatepost: postupdate, post_db:  Session):
        post = post_service.get_post_by_id(post_id, post_db)
        if post:
            for key, value in updatepost.model_dump().items():
                if value is not None:
                    setattr(post, key, value)
                    post_db.commit()
                    post_db.refresh(post)
                    return {"message": "post updated successfully", "post": post}
        return {"error": "post not found"}
    

    @staticmethod
    def delete_post(post_id: UUID, post_db: Session):
        post = post_db.query(PostT).filter(PostT.id == str(post_id)).first()
        if post:
            post_db.delete(post)
            post_db.commit()
            return {"message": "Post deleted successfully"}
        return {"error": "Post not found"}
    
    @staticmethod
    def get_posts_by_user_id(user_id: UUID, post_db: Session):
        posts = post_db.query(PostT).filter(PostT.user_id == str(user_id)).all()
        return posts
    
    @staticmethod
    def get_user_and_posts(user_id: UUID, db: Session):
        user = user_service.get_user_by_id(user_id, db)
        if not user:
            return {"error": "User not found"}
        posts = post_service.get_posts_by_user_id(user_id, db)
        if not posts:
            return {"error": "No posts found for this user"}
        return {
            "user": user.full_name,
            "posts": posts
        }
        


post_service = PostService()
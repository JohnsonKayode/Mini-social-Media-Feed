import uuid
from schema.user import UserCreate, UserUpdate, User, UserBase
from uuid import UUID, uuid4
from model import UserT
from sqlalchemy.orm import Session
from fastapi import status



class UserService:
    @staticmethod
    def get_all_users(user_db = Session):
        users = user_db.query(UserT).all()
        return users
    
    @staticmethod
    def get_user_by_id(user_id: uuid, user_db: Session):
        user = user_db.query(UserT).filter(UserT.id == str(user_id)).first()
        return user
    

    @staticmethod
    def create_user(createUser:UserCreate, user_db: Session):
        user = UserT(id = str(uuid.uuid4()), **createUser.model_dump())
        user_db.add(user)
        user_db.commit()
        user_db.refresh(user)
        return {
            'message': 'User Created Successfully',
            'details': user
        }

    @staticmethod
    def update_user(user_id: UUID, Updateuser: UserUpdate, user_db:  Session):
        user = user_service.get_user_by_id(user_id, user_db)
        if user:
            for key, value in Updateuser.model_dump().items():
                if value is not None:
                    setattr(user, key, value)
                    user_db.commit()
                    user_db.refresh(user)
                    return {"message": "user updated successfully", "user": user}
        return {"error": "User not found"}
    

    @staticmethod
    def delete_user(user_id: UUID, user_db: Session):
        user = user_db.query(UserT).filter(UserT.id == user_id).first()
        if user:
            user_db.delete(user)
            user_db.commit()
            return {"message": "User deleted successfully"}
        return {"error": "User not found"}
    
user_service = UserService()
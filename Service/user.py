import uuid
from schema.user import UserCreate, UserUpdate, UserResponse, User, UserBase
from uuid import UUID, uuid4
from model import UserT
from sqlalchemy.orm import Session
from fastapi import status
from auth import verify_password



class UserService:
    @staticmethod
    def get_all_users(user_db : Session):
        users = user_db.query(UserT).all()
        return users
    
    @staticmethod
    def get_user_by_id(user_id: UUID, user_db: Session):
        user = user_db.query(UserT).filter(UserT.id == str(user_id)).first()
        return user
    
    @staticmethod
    def get_user_by_email(email: str, user_db: Session, password: str):
        user = user_db.query(UserT).filter(UserT.email == email).first()
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    

    @staticmethod
    def create_user(createUser:UserCreate, user_db: Session) -> UserResponse:
        user = UserT(id = str(uuid.uuid4()), **createUser.model_dump())
        user_db.add(user)
        user_db.commit()
        user_db.refresh(user)
        return UserResponse.from_orm(user)

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
        user = user_db.query(UserT).filter(UserT.id == str(user_id)).first()
        if not user:
            return {"error": "User not found"}
        user_db.delete(user)
        user_db.commit()
        return {"message": "User deleted successfully"}
    
user_service = UserService()
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class UserT(Base):

    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=False)
    full_name = Column(String, nullable=False)  
    email = Column(String, unique=False, nullable=False)
    bio = Column(String, default=None)


class PostT(Base):
    
    __tablename__ = "post"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
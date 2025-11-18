from pydantic import BaseModel, EmailStr, Field
import datetime
from typing import List
from schema.post import postresponse, postbase
from uuid import UUID


class UserBase(BaseModel):
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    full_name: str = Field(..., description="Full name of the user")
    password: str = Field(..., description="Password for the user account")
    bio: str = Field(None, description="Short biography of the user")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, description="Time the user was created")
    class Config:
        orm_mode = True

class User(UserBase):
    id: UUID = Field(..., description="Unique identifier for the user")
    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    full_name: str = None
    bio: str = None
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    users : List[UserBase] = []
    posts: List[postbase] = []
    class Config:
        orm_mode = True
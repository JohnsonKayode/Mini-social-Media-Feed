from pydantic import BaseModel, Field
from uuid import UUID

class postbase(BaseModel):
    title: str = Field(..., description="tittle of the post")
    content: str = Field(..., description="content of the post")
    class Config:
        orm_mode = True

class postcreate(postbase):
    pass
    class Config:
      orm_mode = True

class post(postbase):    
      id: UUID
      user_id: UUID
      class Config:
        orm_mode = True

class postupdate(BaseModel):
      title: str = None
      content: str = None
      class Config:
        orm_mode = True

class postresponse(BaseModel):
      message: str
      details: postbase
      class Config:
        orm_mode = True

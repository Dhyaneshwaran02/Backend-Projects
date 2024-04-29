from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post_base(BaseModel):
    title: str
    content: str

class User_base(BaseModel):
    email: EmailStr
    password: str

class Post(Post_base):
    pass
    class Config:
        extra = "forbid"


    class Config:
        from_attributes = True

class UserCreate(User_base):
    pass
    class Config:
        extra = "forbid"

class User_res(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class User_login(BaseModel):
    email:EmailStr
    password: str

class Post_base(BaseModel):
    title: str
    content: str

class Post_res(Post_base):
    id: int
    created_at: datetime
    owner_id:int
    owner: User_res
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    token_type: str
from typing import Optional

from pydantic import BaseModel, EmailStr


class PostBaseSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostSchema(PostBaseSchema):
    pass


class UserBaseSchema(BaseModel):
    email_id: EmailStr
    password: str


class UserSchema(UserBaseSchema):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str

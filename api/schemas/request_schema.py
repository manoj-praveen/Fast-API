from typing import Optional

from pydantic import BaseModel, EmailStr, conint


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


class VoteSchema(BaseModel):
    post_id: str
    vote_direction: conint(le=1)

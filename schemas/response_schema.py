from datetime import datetime

from pydantic import EmailStr
from pydantic.main import BaseModel

from schemas.request_schema import PostBaseSchema


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    email_id: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

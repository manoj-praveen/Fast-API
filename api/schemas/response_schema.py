from datetime import datetime

from pydantic import EmailStr
from pydantic.main import BaseModel

from api.schemas.request_schema import PostBaseSchema


class UserResponseSchema(BaseModel):
    email_id: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponseSchema(PostBaseSchema):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponseSchema

    class Config:
        orm_mode = True

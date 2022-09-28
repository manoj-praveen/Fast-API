from typing import Optional

from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int] = None

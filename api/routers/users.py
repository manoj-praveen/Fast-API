from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from api import models
from api.database_connection import get_db
from api.schemas.request_schema import UserSchema
from api.schemas.response_schema import UserResponseSchema
from api.utils import hash_password

user_router = APIRouter(
    prefix="/users", tags=['Users']
)


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema)
def create_user(request_payload: UserSchema, db: Session = Depends(get_db)):
    # hash the password
    request_payload.password = hash_password(request_payload.password)

    new_user = models.User(**request_payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with the given id doesn't exists - id: {user_id}"
        )
    return user

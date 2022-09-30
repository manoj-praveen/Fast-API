from fastapi import status, Depends, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api import models
from api.database_connection import get_db
from api.routers.oauth2 import create_access_token
from schemas.request_schema import Token
from utils.utils import verify_password

auth_router = APIRouter(
    prefix="/login", tags=['Authentication']
)


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
def login(request_payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email_id == request_payload.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials."
        )
    if not verify_password(request_payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials."
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

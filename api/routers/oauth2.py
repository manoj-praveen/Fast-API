from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from api import models
from api.config import settings
from api.database_connection import get_db
from api.schemas.request_schema import TokenData

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire_time})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt
    except Exception as error:
        print(f"Failed to generate access token. Error: {error}")


def verify_access_token(token: str, token_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise token_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise token_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Failed to validate Credentials",
        headers={"www-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, token_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user.id

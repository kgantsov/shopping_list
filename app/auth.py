from datetime import datetime
from datetime import timedelta

import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED


from app.models.auth import UserModel


security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# openssl rand -hex 32
SECRET_KEY = "c1669dfb649fdf59354d6cc7403cd4f16ea0f2f3d6ee6180bf452bf640472a6f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


async def get_user(user_id: int):
    user = await UserModel.query.where(UserModel.id == user_id).gino.first()

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(security)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = await get_user(user_id=user_id)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

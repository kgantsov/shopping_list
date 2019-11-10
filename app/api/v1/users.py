from fastapi import APIRouter
from fastapi import Depends

from app.auth import get_current_active_user
from app.auth import get_password_hash
from app.models.auth import UserModel
from app.schemas.users import UserSchema


router = APIRouter()


@router.get("/users/me")
async def read_current_user(user: UserModel = Depends(get_current_active_user)):
    return {"username": user.name, "email": user.email}


@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserSchema):
    await UserModel.create(name=user.name, email=user.email, password_hash=get_password_hash(user.password))
    return user

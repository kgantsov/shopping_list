from datetime import timedelta
from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.auth import LoginSchema
from app.models.auth import UserModel
from app.auth import verify_password
from app.auth import create_access_token
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


@router.post("/token")
async def login(form_data: LoginSchema):
    user = await UserModel.query.where(UserModel.email == form_data.email).gino.first()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

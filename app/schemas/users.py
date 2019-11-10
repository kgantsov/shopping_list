from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int = 0
    name: str
    email: str
    password: str

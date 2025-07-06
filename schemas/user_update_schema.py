from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    username: str
    email: EmailStr

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

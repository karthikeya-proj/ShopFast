from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserRegister, UserLogin
from models.user import user_collection
from passlib.context import CryptContext
from auth.auth_handler import create_access_token

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/register")
async def register(user: UserRegister):
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": "user"  # Default role
    }
    await user_collection.insert_one(user_dict)
    return {"message": "User registered successfully"}

@auth_router.post("/login")
async def login(user: UserLogin):
    db_user = await user_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": db_user["username"], "role": db_user["role"]})
    return {"access_token": token}

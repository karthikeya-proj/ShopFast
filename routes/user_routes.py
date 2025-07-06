from fastapi import APIRouter, Depends, HTTPException
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decode_access_token
from models.user import user_collection
from schemas.user_update_schema import UserUpdate, ChangePassword
from passlib.context import CryptContext
from bson import ObjectId

user_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Get profile from JWT token only (quick check)
@user_router.get("/profile", dependencies=[Depends(JWTBearer())])
async def get_profile_from_token(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    return {
        "username": payload["sub"],
        "role": payload["role"]
    }

# ✅ Get full user profile from DB
@user_router.get("/user/profile", dependencies=[Depends(JWTBearer())])
async def get_full_profile(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    user = await user_collection.find_one({"username": username}, {"password": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    return user

# ✏️ Update username/email
@user_router.put("/user/update", dependencies=[Depends(JWTBearer())])
async def update_profile(data: UserUpdate, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    await user_collection.update_one(
        {"username": username},
        {"$set": {"username": data.username, "email": data.email}}
    )

    return {"message": "Profile updated successfully"}

# 🔑 Change password
@user_router.put("/user/change-password", dependencies=[Depends(JWTBearer())])
async def change_password(data: ChangePassword, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    user = await user_collection.find_one({"username": username})
    if not user or not pwd_context.verify(data.old_password, user["password"]):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    new_hashed = pwd_context.hash(data.new_password)

    await user_collection.update_one(
        {"username": username},
        {"$set": {"password": new_hashed}}
    )

    return {"message": "Password changed successfully"}

# 🔐 Admin-only route
@user_router.get("/admin-only", dependencies=[Depends(JWTBearer())])
async def admin_area(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only.")

    return {"message": f"Welcome Admin {payload['sub']}"}

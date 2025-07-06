from fastapi import APIRouter, Depends, HTTPException
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decode_access_token
from models.cart import cart_collection
from models.product import product_collection
from schemas.cart_schema import CartItem
from bson import ObjectId

cart_router = APIRouter()

# 🛒 Add product to cart
@cart_router.post("/cart/add", dependencies=[Depends(JWTBearer())])
async def add_to_cart(item: CartItem, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    product = await product_collection.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await cart_collection.insert_one({
        "username": username,
        "product_id": item.product_id,
        "quantity": item.quantity
    })
    return {"message": "Item added to cart"}

# 🛍 View items in cart
@cart_router.get("/cart", dependencies=[Depends(JWTBearer())])
async def view_cart(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    cart_items = []
    async for item in cart_collection.find({"username": username}):
        product = await product_collection.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            cart_items.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"]
            })
    return cart_items

# ❌ Remove from cart
@cart_router.delete("/cart/{product_id}", dependencies=[Depends(JWTBearer())])
async def remove_from_cart(product_id: str, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    result = await cart_collection.delete_one({"username": username, "product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    return {"message": "Item removed from cart"}
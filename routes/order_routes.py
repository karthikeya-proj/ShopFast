from fastapi import APIRouter, Depends, HTTPException
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decode_access_token
from models.cart import cart_collection
from models.product import product_collection
from models.order import order_collection
from schemas.order_schema import OrderItem
from bson import ObjectId

order_router = APIRouter()

# ✅ Place order
@order_router.post("/orders", dependencies=[Depends(JWTBearer())])
async def place_order(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    cart_items = cart_collection.find({"username": username})
    order_items = []
    total = 0

    async for item in cart_items:
        product = await product_collection.find_one({"_id": ObjectId(item["product_id"])})
        if not product:
            continue
        price = product["price"]
        qty = item["quantity"]
        total += price * qty

        order_items.append({
            "product_id": item["product_id"],
            "name": product["name"],
            "quantity": qty,
            "price": price
        })

    if not order_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    await order_collection.insert_one({
        "username": username,
        "items": order_items,
        "total": total
    })

    await cart_collection.delete_many({"username": username})

    return {"message": "Order placed successfully", "total": total}

# 📜 View order history
@order_router.get("/orders", dependencies=[Depends(JWTBearer())])
async def get_orders(token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    username = payload["sub"]

    orders = []
    async for order in order_collection.find({"username": username}):
        order["_id"] = str(order["_id"])
        orders.append(order)
    return orders

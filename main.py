from fastapi import FastAPI 
from database.connect import db
from routes.auth_routes import auth_router
from routes.user_routes import user_router
from routes.product_routes import product_router
from routes.cart_routes import cart_router
from routes.order_routes import order_router
app=FastAPI()

app.include_router(cart_router, tags=["Cart"])
app.include_router(order_router, tags=["Orders"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(product_router, prefix="/products", tags=["Products"])

@app.get("/")
async def home():
    return {"message":"Welcome to ShopFast"} 

@app.get("/test-db")
async def test_db():
    collections = await db.list_collection_names()
    return{"collections":collections}

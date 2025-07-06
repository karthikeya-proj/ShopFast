from fastapi import APIRouter, HTTPException, Depends, Query
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decode_access_token
from schemas.product_schema import ProductCreate, ProductUpdate
from models.product import product_collection
from bson import ObjectId, errors

product_router = APIRouter()

#  Helper to format MongoDB ObjectId
def product_helper(product) -> dict:
    product["_id"] = str(product["_id"])
    return product

#  Admin-only: Create Product
@product_router.post("/", dependencies=[Depends(JWTBearer())])
async def create_product(product: ProductCreate, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can add products")

    result = await product_collection.insert_one(product.dict())
    return {"message": "Product created", "id": str(result.inserted_id)}

# Public: Get All Products
@product_router.get("/")
async def get_all_products():
    products = []
    async for p in product_collection.find():
        products.append(product_helper(p))
    return products

#  Public: Search Products (MUST come before dynamic /{id})
@product_router.get("/search")
async def search_products(query: str = Query(..., min_length=1)):
    try:
        products = await product_collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }).to_list(length=100)

        return [product_helper(p) for p in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

#  Public: Filter Products
@product_router.get("/filter")
async def filter_products(
    min_price: float = 0,
    max_price: float = 999999,
    min_stock: int = 0
):
    try:
        filters = {
            "price": {"$gte": min_price, "$lte": max_price},
            "stock": {"$gte": min_stock}
        }

        products = await product_collection.find(filters).to_list(length=100)
        return [product_helper(p) for p in products]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Filter failed: {str(e)}")

#  Public: Get Product by ID (MUST come last!)
@product_router.get("/{product_id}")
async def get_product(product_id: str):
    try:
        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product_helper(product)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")

#  Admin-only: Update Product
@product_router.put("/{product_id}", dependencies=[Depends(JWTBearer())])
async def update_product(product_id: str, updated: ProductUpdate, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update products")

    try:
        result = await product_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updated.dict()}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="No changes or product not found")
        return {"message": "Product updated"}
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")

#  Admin-only: Delete Product
@product_router.delete("/{product_id}", dependencies=[Depends(JWTBearer())])
async def delete_product(product_id: str, token: str = Depends(JWTBearer())):
    payload = decode_access_token(token)
    if payload["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete products")

    try:
        result = await product_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product deleted"}
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID")

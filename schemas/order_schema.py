from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: str
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    items: List[OrderItem]
    total: float

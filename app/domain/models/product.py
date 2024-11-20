from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: str
    promo_price: str

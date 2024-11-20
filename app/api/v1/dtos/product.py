from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

from app.domain.models.product import Product

class ProductRequest(BaseModel):
    url: HttpUrl
    num_products: Optional[int] = Field(None, ge=1) 


class ProductsResponse(BaseModel):
    products: List[Product]
    url: str
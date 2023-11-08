from typing import Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Product

ProductRetrieveSchema = pydantic_model_creator(Product, name="Product")


class ProductCreateUpdateSchema(BaseModel):
    name: str = Field(..., max_length=150)
    description: str = Field(..., max_length=255)
    price: float = Field(..., gt=0)
    #owner_id: int = Field(..., gt=0)


class ProductPartialUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    description: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    #owner_id: Optional[int] = Field(None, gt=0)

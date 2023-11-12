from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Product

ProductRetrieveSchema = pydantic_model_creator(Product, name="Product")


class ProductCreateUpdateSchema(BaseModel):
    """
    Pydantic schema for creating or updating a product.

    Attributes:
    - `name` (str): The name of the product.
    - `description` (str): The description of the product.
    - `price` (float): The price of the product.

    """
    name: str = Field(..., max_length=150)
    description: str = Field(..., max_length=255)
    price: float = Field(..., gt=0)

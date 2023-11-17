from pydantic import BaseModel, Field


class CartCreateSchema(BaseModel):
    """
    Pydantic schema for creating or updating a cart.
    Attributes:
    - `product_id` (int): The ID of the product.
    - `quantity` (int): The quantity of the product in the cart.
    """
    product_id: int
    quantity: int


class CartUpdateSchema(BaseModel):
    quantity: int


class CartSchema(BaseModel):
    """
    Pydantic schema for representing a cart item.
    Attributes:
    - `id` (int): The ID of the cart item.
    - `user_id` (int): The ID of the user.
    - `product_id` (int): The ID of the product.
    - `quantity` (int): The quantity of the product in the cart.
    """
    user_id: int
    product_id: int
    quantity: int
    total_price: float = Field(None)

    class Config:
        from_attributes = True

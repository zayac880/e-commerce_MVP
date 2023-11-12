from tortoise.models import Model
from tortoise import fields


class Product(Model):
    """
    Represents a product in the system.

    Attributes:
    - `id` (int): The unique identifier for the product.
    - `name` (str): The name of the product.
    - `price` (Decimal): The price of the product.
    - `description` (str): The description of the product.
    - `created_at` (Datetime): The timestamp when the product was created.
    - `updated_at` (Datetime): The timestamp when the product was last updated.
    - `is_active` (bool): Indicates whether the product is currently active.

    Methods:
    - `__str__`: Returns the string representation of the product.
    """
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    description = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.name

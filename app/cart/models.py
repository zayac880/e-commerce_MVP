from tortoise.models import Model
from tortoise import fields


class Cart(Model):
    """
    Represents an item in the user's cart.
    Attributes:
    - `id` (int): The unique identifier for the cart item.
    - `user` (fields.ForeignKeyField): The user associated with the cart item.
    - `product` (fields.ForeignKeyField): The product associated with the cart item.
    - `quantity` (fields.IntField): The quantity of the product in the cart.
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='user_cart')
    product = fields.ForeignKeyField('models.Product', related_name='product_cart')
    quantity = fields.IntField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('user', 'product')

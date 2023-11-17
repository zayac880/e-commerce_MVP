from typing import List, Optional
from tortoise.exceptions import IntegrityError

from .models import Cart
from .schemas import CartCreateSchema, CartSchema, CartUpdateSchema


async def create_cart(cart_data: CartCreateSchema, user_id) -> Cart:
    try:
        cart = await Cart.create(**cart_data.model_dump(), user_id=user_id)
        return cart
    except IntegrityError:
        return None


async def get_list_cart(user_id: int) -> List[CartSchema]:
    cart_list = await Cart.filter(user_id=user_id).all()
    return cart_list


async def update_cart(user_id: int, product_id: int, cart_data: CartUpdateSchema) -> Optional[Cart]:
    cart = await Cart.filter(product_id=product_id, user_id=user_id).update(**cart_data.model_dump())

    if cart:
        return await Cart.get(product_id=product_id, user_id=user_id)
    return None


async def delete_cart(product_id: int, user_id: int) -> bool:
    cart = await Cart.filter(product_id=product_id, user_id=user_id).first()
    if cart:
        await cart.delete()
        return True
    else:
        return False

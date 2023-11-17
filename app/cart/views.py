from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated, List

from app.cart.services import create_cart, get_list_cart, update_cart, delete_cart
from app.cart.schemas import CartCreateSchema, CartSchema, CartUpdateSchema
from app.users.models import User
from app.users.services import get_current_user

cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.post("/create", response_model=CartSchema)
async def create_cart_view(cart_data: CartCreateSchema, current_user: Annotated[User, Depends(get_current_user)]):
    cart_item = await create_cart(cart_data, current_user.id)
    if cart_item:
        return CartSchema(**cart_item.__dict__)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart with the product already exists"
        )


@cart_router.get("/", response_model=List[CartSchema])
async def get_list_cart_view(current_user: User = Depends(get_current_user)):
    return await get_list_cart(current_user.id)


@cart_router.put("/{product_id}", response_model=CartSchema)
async def update_cart_view(
    product_id: int, cart_data: CartUpdateSchema, current_user: User = Depends(get_current_user)
):
    return await update_cart(current_user.id, product_id, cart_data)


@cart_router.delete("/{product_id}")
async def delete_cart_view(product_id: int, current_user: User = Depends(get_current_user)):
    deleted = await delete_cart(product_id, current_user.id)
    if deleted:
        return {"detail": "Successfully deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )

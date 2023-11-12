from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import ProductCreateUpdateSchema, ProductRetrieveSchema
from .services import (
    create_product, get_product,
    update_product, delete_product,
    get_products
)

from ..users.services import get_current_user

product_router = APIRouter()


@product_router.post("/products/",
                     dependencies=[Depends(get_current_user)]
                     )
async def create_product_view(product_data: ProductCreateUpdateSchema):
    product = await create_product(product_data)
    if product:
        return await ProductRetrieveSchema.from_tortoise_orm(product)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.get("/products/{product_id}",
                    response_model=ProductRetrieveSchema,
                    dependencies=[Depends(get_current_user)]
                    )
async def get_product_view(product_id: int):

    product = await get_product(product_id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.put("/products/{product_id}",
                    response_model=ProductRetrieveSchema,
                    dependencies=[Depends(get_current_user)]
                    )
async def update_product_view(
        product_id: int,
        product_data: ProductCreateUpdateSchema
):
    product = await update_product(product_id, product_data)
    if product:
        return await ProductRetrieveSchema.from_tortoise_orm(product)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.delete("/products/{product_id}",
                       response_model=dict,
                       dependencies=[Depends(get_current_user)]
                       )
async def delete_product_view(product_id: int):
    result = await delete_product(product_id)
    if result:
        return {"message": "Product deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.get("/products/",
                    response_model=list[ProductRetrieveSchema],
                    dependencies=[Depends(get_current_user)]
                    )
async def get_products_view(skip: int = 0, limit: int = 10):
    products = await get_products(skip, limit)
    return products

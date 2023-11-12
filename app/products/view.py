from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import ProductCreateUpdateSchema, ProductRetrieveSchema
from .services import (
    create_product, get_product,
    update_product, delete_product,
    get_products
)

from ..users.services import get_current_user

product_router = APIRouter(prefix="/products", tags=["Products"])


@product_router.post("/create",
                     dependencies=[Depends(get_current_user)]
                     )
async def create_product_view(product_data: ProductCreateUpdateSchema):
    """
    Create a new product.

    Args:
    - `product_data` (ProductCreateUpdateSchema):
    The data for creating the product.

    Returns:
    - `ProductRetrieveSchema`:
    The created product.

    Raises:
    - `HTTPException`:
    If the product cannot be created.
    """
    product = await create_product(product_data)
    if product:
        return await ProductRetrieveSchema.from_tortoise_orm(product)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.get("/{product_id}",
                    response_model=ProductRetrieveSchema,
                    dependencies=[Depends(get_current_user)]
                    )
async def get_product_view(product_id: int):
    """
    Get a product by its ID.

    Args:
    - `product_id` (int): The ID of the product to retrieve.

    Returns:
    - `ProductRetrieveSchema`: The retrieved product.

    Raises:
    - `HTTPException`: If the product with the given ID is not found.
    """
    product = await get_product(product_id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.put("/{product_id}",
                    response_model=ProductRetrieveSchema,
                    dependencies=[Depends(get_current_user)]
                    )
async def update_product_view(
        product_id: int,
        product_data: ProductCreateUpdateSchema
):
    """
    Update a product by its ID.

    Args:
    - `product_id` (int):
     The ID of the product to update.
    - `product_data` (ProductCreateUpdateSchema):
     The data for updating the product.

    Returns:
    - `ProductRetrieveSchema`:
    The updated product.

    Raises:
    - `HTTPException`: If the product with the given ID is not found.
    """
    product = await update_product(product_id, product_data)
    if product:
        return await ProductRetrieveSchema.from_tortoise_orm(product)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.delete("/{product_id}",
                       response_model=dict,
                       dependencies=[Depends(get_current_user)]
                       )
async def delete_product_view(product_id: int):
    """
    Delete a product by its ID.

    Args:
    - `product_id` (int): The ID of the product to delete.

    Returns:
    - `message`: A message indicating successful deletion.

    Raises:
    - `HTTPException`: If the product with the given ID is not found.
    """
    result = await delete_product(product_id)
    if result:
        return {"message": "Product deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


@product_router.get("/",
                    response_model=list[ProductRetrieveSchema],
                    dependencies=[Depends(get_current_user)]
                    )
async def get_products_view(skip: int = 0, limit: int = 10):
    """
    Get a list of products with optional pagination.

    Args:
    - `skip` (int):
     The number of products to skip.
    - `limit` (int):
    The maximum number of products to retrieve.

    Returns:
    - `List[ProductRetrieveSchema]`:
     A list of products based on the specified skip and limit.
    """
    products = await get_products(skip, limit)
    return products

from .models import Product
from .schemas import ProductCreateUpdateSchema


async def create_product(product_data: ProductCreateUpdateSchema):
    """
    Create a new product.

    Args:
    - `product_data` (ProductCreateUpdateSchema):
     The data for creating the product.

    Returns:
    - `Product`: The created product.
    """
    product = await Product.create(**product_data.model_dump())
    return product


async def get_product(product_id: int):
    """
    Get a product by its ID.

    Args:
    - `product_id` (int): The ID of the product to retrieve.

    Returns:
    - `Product` | `None`: The retrieved product or None if not found.
    """
    product = await Product.filter(id=product_id, is_active=True).first()
    return product


async def update_product(
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
    - `Product` | `None`:
    The updated product or None if the product doesn't exist.
    """
    product = await Product.filter(id=product_id).first()
    if product:
        await product.update_from_dict(
            product_data.model_dump(exclude_unset=True)
        )
        await product.save()
        return product
    else:
        return None


async def delete_product(product_id: int):
    """
    Delete a product by its ID.

    Args:
    - `product_id` (int): The ID of the product to delete.

    Returns:
    - `None`: Returns None regardless of success or failure.
    """
    product = await Product.filter(id=product_id).first()
    if product:
        await product.delete()
    else:
        return None


async def get_products(skip: int = 0, limit: int = 10, is_active: bool = True):
    """
    Get a list of products with optional pagination.

    Args:
    - `skip` (int):
    The number of products to skip.
    - `limit` (int):
    The maximum number of products to retrieve.

    Returns:
    - `List[Product]`:
    A list of products based on the specified skip and limit.
    """
    query = Product.filter(is_active=is_active).offset(skip).limit(limit)
    products = await query.all()
    return products

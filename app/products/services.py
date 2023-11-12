from .models import Product
from .schemas import ProductCreateUpdateSchema


async def create_product(product_data: ProductCreateUpdateSchema):
    product = await Product.create(**product_data.model_dump())
    return product


async def get_product(product_id: int):
    product = await Product.filter(id=product_id).first()
    if product:
        return product
    else:
        return None


async def update_product(
        product_id: int,
        product_data: ProductCreateUpdateSchema
):
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
    product = await Product.filter(id=product_id).first()
    if product:
        await product.delete()
    else:
        return None


async def get_products(skip: int = 0, limit: int = 10):
    products = await Product.all().offset(skip).limit(limit)
    return products

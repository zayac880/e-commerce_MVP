from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import DATABASE_URL, MODELS
from app.products.view import product_router
from app.users.views import user_router


def setup_database(app: FastAPI):
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={
            "models": [*MODELS],
        },
        generate_schemas=True,
    )


def setup_routes(app: FastAPI):
    app.include_router(product_router)
    app.include_router(user_router)

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import DATABASE_URL, MODELS
from app.products.view import product_router
from app.users.views import user_router


def setup_database(app: FastAPI):
    """
    Set up the Tortoise ORM database for the FastAPI application.

    This function
    configures Tortoise ORM
    with the specified database URL and models,
    generating schemas if needed.

    Parameters:
    - `app`: The FastAPI application instance.
    """
    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={
            "models": [*MODELS],
        },
        generate_schemas=True,
    )


def setup_routes(app: FastAPI):
    """
    Set up the FastAPI
    application routes.
    This function includes the routers for
    products and users in the FastAPI application.

    Parameters:
    - `app`: The FastAPI application instance.
    """
    app.include_router(product_router)
    app.include_router(user_router)

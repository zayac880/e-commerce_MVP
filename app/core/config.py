import os

POSTGRES_DB: str = os.getenv("POSTGRES_DB", "commerce_db")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "alzy")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)

DATABASE_LOGIN = f"asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
DATABASE_CONNECT = f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

DATABASE_URL = DATABASE_LOGIN + DATABASE_CONNECT

MODELS = [
    #"app.users.models",
    "app.products.models",
    # "app.models.cart",
    # "app.models.order",
    # "app.models.payment",
]

# Tortoise ORM settings
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL
    },
    "apps": {
        "models": {
            "models": [
                *MODELS,
                "aerich.models"
            ],
            "default_connection": "default",
            "generate_schemas": True,
            "add_exception_handlers": False,
        },
    },
}

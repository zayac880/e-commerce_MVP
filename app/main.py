from fastapi import FastAPI

from app.factory import setup_database, setup_routes

app = FastAPI()


setup_database(app)
setup_routes(app)

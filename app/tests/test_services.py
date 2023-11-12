import pytest
from httpx import AsyncClient

from app.main import app
from app.products.models import Product
from app.users.models import User


@pytest.mark.asyncio
async def test_create_user(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users/register",
            json={
               "full_name": "test",
               "email": "test@example.com",
               "phone": "+79500664444",
               "password": "Test1234!",
               "confirm_password": "Test1234!"
               }
            )
        assert response.status_code == 200
        assert response.json()["full_name"] == "test"
        assert response.json()["email"] == "test@example.com"
        assert response.json()["phone"] == "+79500664444"


@pytest.mark.asyncio
async def test_user_login(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
            )

        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_product(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        login_response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        response = await client.post(
            "/products/create",
            json={
                "name": "test",
                "description": "description",
                "price": 1000.00
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        assert response.json()["name"] == "test"
        assert response.json()["description"] == "description"
        assert float(response.json()["price"]) == 1000.00

        # Сохранение ID созданного продукта
        created_product_id = response.json()["id"]

        # Передача ID в следующий тест
        return created_product_id


@pytest.mark.asyncio
async def test_get_product(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        created_product_id = await test_create_product(test_db)

        login_response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        response = await client.get(
            f"/products/{created_product_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        assert response.json()["name"] == "test"
        assert response.json()["description"] == "description"
        assert float(response.json()["price"]) == 1000.00


@pytest.mark.asyncio
async def test_update_product(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        created_product_id = await test_create_product(test_db)

        login_response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        response = await client.put(
            f"/products/{created_product_id}",
            json={
                "name": "test123",
                "description": "description",
                "price": 2000,
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        assert response.json()["name"] == "test123"
        assert response.json()["description"] == "description"
        assert float(response.json()["price"]) == 2000.00


@pytest.mark.asyncio
async def test_get_products(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        login_response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        response = await client.get(
            "/products/",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 200
        assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_delete_product(test_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        created_product_id = await test_create_product(test_db)
        login_response = await client.post(
            "/users/login",
            data={
                "username": "test@example.com",
                "password": "Test1234!"
            }
        )
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        response = await client.delete(
            f"/products/{created_product_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
        await User.filter(email="test@example.com").delete()
        await Product.all().delete()

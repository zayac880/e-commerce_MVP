from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.users.auth import generate_tokens
from app.users.schemas import UserCreate, UserReg
from app.users.services import register_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/register", response_model=UserReg)
async def register(user_data: UserCreate):
    """
    Register a new user.

    Args:
    - `user_data` (UserCreate): Data for creating a new user.

    Raises:
    - `HTTPException`: If a user with the provided email already exists.

    Returns:
    - `UserReg`: Information about the registered user.
    """
    user = await register_user(user_data)
    return UserReg(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        status_message="Пользователь успешно зарегистрирован"
    )


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get the current authenticated user.

    Args:
    - `token` (str): The user's access token.

    Raises:
    - `HTTPException`: If the provided token is invalid.

    Returns:
    - `User`: The current authenticated user.
    """
    token = await generate_tokens(form_data.username, form_data.password)
    return token

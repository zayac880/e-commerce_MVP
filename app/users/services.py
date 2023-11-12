from fastapi import Depends, HTTPException
from .auth import oauth2_scheme, verify_token

from app.users.models import User
from app.users.schemas import UserCreate
from passlib.hash import bcrypt


async def register_user(user_data: UserCreate):
    """
      Register a new user.

      Args:
      - `user_data` (UserCreate): Data for creating a new user.

      Raises:
      - `ValueError`: If a user with the provided email already exists.

      Returns:
      - `User`: The newly created user.

      Example:
      ```python
      user_data = UserCreate(
      full_name="John Doe",
      email="john@example.com",
      phone="+71234567890",
      password="Password123!")
      user = await register_user(user_data)
      ```
      """
    if await User.filter(email=user_data.email).first():
        raise ValueError("User with this email already exists")

    user = await User.create(
        full_name=user_data.full_name,
        email=user_data.email,
        phone=user_data.phone,
        password_hash=bcrypt.hash(user_data.password)
    )
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
      Get the current authenticated user.

      Args:
      - `token` (str): The authentication token.

      Raises:
      - `HTTPException`:
      If the provided token is invalid or the user cannot be authenticated.

      Returns:
      - `User`: The authenticated user.

      Example:
      ```python
      user = await get_current_user("valid_token_here")
      ```
      """
    user = await verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

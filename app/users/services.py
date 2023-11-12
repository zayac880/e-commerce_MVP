from fastapi import Depends, HTTPException
from .auth import oauth2_scheme, verify_token

from app.users.models import User
from app.users.schemas import UserCreate
from passlib.hash import bcrypt


async def register_user(user_data: UserCreate):
    # Проверка уникальности email перед созданием пользователя
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
    user = await verify_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.users.auth import generate_tokens
from app.users.schemas import UserCreate, UserReg
from app.users.services import register_user

user_router = APIRouter()


@user_router.post("/register/", response_model=UserReg)
async def register(user_data: UserCreate):
    user = await register_user(user_data)
    return UserReg(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        status_message="Пользователь успешно зарегистрирован"
    )


@user_router.post("/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = await generate_tokens(form_data.username, form_data.password)
    return token

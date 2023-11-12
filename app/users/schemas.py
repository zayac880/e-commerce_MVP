from pydantic import BaseModel, EmailStr, constr, validator
from fastapi import HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator
from app.users.models import User


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: constr(strict=True)

    @validator("phone")
    def validate_phone(cls, value):
        if not value.startswith("+7") or not \
                value[1:].isdigit() or \
                len(value) != 12:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Телефон должен начинаться "
                       "с +7 и содержать 10 цифр после этого"
            )
        return value


class UserCreate(UserBase):
    password: constr(min_length=8, strict=True)
    confirm_password: constr(min_length=8, strict=True)

    @validator("password")
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать хотя бы 1 заглавную букву"
            )

        if not any(char in "$%&!:" for char in value):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать хотя бы 1"
                       " из спецсимволов: $%&!:"
            )
        return value

    @validator("confirm_password", pre=True, always=True)
    def validate_confirm_password(cls, confirm_password, values):
        if "password" in values and values["password"] != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароли не совпадают"
            )
        return confirm_password


class UserReg(UserBase):
    pass


UserOut = pydantic_model_creator(
    User,
    name="user",
    exclude=("password",)
)


class UserLogin(BaseModel):
    email_or_phone: str
    password: str

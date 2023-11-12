from pydantic import BaseModel, EmailStr, constr, validator
from fastapi import HTTPException, status
from tortoise.contrib.pydantic import pydantic_model_creator
from app.users.models import User


class UserBase(BaseModel):
    """
    Base Pydantic model for user data.

    Attributes:
    - `full_name` (str): The full name of the user.
    - `email` (EmailStr): The email address of the user.
    - `phone` (constr, strict=True): The phone number of the user.

    Validators:
    - `validate_phone`: Ensures the phone number format is valid.

    Example:
    ```python
    user_data = UserBase(
    full_name="John Doe",
    email="john@example.com",
    phone="+71234567890"
    )
    ```
    """
    full_name: str
    email: EmailStr
    phone: constr(strict=True)

    @validator("phone")
    def validate_phone(cls, value):
        """
        Validate the phone number format.

        Parameters:
        - `value` (str): The phone number to be validated.

        Returns:
        - The validated phone number.

        Raises:
        - HTTPException with 422 status code if
        the phone number format is invalid.
        """
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
    """
    Pydantic model for user creation.

    Inherits from UserBase and adds:
    - `password` (constr, min_length=8, strict=True):
     The user's password.
    - `confirm_password` (constr, min_length=8, strict=True):
     Confirmation of the user's password.

    Validators:
    - `validate_password`:
     Ensures the password meets certain criteria.
    - `validate_confirm_password`:
     Ensures the confirmation password matches the original.

    Example:
    ```python
    user_data = UserCreate(
        full_name="John Doe",
        email="john@example.com",
        phone="+71234567890",
        password="Password123!",
        confirm_password="Password123!"
    )
    ```

    """
    password: constr(min_length=8, strict=True)
    confirm_password: constr(min_length=8, strict=True)

    @validator("password")
    def validate_password(cls, value):
        """
        Validate the password format.

        Parameters:
        - `value` (str): The password to be validated.

        Returns:
        - The validated password.

        Raises:
        - HTTPException with 422 status code if the password format is invalid.
        """
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
        """
        Validate the confirmation password.

        Parameters:
        - `confirm_password` (str): The confirmation password to be validated.
        - `values` (dict): The values of the model.

        Returns:
        - The validated confirmation password.

        Raises:
        - HTTPException with 422 status code if
        the confirmation password doesn't match the original.
        """
        if "password" in values and values["password"] != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароли не совпадают"
            )
        return confirm_password


class UserReg(UserBase):
    """
    Pydantic model for user registration.

    Inherits from UserBase with no additional fields.

    Example:
    ```python
    user_data = UserReg(
    full_name="John Doe",
    email="john@example.com",
    phone="+71234567890"
    )
    ```

    """
    pass


UserOut = pydantic_model_creator(
    User,
    name="user",
    exclude=("password",)
)


class UserLogin(BaseModel):
    """
    Pydantic model for user login.

    Attributes:
    - `email_or_phone` (str):
    The email or phone number used for login.
    - `password` (str):
     The user's password.

    Example:
    ```python
    login_data = UserLogin(
    email_or_phone="john@example.com",
     password="Password123!"
     )
    ```

    """
    email_or_phone: str
    password: str

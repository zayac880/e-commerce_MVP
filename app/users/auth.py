import calendar
import datetime

from fastapi.security import OAuth2PasswordBearer

from app.users.models import User
from passlib.hash import bcrypt
from fastapi import HTTPException

from jose import JWTError, jwt
from app.core.config import JWT_SECRET, JWT_ALGORITHM
from app.users.schemas import UserOut


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login/")


async def authenticate_user(email_or_phone: str, password: str):
    """
    Authenticate a user based on email or phone and password.

    Parameters:
    - `email_or_phone`: The email or phone provided by the user.
    - `password`: The password provided by the user.

    Returns:
    - The authenticated user.

    Raises:
    - HTTPException with a status code of 401 if the credentials are invalid.

    Example:
    ```python
    user = await authenticate_user("user@example.com", "Password123!")
    ```

    """
    is_email = "@" in email_or_phone

    if is_email:
        user = await User.get(email=email_or_phone)
    else:
        user = await User.get(phone=email_or_phone)

    if user and user.verify_password(password):
        return user
    raise HTTPException(status_code=401, detail="Invalid credentials")


def compare_passwords(db_pass_hash, received_pass):
    """
    Compare a hashed password from the
    database with a received hashed password.

    Parameters:
    - `db_pass_hash`:
    The hashed password stored in the database.
    - `received_pass`:
    The hashed password received from the user.

    Returns:
    - True if the passwords match, False otherwise.

    Example:
    ```python
    result = compare_passwords("$2b$12$...", "$2b$12$...")
    ```

    """
    received_pass_hash = bcrypt.hash(received_pass)
    return received_pass_hash == db_pass_hash


async def generate_tokens(email_or_phone, password):
    """
    Generate JWT tokens for authentication.

    Parameters:
    - `email_or_phone`: The email or phone provided by the user.
    - `password`: The password provided by the user.

    Returns:
    - A dictionary containing the generated access token.

    Example:
    ```python
    tokens = await generate_tokens("user@example.com", "Password123!")
    ```

    """
    user = await authenticate_user(email_or_phone, password)

    data = {
        "phone": user.phone,
        "email": user.email,
    }

    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)

    return {"access_token": access_token}


async def verify_token(token):
    """
    Verify and decode a JWT token.

    Parameters:
    - `token`: The JWT token to be verified.

    Returns:
    - The user details if the token is valid.

    Raises:
    - HTTPException with a status code of 401 if the token is invalid.

    Example:
    ```python
    user_details = await verify_token("eyJhbGciOi...")
    ```

    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, [JWT_ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        user = await User.filter(email=email).first()
        if user is None:
            raise credentials_exception
        return await UserOut.from_tortoise_orm(user)
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Could not decode token"
        ) from e

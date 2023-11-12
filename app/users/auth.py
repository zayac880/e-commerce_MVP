import calendar
import datetime

from fastapi.security import OAuth2PasswordBearer

from app.users.models import User
from passlib.hash import bcrypt
from fastapi import HTTPException

from jose import JWTError, jwt
from app.core.config import JWT_SECRET, JWT_ALGORITHM
from app.users.schemas import UserOut


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def authenticate_user(email_or_phone: str, password: str):
    # Определяем, является ли введенная строка email или phone
    is_email = "@" in email_or_phone

    # Выполняем запрос к базе данных
    if is_email:
        user = await User.get(email=email_or_phone)
    else:
        user = await User.get(phone=email_or_phone)

    if user and user.verify_password(password):
        return user
    raise HTTPException(status_code=401, detail="Неверные учетные данные")


def compare_passwords(db_pass_hash, received_pass):
    received_pass_hash = bcrypt.hash(received_pass)
    return received_pass_hash == db_pass_hash


async def generate_tokens(email_or_phone, password):
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

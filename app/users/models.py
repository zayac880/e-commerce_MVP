from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    """
        Represents a user in the application.

        Attributes:
        - `id` (int): The unique identifier for the user.
        - `full_name` (str): The full name of the user.
        - `email` (str): The email address of the user (must be unique).
        - `phone` (str): The phone number of the user (must be unique).
        - `password_hash` (str): The hashed password of the user.

        Methods:
        - `verify_password(password: str) -> bool`:
        Verify if the provided password matches the stored hashed password.
        - `set_password(password: str) -> None`:
         Set the user's password by hashing the provided password.
        - `__str__() -> str`:
        Return a string representation of the user (returns the full name).
        """
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=14, unique=True)
    password_hash = fields.CharField(max_length=128)

    def verify_password(self, password):
        """
        Verify if the provided password matches the stored hashed password
        Parameters:
        - `password` (str): The password to be verified
        Returns:
        - True if the passwords match, False otherwise.
        """
        return bcrypt.verify(password, self.password_hash)

    def set_password(self, password):
        """
        Set the user's password by hashing the provided password.

        Parameters:
        - `password` (str): The password to be hashed.
        """
        self.password_hash = bcrypt.hash(password)

    def __str__(self):
        """
        Return a string representation of the user (returns the full name).

        Returns:
        - The full name of the user as a string.
        """
        return self.full_name

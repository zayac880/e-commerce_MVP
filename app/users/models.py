from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=14, unique=True)
    password_hash = fields.CharField(max_length=128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def __str__(self):
        return self.full_name

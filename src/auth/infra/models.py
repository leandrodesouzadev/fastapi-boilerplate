from tortoise import fields, models

from main.infra import models


class UserModel(models.UUIDTimeStampedModel):
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)

    def __str__(self):
        return self.email

    class Meta:
        table = "users"

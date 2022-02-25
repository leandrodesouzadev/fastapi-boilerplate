import uuid
from typing import TypeVar, Type
from tortoise import models, fields

from main.domain.entity import Entity


EntityType = TypeVar("EntityType", bound=Entity)


class UUIDTimeStampedModel(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self):
        return "{} ({})".format(self.__class__.__name__, self.id)

    def to_entity(self, EntityClass: Type[EntityType]) -> EntityType:
        attrs = {f: getattr(self, f) for f in self._meta.fields}
        return EntityClass(**attrs)

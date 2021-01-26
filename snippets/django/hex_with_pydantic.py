import uuid

from django.db import models
from pydantic import BaseModel, UUID4


class EntityORM(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    stuff = models.CharField(max_length=10)


class DomainEntity(BaseModel):
    id: UUID4
    stuff: str

    class Config:
        orm_mode = True


def test_stuff():
    m = EntityORM(stuff='123')
    print(m)
    domain = DomainEntity.from_orm(m)

    print('dd', domain)

    m2 = EntityORM(**domain.dict())
    print(m2)

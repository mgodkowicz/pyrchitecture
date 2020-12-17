
class Modelicho(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    stuff = models.CharField(max_length=10)


class DomainModelicho(BaseModel):
    id: UUID4
    stuff: str

    class Config:
        orm_mode = True


def test_stuff():
    m = Modelicho(stuff='123')
    print(m)
    domain = DomainModelicho.from_orm(m)

    print('dd', domain)

    m2 = Modelicho(**domain.dict())
    print(m2)

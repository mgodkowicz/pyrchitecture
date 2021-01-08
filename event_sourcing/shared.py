from pydantic import BaseModel


class Money(BaseModel):
    amount: float
    currency: str

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency == self.currency:
                return Money(amount=self.amount + other.amount, currency=self.currency)
            else:
                raise ValueError("no no ")
        raise ValueError("no no ")

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency == self.currency:
                return Money(amount=self.amount - other.amount, currency=self.currency)
            else:
                raise ValueError("no no ")
        raise ValueError("no no ")


class OrderItem(BaseModel):
    sku: str
    line_total: Money

    class Config:
        arbitrary_types_allowed = True

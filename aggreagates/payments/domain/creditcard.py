import datetime
from collections import UserList
from dataclasses import dataclass
from decimal import Decimal


# Value object
from uuid import uuid4

from pydantic import UUID4

from aggreagates.common.result import Result, success, failure


@dataclass
class Currency:
    name: str


@dataclass
class Money:
    amount: Decimal
    currency: str

    def __gt__(self, other: "Money"):
        if isinstance(other, Money):
            return self.amount > other.amount
        return False

    def decrease(self, amount):
        self.amount -= amount

    def increase(self, amount):
        self.amount += amount


@dataclass
class CreditCard:
    id: UUID4
    balance: Money

    def withdraw(self, withdraw_amount: Money) -> Result:
        if self._not_enough_money(withdraw_amount):
            return failure("No money!")

        self.balance.decrease(withdraw_amount)

        return success()

    def repay(self, repay_amount: Money) -> None:
        self.balance.increase(repay_amount)

    def _not_enough_money(self, withdraw_amount: Money) -> bool:
        return withdraw_amount > self.balance


# domain service
def transfer_money(from_account: CreditCard, to_account: CreditCard, amount: Money):
    if not from_account.balance > amount:
        return failure("no money")

    if from_account.balance.currency != amount.currency:
        return failure("different currencies")

    if to_account.balance.currency != amount.currency:
        return failure("different currencies")

    return success()


# group?


@dataclass
class Attendee:
    id: UUID4 = uuid4()


class Attendees(UserList):

    def attendee_in_group(self, attendee: Attendee):
        return attendee in self.data


@dataclass
class MeetingGroup:
    attendees: Attendees
    max_attendees_amount = 10

    def add_attendee(self, attendee: Attendee):
        if self.max_size_excited():
            return failure("Max sized excited")

        if attendee in self.attendees:
            return failure("Already in group")

        self.attendees.append(attendee)
        return success()

    def max_size_excited(self):
        return len(self.attendees.data) > self.max_attendees_amount


class Meeting:
    start_date_time: datetime
    finish_date_time: datetime
    attendees: list  # [Attendee]

import datetime
from collections import UserList
from dataclasses import dataclass
from decimal import Decimal


# Value object
from uuid import uuid4

from pydantic import UUID4

from aggreagates.common import success, failure


@dataclass
class Currency:
    name: str


@dataclass
class Money:
    amount: Decimal
    currency: Currency

    def __gt__(self, other: "Money"):
        if isinstance(other, Money):
            return self.amount > other.amount
        return False

    def decrease(self, amount):
        self.amount -= amount


# Entity / Aggregate?
@dataclass
class Account:
    name: str
    balance: Money

    def pay(self, amount: Money):
        if self.balance > amount:
            self.balance.decrease(amount)
            return failure("No money!")

        print('Money left: ', self.balance)
        return success()


# domain service
def transfer_money(from_account: Account, to_account: Account, amount: Money):
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

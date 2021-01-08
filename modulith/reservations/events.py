from django.dispatch import Signal

from common.domain_event import DomainEvent


class IntegersAdded(DomainEvent):
    num_one: int
    num_sec: int


integers_added = Signal()

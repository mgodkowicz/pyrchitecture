from common.domain_event import DomainEvent


class IntegersAdded(DomainEvent):
    num_one: int
    num_sec: int

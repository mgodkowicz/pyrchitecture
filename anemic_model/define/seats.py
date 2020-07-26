from dataclasses import dataclass


@dataclass
class MaxNoOfSeats:
    number: int

    def __post_init__(self):
        if self.number < 1:
            raise ValueError("MaxNoOfSeats can not be smaller than 1")

    def __int__(self):
        return self.number


# mix_in have a side effect
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


class Paint:
    def __init__(self, volume, red, yellow, blue):
        self.blue: int = blue
        self.yellow: int = yellow
        self.red: int = red
        self.volume: float  = volume

    def mix_in(self, paint: "Paint"):
        volume = self.volume + paint.volume
        # Logic


def test_paint():
    yellow = Paint(100.0, 0, 50, 0)
    blue = Paint(100.0, 0, 50, 0)

    yellow.mix_in(blue)

    # To test this you have to dig into implementation
    assert 200 == yellow.volume
    assert 25 == yellow.red
    assert 25 == yellow.yellow
    assert 0 == yellow.blue


@dataclass(frozen=True)
class PigmentColor:
    blue: int
    yellow: int
    red: int

    def mixed_with(self, other: "PigmentColor", ratio: float) -> "PigmentColor":
        # complex logic
        return PigmentColor()


class PaintV2:
    def __init__(self, volume: float, pigment_color: PigmentColor):
        self.volume = volume
        self.pigment_color = pigment_color

    def mix_in(self, other: "PaintV2"):
        volume = self.volume + other.volume
        ratio = other.volume / volume
        pigment_color = self.pigment_color.mixed_with(other.pigment_color, ratio)


class PaintBase(ABC):
    @property
    @abstractmethod
    def volume(self) -> float:
        pass

    @property
    @abstractmethod
    def color(self) -> PigmentColor:
        pass


class StockPaint(PaintBase):
    def __init__(self, volume: float, pigment_color: PigmentColor):
        self._volume = volume
        self.pigment_color = pigment_color

    @property
    def volume(self) -> float:
        return self._volume

    @property
    def color(self) -> PigmentColor:
        return self.pigment_color


class MixedPaint(PaintBase):
    def __init__(self):
        self.stock_constituents: List[StockPaint] = []

    @property
    def volume(self) -> float:
        return sum(paint.volume for paint in self.stock_constituents)

    @property
    def color(self) -> PigmentColor:
        # uses PigmentColor mixed_with() to compute mix of constituents's colors, and
        # returns resulting value
        if not self.stock_constituents:
            raise TypeError('no paints')

        new_color = self.stock_constituents[0]
        for paint in self.stock_constituents[1:]:
            new_color = new_color.mixed_with(paint.color, 1)

        return new_color

    def mix_in(self, paint: StockPaint):
        self.stock_constituents.append(paint)


def test_mixing_volume():
    yellow = PigmentColor(0, 50, 0)
    blue = PigmentColor(0, 50, 0)

    paint1 = StockPaint(1, yellow)
    paint2 = StockPaint(1.5, blue)
    mix = MixedPaint()

    mix.mix_in(paint1)
    mix.mix_in(paint2)

    assert mix.volume == 2.5

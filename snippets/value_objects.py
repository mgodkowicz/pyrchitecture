@dataclass(frozen=True)
class DateRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start >= self.end:
            raise ValueError("Can not end before starting.")

    def __str__(self) -> str:
        return f"DateRange({self.start} - {self.end})"

    def __add__(self, other: timedelta) -> "DateRange":
        if isinstance(other, timedelta):
            return DateRange(self.start + other, self.end + other)

        raise TypeError()

    def hour_later(self) -> "DateRange":
        return self + timedelta(hours=1)

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    def overlaps(self, date_range: "DateRange") -> bool:
        return (self.start <= date_range.end
            and self.end >= date_range.start)

    def starts_before(self, date_range: "DateRange") -> bool:
        return self.start < date_range.start

    def range(self, step: timedelta) -> Iterator[datetime]:
        current_datetime = self.start
        while current_datetime <= self.end:
            yield current_datetime
            current_datetime = current_datetime + step


class Appointment(models.Model):
    _start = models.DateTimeField(null=True) (1)
    _end = models.DateTimeField(null=True)

    objects = CustomManager()

    @property
    def date_range(self) -> DateRange: (2)
        return DateRange(self._start, self._end)

    @date_range.setter
    def date_range(self, value: DateRange) -> None: (3)
        self._start = value.start
        self._end = value.end

    @classmethod
    def new_in_date_range(cls, date_range: DateRange): (4)
        return cls(_start=date_range.start, _end=date_range.end)


class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def in_range(self, date_range: DateRange):
        return self.get_queryset().filter(
            _start__gt=date_range.start,
            _end__lt=date_range.end
         )

class CustomQuerySet(models.QuerySet):

    def filter(self, *args, **kwargs):
        date_range = kwargs.get("date_range")

        if date_range and isinstance(date_range, DateRange):
            kwargs["_start"] = date_range.start
            kwargs["_end"] = date_range.end

        return super().filter(*args, **kwargs)
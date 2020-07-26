from dataclasses import dataclass
from functools import partial
from typing import Union, Type, Any


@dataclass
class Success:
    value: Any = None


@dataclass
class Failure:
    value: Any


class Result:
    def __init__(
        self, result_class: Union[Type["Success"], Type["Failure"]], *args: Any
    ) -> None:
        self.result_instance = result_class(*args)

    def is_success(self) -> bool:
        return isinstance(self.result_instance, Success)

    @property
    def value(self) -> Any:
        return self.result_instance.value


success = partial(Result, Success)
failure = partial(Result, Failure)

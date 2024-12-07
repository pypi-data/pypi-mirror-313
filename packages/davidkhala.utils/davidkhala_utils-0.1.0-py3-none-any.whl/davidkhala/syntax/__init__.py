import re
from enum import Enum
from typing import Callable


class Package:
    def __init__(self, name: str):
        assert re.match('^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', name, re.IGNORECASE)


class NameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


def for_each(content: [], on_each: Callable[[int, str], None]):
    for index, value in enumerate(content):
        on_each(index, value)

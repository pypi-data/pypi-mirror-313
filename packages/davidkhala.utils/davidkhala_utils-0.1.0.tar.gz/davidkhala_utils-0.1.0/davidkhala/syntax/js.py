from functools import reduce
from typing import Callable


class Array(list):
    def map(self, func: Callable):
        return Array(map(func, self))

    def reduce(self, func: Callable, initial=None):
        if initial is None:
            return reduce(func, self)
        return reduce(func, self, initial)
    def filter(self, func: Callable):
        return Array(filter(func, self))
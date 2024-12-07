import json


def JSONReadable(data):
    return json.dumps(data, indent=4, sort_keys=True)


from abc import ABC, abstractmethod


class Serializable(ABC):

    @abstractmethod
    def as_dict(self) -> dict:
        pass


from sqlparse import split, format


class SQL:
    def __init__(self, sql: str):
        self.sql = sql

    def split(self) -> list[str]:
        return split(format(self.sql, strip_comments=True))

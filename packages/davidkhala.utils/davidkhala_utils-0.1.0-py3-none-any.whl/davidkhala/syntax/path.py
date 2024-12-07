import os
from pathlib import Path


def resolve(*path_tokens):
    return str(Path(os.path.join(*path_tokens)))


def homedir():
    return os.path.expanduser('~')


HOME = homedir()


def dirname(file):
    return os.path.dirname(file)


def home_resolve(*path_tokens):
    return resolve(HOME, *path_tokens)


def delete(_path):
    Path(_path).unlink(True)

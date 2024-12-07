from davidkhala.syntax.format import Serializable, JSONReadable


def read(path: str) -> str:
    with open(path, encoding="utf-8") as file:
        return file.read()


def write(path: str, data):
    with open(path, mode='w') as file:
        return file.write(data)


def write_json(data, name=None):
    if not name:
        name = data.__str__()
    if isinstance(data, Serializable):
        data = data.as_dict()
    write(f"{name}.json", JSONReadable(data))


def append(path: str, data):
    with open(path, mode='a') as file:
        return file.write(data)



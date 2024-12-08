import orjson


class Orjson:
    @staticmethod
    def load(path: str) -> dict | list:
        with open(path, "rb") as f:
            return orjson.loads(f.read())

    @staticmethod
    def dump(path: str, data: dict | list, utf8: bool = True):
        with open(path, "wb") as f:
            f.write(orjson.dumps(data, option=orjson.OPT_UTF8 if utf8 else 0))

    @staticmethod
    def dumps(data: dict | list, utf8: bool = True) -> bytes:
        return orjson.dumps(data, option=orjson.OPT_UTF8 if utf8 else 0)

    loads = orjson.loads

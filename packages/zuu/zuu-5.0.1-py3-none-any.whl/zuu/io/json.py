try:
    import json5 as json
except ImportError:
    import json

import os


class Json:
    @staticmethod
    def load(path: str) -> dict | list:
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def dump(path: str, data: dict | list, utf8: bool = True):
        with open(path, "w") as f:
            json.dump(data, f, ensure_ascii=utf8)

    @staticmethod
    def update(path: str, data: dict | list, utf8: bool = True):
        with open(path, "r") as f:
            old = json.load(f)

        old.update(data)

        with open(path, "w") as f:
            json.dump(old, f, ensure_ascii=utf8)

    @staticmethod
    def append(path: str, data: dict | list, utf8: bool = True):
        with open(path, "r") as f:
            old = json.load(f)

        if isinstance(old, list):
            old.extend(data)
        else:
            old.update(data)

        with open(path, "w") as f:
            json.dump(old, f, ensure_ascii=utf8)

    @staticmethod
    def touch(path: str, default: dict | list = {}):
        if not os.path.exists(path):
            Json.dump(path, default)

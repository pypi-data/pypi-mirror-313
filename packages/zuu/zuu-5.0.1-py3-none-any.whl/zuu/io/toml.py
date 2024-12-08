import toml


class Toml:
    @staticmethod
    def load(path: str) -> dict:
        with open(path, "r") as f:
            return toml.load(f)

    @staticmethod
    def dump(path: str, data: dict):
        with open(path, "w") as f:
            toml.dump(data, f)

    @staticmethod
    def dumps(data: dict) -> str:
        return toml.dumps(data)

    loads = toml.loads

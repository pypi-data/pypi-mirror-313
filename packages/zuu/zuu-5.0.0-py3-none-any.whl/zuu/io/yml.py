import yaml


class Yaml:
    @staticmethod
    def load(path: str) -> dict | list:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    @staticmethod
    def dump(path: str, data: dict | list):
        with open(path, "w") as f:
            yaml.dump(data, f)

    @staticmethod
    def dumps(data: dict | list) -> str:
        return yaml.dump(data)

    loads = yaml.safe_load

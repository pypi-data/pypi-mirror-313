

class Env:
    @staticmethod
    def load(path: str) -> dict:
        with open(path, "r") as f:
            return dict(line.split("=") for line in f if line.strip() and not line.startswith("#"))

    @staticmethod
    def dump(path: str, data: dict):
        with open(path, "w") as f:
            for key, value in data.items():
                f.write(f"{key}={value}\n")

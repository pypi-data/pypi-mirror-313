import pickle


class Pickle:
    @staticmethod
    def load(path: str) -> dict:
        with open(path, "rb") as f:
            return pickle.load(f)

    @staticmethod
    def dump(path: str, data: dict):
        with open(path, "wb") as f:
            pickle.dump(data, f)

    loads = pickle.loads
    dumps = pickle.dumps

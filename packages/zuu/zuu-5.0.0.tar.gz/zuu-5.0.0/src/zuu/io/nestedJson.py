import json


class NestedJson:
    @staticmethod
    def _flatten(data: dict, parent_key: str = "", sep: str = ".") -> dict:
        """
        Flattens a nested dictionary into a single-level dictionary.

        Args:
            data (dict): The nested dictionary to be flattened.
            parent_key (str, optional): The parent key of the current dictionary. Defaults to ''.
            sep (str, optional): The separator used to join the parent key and the current key. Defaults to '.'.

        Returns:
            dict: The flattened dictionary.

        Example:
            >>> data = {'a': {'b': 1, 'c': {'d': 2}}}
            >>> flatten_nested_dict(data)
            {'a.b': 1, 'a.c.d': 2}
        """
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(NestedJson._flatten(value, new_key, sep).items())
            else:
                items.append((new_key, value))
            return dict(items)

    @staticmethod
    def _unflatten(data: dict, sep: str = ".") -> dict:
        """
        Unflattens a single-level dictionary into a nested dictionary.
        """
        result = {}
        for key, value in data.items():
            keys = key.split(sep)
            d = result
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = value
        return result

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "r") as f:
            json_data = json.load(f)
        return NestedJson._unflatten(json_data)

    @staticmethod
    def dump(path: str, data: dict):
        with open(path, "w") as f:
            json.dump(NestedJson._flatten(data), f)

    flatten = _flatten
    unflatten = _unflatten

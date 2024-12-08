import typing


def load(path: str, no_nested_parse: bool = False, objonly: bool = False, **kwargs):
    extension = path.split(".")[-1]
    if extension == "json":
        try:
            from zuu.io.orjson import Orjson

            data = Orjson.load(path)
        except Exception:
            from zuu.io.json import Json

            data = Json.load(path)

        if no_nested_parse:
            return data

        if any("." in k for k in data):
            from zuu.io.nestedJson import NestedJson

            return NestedJson.load(path)

        return data

    elif extension == "yml" or extension == "yaml":
        from zuu.io.yml import Yaml

        return Yaml.load(path)

    elif extension == "toml":
        from zuu.io.toml import Toml

        return Toml.load(path)

    elif extension == "xml":
        from zuu.io.xml import Xml

        return Xml.load(path)

    elif extension == "pickle":
        from zuu.io.pickle import Pickle

        return Pickle.load(path)

    elif extension == "env":
        from zuu.io.env import Env

        return Env.load(path)

    # other:
    elif extension == "csv":
        import csv

        with open(path, "r") as f:
            return list(csv.reader(f))

    elif extension == "tsv":
        import csv

        with open(path, "r") as f:
            return list(csv.reader(f, delimiter="\t"))

    if not objonly:
        with open(path, "rb") as f:
            data = f.read()
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError:
            return data

    raise ValueError(f"Unsupported file extension: {extension}")

def _get_json():
    try:
        from zuu.io.orjson import Orjson
        return Orjson
    except Exception:
        from zuu.io.json import Json
        return Json

def dump(
    path: str,
    data: dict | list | str | bytes,
    dict_parse: typing.Literal["json", "toml", "yaml", "xml", "nestedjson"] = None,
    **kwargs,
):
    extension = path.split(".")[-1]
    if extension == "json" or dict_parse == "json":
        return _get_json().dump(path, data, **kwargs)

    elif extension == "yml" or extension == "yaml" or dict_parse == "yaml":
        from zuu.io.yml import Yaml

        return Yaml.dump(path, data, **kwargs)

    elif extension == "toml" or dict_parse == "toml":
        from zuu.io.toml import Toml

        return Toml.dump(path, data, **kwargs)

    elif extension == "xml" or dict_parse == "xml":
        from zuu.io.xml import Xml

        return Xml.dump(path, data, **kwargs)

    elif extension == "pickle":
        from zuu.io.pickle import Pickle

        return Pickle.dump(path, data, **kwargs)

    elif extension == "env":
        from zuu.io.env import Env

        return Env.dump(path, data, **kwargs)

    elif isinstance(data, dict) and dict_parse == "nestedjson":
        from zuu.io.nestedJson import NestedJson
        return NestedJson.dump(path, data, **kwargs)

    elif isinstance(data, dict | list):
        return _get_json().dump(path, data, **kwargs)

    elif isinstance(data, str):
        with open(path, "w") as f:
            f.write(data)

    elif isinstance(data, bytes):
        with open(path, "wb") as f:
            f.write(data)

    else:
        raise ValueError(f"Unsupported file extension: {extension}")

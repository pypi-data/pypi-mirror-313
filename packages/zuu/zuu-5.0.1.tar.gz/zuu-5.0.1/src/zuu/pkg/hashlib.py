import hashlib
import os

__all__ = ["sha256"]


def sha256(string: str) -> str:
    hasher = hashlib.sha256()
    if not os.path.exists(string):
        return hasher(string).hexdigest()

    with open(string, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            chunk = chunk.replace(b"\r\n", b"\n")
            hasher.update(chunk)
    return hasher.hexdigest()

from hashlib import md5
import os
import typing
from ..pkg.hashlib import sha256
from ..io import load as read


class FileProperty:
    """
    Represents a file property that can be monitored for changes, with support for various file metadata checks such as size, modification date, SHA-256 hash, and MD5 hash.

    The `FileProperty` class provides a way to track changes to a file and optionally execute callbacks when changes are detected. It supports several built-in file property checks, as well as the ability to provide custom load and save methods.

    The class initializes with a file path, a list of properties to watch (e.g. "size", "mdate", "sha256", "md5"), and optional callback functions. The `__get__` method is used to retrieve the file content, automatically updating the content if any of the watched properties have changed.
    """

    _content: dict = {}
    _meta: dict = {}

    def __init__(
        self,
        filepath: str,
        watcher: typing.Union[str, typing.List[str], typing.Callable] = [
            "size",
            "mdate",
        ],
        callbacks: typing.List[typing.Callable] = [],
        loadMethod: typing.Callable = None,
        saveMethod: typing.Callable = None,
    ):
        self.customWatcher = None
        self.filepath = filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} does not exist")
        self.filepath = os.path.abspath(filepath)

        self.watcher = watcher
        if isinstance(watcher, str):
            self.watcher = [watcher]
        elif isinstance(watcher, typing.Callable):
            self.customWatcher = watcher

        self.customLoad = loadMethod
        self.customSave = saveMethod
        self.callbacks = callbacks

        self._meta[filepath] = {}

    def _contentChanged(self):
        if self.customWatcher is not None:
            return self.customWatcher(self.filepath)

        for w in self.watcher:
            match w:
                case "size":
                    res = self._check_size()
                case "mdate":
                    res = self._check_mdate()
                case "hash" | "sha256":
                    res = self._check_sha256()
                case "md5":
                    res = self._check_md5()

            if res:
                return True

        return False

    def _check_size(self):
        meta: dict = self._meta[self.filepath]
        newsize = os.path.getsize(self.filepath)
        if "size" not in meta:
            meta["size"] = newsize
            return True

        if meta["size"] != newsize:
            meta["size"] = newsize
            return True

        return False

    def _check_mdate(self):
        meta: dict = self._meta[self.filepath]
        newmdate = os.path.getmtime(self.filepath)
        if "mdate" not in meta:
            meta["mdate"] = newmdate
            return True

        if meta["mdate"] != newmdate:
            meta["mdate"] = newmdate
            return True

        return False

    def _check_sha256(self):
        meta: dict = self._meta[self.filepath]
        newsha256 = sha256(self.filepath)
        if "sha256" not in meta:
            meta["sha256"] = newsha256
            return True

        if meta["sha256"] != newsha256:
            meta["sha256"] = newsha256
            return True

        return False

    def _check_md5(self):
        meta: dict = self._meta[self.filepath]
        newmd5 = md5(self.filepath)
        if "md5" not in meta:
            meta["md5"] = newmd5
            return True

        if meta["md5"] != newmd5:
            meta["md5"] = newmd5
            return True

        return False

    def __get__(self, instance, owner):
        self.filepath = (
            self.filepath(instance)
            if isinstance(self.filepath, property)
            else self.filepath
        )

        if self.filepath not in self._content or self._contentChanged():
            self._content[self.filepath] = (
                read(self.filepath)
                if self.customLoad is None
                else self.customLoad(self.filepath)
            )

        for callback in self.callbacks:
            callback(self.filepath, self._content[self.filepath])

        return self._content[self.filepath]

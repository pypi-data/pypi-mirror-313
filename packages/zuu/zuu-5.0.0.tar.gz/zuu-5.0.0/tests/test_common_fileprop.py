import os
import tempfile
import time
import pytest
from zuu.common.fileProp import FileProperty

class TestFileProperty:

    @pytest.fixture
    def temp_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"Test content")
        yield tmp.name
        os.unlink(tmp.name)

    def test_file_property_initialization(self, temp_file):
        fp = FileProperty(temp_file)
        assert fp.filepath == os.path.abspath(temp_file)
        assert fp.watcher == ["size", "mdate"]

    def test_file_property_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            FileProperty("nonexistent_file.txt")

    def test_file_property_content_changed_size(self, temp_file):
        fp = FileProperty(temp_file, watcher="size")
        initial_content = fp.__get__(None, None)
        
        with open(temp_file, 'a') as f:
            f.write("Additional content")
        
        new_content = fp.__get__(None, None)
        assert new_content != initial_content

    def test_file_property_content_changed_mdate(self, temp_file):
        fp = FileProperty(temp_file, watcher="mdate")
        initial_content = fp.__get__(None, None)
        
        time.sleep(1)  # Ensure modification time changes
        os.utime(temp_file, None)
        
        new_content = fp.__get__(None, None)
        assert new_content == initial_content  # Content should be the same, but mdate changed

    def test_file_property_custom_load_method(self, temp_file):
        def custom_load(filepath):
            return "Custom loaded content"

        fp = FileProperty(temp_file, loadMethod=custom_load)
        content = fp.__get__(None, None)
        assert content == "Custom loaded content"

    def test_file_property_callbacks(self, temp_file):
        callback_called = False
        def test_callback(filepath, content):
            nonlocal callback_called
            callback_called = True

        fp = FileProperty(temp_file, callbacks=[test_callback])
        fp.__get__(None, None)
        assert callback_called

    def test_file_property_multiple_watchers(self, temp_file):
        fp = FileProperty(temp_file, watcher=["size", "mdate", "sha256", "md5"])
        initial_content = fp.__get__(None, None)
        
        with open(temp_file, 'a') as f:
            f.write("Additional content")
        
        new_content = fp.__get__(None, None)
        assert new_content != initial_content

    def test_file_property_custom_watcher(self, temp_file):
        def custom_watcher(filepath):
            return True  # Always indicate change

        fp = FileProperty(temp_file, watcher=custom_watcher)
        initial_content = fp.__get__(None, None)
        new_content = fp.__get__(None, None)
        assert new_content == initial_content  # Content should be the same, but watcher always returns True


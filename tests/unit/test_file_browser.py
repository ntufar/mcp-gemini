import pytest
import os
import datetime
from src.services.file_browser import FileBrowser
import base64

# Mock root directory for testing
@pytest.fixture
def mock_root_dir(tmp_path):
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").write_text("content2")
    (tmp_path / "binary.bin").write_bytes(b'\xff\xfe')
    return tmp_path

@pytest.fixture
def file_browser_instance(mock_root_dir):
    return FileBrowser(root_dir=str(mock_root_dir))

def test_list_directory(file_browser_instance, mock_root_dir):
    result = file_browser_instance.list_directory(".")
    assert len(result["files"]) == 2  # file1.txt, binary.bin
    assert len(result["directories"]) == 1 # subdir
    
    file_names = [f["name"] for f in result["files"]]
    assert "file1.txt" in file_names
    assert "binary.bin" in file_names

    dir_names = [d["name"] for d in result["directories"]]
    assert "subdir" in dir_names

def test_list_subdirectory(file_browser_instance, mock_root_dir):
    result = file_browser_instance.list_directory("subdir")
    assert len(result["files"]) == 1
    assert result["files"][0]["name"] == "file2.txt"

def test_list_non_existent_directory(file_browser_instance):
    with pytest.raises(FileNotFoundError):
        file_browser_instance.list_directory("non_existent_dir")

def test_read_file(file_browser_instance, mock_root_dir):
    content = file_browser_instance.read_file("file1.txt")
    assert content == "content1"

def test_read_non_existent_file(file_browser_instance):
    with pytest.raises(FileNotFoundError):
        file_browser_instance.read_file("non_existent_file.txt")

def test_read_file_size_limit(file_browser_instance, mock_root_dir):
    # Create a file larger than 10MB
    large_file_path = mock_root_dir / "large_file.txt"
    large_file_path.write_bytes(b'a' * (10 * 1024 * 1024 + 1))
    with pytest.raises(ValueError, match="File size exceeds the 10MB limit"):
        file_browser_instance.read_file("large_file.txt")

def test_read_binary_file(file_browser_instance, mock_root_dir):
    content = file_browser_instance.read_file("binary.bin")
    # Base64 encoded content of b'\x00\x01\x02\x03' is AAECAw==
    assert content == base64.b64encode(b'\xff\xfe').decode("utf-8")

def test_resolve_path_sandboxing(file_browser_instance, mock_root_dir):
    # Attempt to access outside root_dir using ..
    with pytest.raises(ValueError, match="Attempted to access path outside root directory"):
        file_browser_instance._resolve_path("../outside_dir")

    # Attempt to access outside root_dir using absolute path
    with pytest.raises(ValueError, match="Attempted to access path outside root directory"):
        file_browser_instance._resolve_path("/etc/passwd")

    # Valid path within root_dir
    resolved_path = file_browser_instance._resolve_path("file1.txt")
    assert resolved_path == str(mock_root_dir / "file1.txt")

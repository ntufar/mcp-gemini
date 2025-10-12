
import pytest
from httpx import Client
import os
import tempfile
import shutil

def test_search_in_directory(client: Client, server_root_dir):
    """
    Test searching for a pattern in a directory.
    """
    test_dir = os.path.join(server_root_dir, "test_search_dir")
    os.makedirs(test_dir, exist_ok=True)

    try:
        # Create some test files
        with open(os.path.join(test_dir, "file1.txt"), "w") as f:
            f.write("hello world\n")
            f.write("another line\n")
        with open(os.path.join(test_dir, "file2.txt"), "w") as f:
            f.write("hello again\n")
        
        # a subdirectory with a file
        os.makedirs(os.path.join(test_dir, "subdir"))
        with open(os.path.join(test_dir, "subdir", "file3.txt"), "w") as f:
            f.write("hello from subdir\n")

        response = client.post("/", json={"method": "fs.search", "params": {"path": "test_search_dir", "pattern": "hello"}, "id": 1, "jsonrpc": "2.0"})

        assert response.status_code == 200
        response_json = response.json()
        assert "result" in response_json
        results = response_json["result"]
        
        assert len(results) == 3
        
        expected_results = [
            {"file_path": os.path.join("test_search_dir", "file1.txt"), "line_number": 1, "line": "hello world"},
            {"file_path": os.path.join("test_search_dir", "file2.txt"), "line_number": 1, "line": "hello again"},
            {"file_path": os.path.join("test_search_dir", "subdir", "file3.txt"), "line_number": 1, "line": "hello from subdir"},
        ]

        # Normalize paths for comparison
        for r in results:
            r["file_path"] = r["file_path"].replace("\\", "/")
        for e in expected_results:
            e["file_path"] = e["file_path"].replace("\\", "/")

        assert all(expected in results for expected in expected_results)
    finally:
        shutil.rmtree(test_dir)

def test_search_pattern_not_found(client: Client, server_root_dir):
    """
    Test searching for a pattern that doesn't exist.
    """
    test_dir = os.path.join(server_root_dir, "test_search_no_pattern_dir")
    os.makedirs(test_dir, exist_ok=True)
    try:
        with open(os.path.join(test_dir, "file1.txt"), "w") as f:
            f.write("hello world\n")

        response = client.post("/", json={"method": "fs.search", "params": {"path": "test_search_no_pattern_dir", "pattern": "goodbye"}, "id": 1, "jsonrpc": "2.0"})

        assert response.status_code == 200
        response_json = response.json()
        assert "result" in response_json
        assert response_json["result"] == []
    finally:
        shutil.rmtree(test_dir)

def test_search_in_nonexistent_directory(client: Client):
    """
    Test searching in a directory that does not exist.
    """
    response = client.post("/", json={"method": "fs.search", "params": {"path": "../", "pattern": "hello"}, "id": 1, "jsonrpc": "2.0"})

    assert response.status_code == 200
    response_json = response.json()
    assert "error" in response_json
    assert response_json["error"]["code"] == -32000
    assert "attempted to access path outside root directory" in response_json["error"]["message"].lower()

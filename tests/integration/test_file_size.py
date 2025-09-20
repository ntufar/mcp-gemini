import pytest
import os

def test_file_size_limit(client, server_root_dir):
    # Create a file larger than 10MB
    large_file_path = os.path.join(server_root_dir, "large_file.txt")
    with open(large_file_path, "wb") as f:
        f.write(b'a' * (10 * 1024 * 1024 + 1))

    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.readFile",
            "params": {"path": "large_file.txt"},
            "id": 1
        }
    )
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "File size exceeds the 10MB limit" in result["detail"]


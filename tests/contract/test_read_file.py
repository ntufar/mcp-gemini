import pytest
import os

def test_read_file_contract(client, server_root_dir):
    # Create a dummy file for testing in the server's root directory
    test_file_path = os.path.join(server_root_dir, "test_read_file.txt")
    with open(test_file_path, "w") as f:
        f.write("Hello, world!")

    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.readFile",
            "params": {"path": "test_read_file.txt"},
            "id": 2
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "jsonrpc" in result
    assert result["jsonrpc"] == "2.0"
    assert "result" in result
    assert result["result"] == "Hello, world!"
    assert "id" in result
    assert result["id"] == 2

    # Clean up the dummy file
    os.remove(test_file_path)


import pytest
import os
from unittest.mock import patch

def test_invalid_json_structure(client):
    # FastAPI handles invalid JSON before it reaches the rpc_endpoint
    # This test verifies FastAPI's default error response for invalid JSON
    response = client.post(
        "/",
        content="this is not json",
        headers={
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 422 # Unprocessable Entity for invalid JSON
    assert "detail" in response.json()

def test_missing_method_in_request(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "params": {"path": "."},
            "id": 1
        }
    )
    assert response.status_code == 200 # JSON-RPC errors return 200 OK
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32601
    assert "Method not found" in result["error"]["message"]

def test_missing_id_in_request(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.listDirectory",
            "params": {"path": "."}
        }
    )
    assert response.status_code == 200 # JSON-RPC errors return 200 OK
    result = response.json()
    assert "error" in result # ID is null in error response if missing in request
    assert result["id"] is None

def test_permission_denied_list_directory(client, server_root_dir):
    # Create a directory that we will make unreadable
    unreadable_dir = os.path.join(server_root_dir, "unreadable_dir")
    os.makedirs(unreadable_dir)
    os.chmod(unreadable_dir, 0o000) # Make directory unreadable

    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.listDirectory",
            "params": {"path": "unreadable_dir"},
            "id": 1
        }
    )
    os.chmod(unreadable_dir, 0o755) # Restore permissions for cleanup
    os.rmdir(unreadable_dir)

    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32000 # Generic server error
    assert "Permission denied to list directory" in result["error"]["data"]

def test_permission_denied_read_file(client, server_root_dir):
    # Create a file that we will make unreadable
    unreadable_file = os.path.join(server_root_dir, "unreadable_file.txt")
    with open(unreadable_file, "w") as f:
        f.write("secret content")
    os.chmod(unreadable_file, 0o000) # Make file unreadable

    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.readFile",
            "params": {"path": "unreadable_file.txt"},
            "id": 1
        }
    )
    os.chmod(unreadable_file, 0o644) # Restore permissions for cleanup
    os.remove(unreadable_file)

    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32000 # Generic server error
    assert "Permission denied to read file" in result["error"]["data"]

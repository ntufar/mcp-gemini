import pytest

def test_error_handling_non_existent_path(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.listDirectory",
            "params": {"path": "non_existent_dir"},
            "id": 1
        }
    )
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Directory not found" in result["detail"]


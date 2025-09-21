import pytest

def test_sandboxing(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.listDirectory",
            "params": {"path": "../"},
            "id": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32000 # Generic server error for ValueError
    assert "Attempted to access path outside root directory" in result["error"]["data"]


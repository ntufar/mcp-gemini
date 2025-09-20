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
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Attempted to access path outside root directory" in result["detail"]


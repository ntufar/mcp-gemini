import pytest

def test_list_directory_contract(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.listDirectory",
            "params": {"path": "."},
            "id": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "jsonrpc" in result
    assert result["jsonrpc"] == "2.0"
    assert "result" in result
    assert "id" in result
    assert result["id"] == 1
    assert "files" in result["result"]
    assert "directories" in result["result"]


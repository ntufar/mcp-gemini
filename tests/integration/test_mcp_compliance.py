import pytest

def test_mcp_compliance_invalid_jsonrpc_version(client):
    response = client.post(
        "/",
        json={
            "method": "fs.listDirectory",
            "params": {"path": "."},
            "id": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32600 # Invalid Request
    assert "Request does not comply with MCP specification" in result["error"]["data"]

def test_mcp_compliance_method_not_found(client):
    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "nonExistentMethod",
            "params": {},
            "id": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "error" in result
    assert result["error"]["code"] == -32601 # Method not found
    assert "Method not found" in result["error"]["data"]


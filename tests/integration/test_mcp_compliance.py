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
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "Request does not comply with MCP specification" in result["detail"]

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
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Method not found" in result["detail"]


import pytest
import os
import base64

def test_binary_file_handling(client, server_root_dir):
    binary_content = b'\x00\x01\x02\x03\xff\xfe'
    binary_file_path = os.path.join(server_root_dir, "test_binary.bin")
    with open(binary_file_path, "wb") as f:
        f.write(binary_content)

    response = client.post(
        "/",
        json={
            "jsonrpc": "2.0",
            "method": "fs.readFile",
            "params": {"path": "test_binary.bin"},
            "id": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "result" in result
    assert result["result"] == base64.b64encode(binary_content).decode("utf-8")


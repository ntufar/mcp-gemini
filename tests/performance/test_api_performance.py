import pytest
import os

@pytest.fixture
def large_file(server_root_dir):
    # Create a large file for read performance testing within the server's root directory
    file_path = os.path.join(server_root_dir, "large_test_file.txt")
    content = "a" * (5 * 1024 * 1024)  # 5MB file
    with open(file_path, "w") as f:
        f.write(content)
    return file_path

def test_list_directory_performance(benchmark, client):
    # Benchmark the fs.listDirectory method
    @benchmark
    def run_list_directory():
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
        assert "result" in response.json()

def test_read_file_performance(benchmark, client, large_file, server_root_dir):
    # Benchmark the fs.readFile method with a large file
    relative_path = os.path.relpath(large_file, server_root_dir)
    @benchmark
    def run_read_file():
        response = client.post(
            "/",
            json={
                "jsonrpc": "2.0",
                "method": "fs.readFile",
                "params": {"path": relative_path},
                "id": 1
            }
        )
        assert response.status_code == 200
        assert "result" in response.json()

import pytest
import os

@pytest.fixture
def large_file(tmp_path):
    # Create a large file for read performance testing
    file_path = tmp_path / "large_test_file.txt"
    content = "a" * (5 * 1024 * 1024)  # 5MB file
    file_path.write_text(content)
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

def test_read_file_performance(benchmark, client, large_file):
    # Benchmark the fs.readFile method with a large file
    @benchmark
    def run_read_file():
        response = client.post(
            "/",
            json={
                "jsonrpc": "2.0",
                "method": "fs.readFile",
                "params": {"path": os.path.basename(large_file)},
                "id": 1
            }
        )
        assert response.status_code == 200
        assert "result" in response.json()


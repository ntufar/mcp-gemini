import pytest
import uvicorn
import threading
import httpx
import os
import time

import sys

def run_server(root_dir):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    os.environ["MCP_SERVER_ROOT_DIR"] = str(root_dir)
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, log_level="info")

@pytest.fixture(scope="session")
def live_server_url(tmp_path_factory):
    # Create a temporary directory for the server's root during testing
    test_root_dir = tmp_path_factory.mktemp("mcp_server_root")

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(test_root_dir,))
    server_thread.daemon = True  # Daemonize thread to stop with main program
    server_thread.start()

    # Wait for the server to start (you might need a more robust check)
    time.sleep(2) 

    yield "http://127.0.0.1:8000"

    # Teardown: In a real scenario, you'd want to gracefully shut down the server thread.
    # For daemon threads, exiting the main program will terminate them.

@pytest.fixture(scope="session")
def client(live_server_url):
    with httpx.Client(base_url=live_server_url) as client:
        yield client

@pytest.fixture
def server_root_dir():
    # This fixture provides the actual root directory the server is using
    return os.environ.get("MCP_SERVER_ROOT_DIR")

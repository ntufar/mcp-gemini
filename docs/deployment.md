# Deployment Guide for MCP Server

This guide provides instructions on how to deploy the MCP Server.

## 1. Running with Uvicorn

The simplest way to run the MCP Server is using `uvicorn`.

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)

### Steps

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server:**
    Navigate to the project root directory and execute:
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8000
    ```
    This will start the server on `http://0.0.0.0:8000`. You can adjust the host and port as needed.

3.  **Configure Root Directory (Optional):**
    By default, the server's root directory for file system access is the current working directory where `uvicorn` is run. To specify a different root directory, set the `MCP_SERVER_ROOT_DIR` environment variable:
    ```bash
    MCP_SERVER_ROOT_DIR=/path/to/your/data uvicorn src.main:app --host 0.0.0.0 --port 8000
    ```

## 2. Running with Docker (Recommended for Production)

Using Docker provides a consistent and isolated environment for running the MCP Server.

### Prerequisites

- Docker installed and running on your system.

### Steps

1.  **Build the Docker Image:**
    Navigate to the project root directory (where `Dockerfile` is located) and build the image:
    ```bash
    docker build -t mcp-server .
    ```

2.  **Run the Docker Container:**
    You can run the container and map the server's port to a port on your host machine. You also need to mount the desired root directory for file system access into the container.
    ```bash
    docker run -d -p 8000:8000 -v /path/to/your/data:/app/data -e MCP_SERVER_ROOT_DIR=/app/data mcp-server
    ```
    - `-d`: Runs the container in detached mode.
    - `-p 8000:8000`: Maps port 8000 of the container to port 8000 of your host.
    - `-v /path/to/your/data:/app/data`: Mounts your host machine's `/path/to/your/data` directory into the container at `/app/data`. This is the directory the MCP Server will be able to access.
    - `-e MCP_SERVER_ROOT_DIR=/app/data`: Sets the `MCP_SERVER_ROOT_DIR` environment variable inside the container to `/app/data`, making it the sandboxed root for the server.

## 3. Systemd Service (for Linux Servers)

For production deployments on Linux, you can configure a `systemd` service to manage the MCP Server.

### Steps

1.  **Create a Service File:**
    Create a file named `mcp-server.service` in `/etc/systemd/system/` with content similar to this:
    ```ini
    [Unit]
    Description=MCP Server
    After=network.target

    [Service]
    User=your_user
    Group=your_group
    WorkingDirectory=/path/to/your/mcp-server-directory
    Environment="MCP_SERVER_ROOT_DIR=/path/to/your/data"
    ExecStart=/usr/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
    - Replace `your_user`, `your_group`, `/path/to/your/mcp-server-directory`, and `/path/to/your/data` with your actual values.

2.  **Reload Systemd and Start the Service:**
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl start mcp-server
    sudo systemctl enable mcp-server # To start on boot
    ```

3.  **Check Service Status:**
    ```bash
    sudo systemctl status mcp-server
    ```

# MCP Server Configuration Options

This document outlines the configurable options for the MCP Server.

## Environment Variables

### `MCP_SERVER_ROOT_DIR`

- **Description**: Specifies the absolute path to the root directory that the MCP Server will use for all file system operations (e.g., `fs.listDirectory`, `fs.readFile`). This acts as a sandboxing mechanism, preventing the server from accessing files outside this designated directory.
- **Default Value**: If not set, the server defaults to the current working directory from where the `uvicorn` command is executed.
- **Example Usage**:
    ```bash
    MCP_SERVER_ROOT_DIR=/var/mcp_data uvicorn src.main:app --host 0.0.0.0 --port 8000
    ```

## Future Configuration Options (Planned)

- **`MCP_SERVER_PORT`**: To configure the port the server listens on (currently hardcoded to 8000 or configured via `uvicorn` command-line arguments).
- **`MCP_FILE_SIZE_LIMIT_MB`**: To configure the maximum file size (in megabytes) that `fs.readFile` can process (currently hardcoded to 10MB).
- **`MCP_LOG_LEVEL`**: To configure the logging verbosity (e.g., `INFO`, `DEBUG`, `WARNING`).

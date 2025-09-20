# MCP Server

**MCP Server** is a lightweight, secure server that empowers Large Language Models (LLMs) to browse and interact with local file systems. It provides a simple API for listing directories and reading files, enabling LLMs to access local data and perform tasks that require file system access.

## Features

- **Secure by Design**: MCP Server is built with security as a top priority. It uses a sandboxed environment to prevent any unauthorized access to files or directories outside of a specified root directory.
- **Simple API**: A straightforward API with two main endpoints for listing directories and reading files.
- **Observability**: Detailed logging of all requests and responses for easy monitoring and debugging.
- **Extensible**: The modular architecture allows for easy extension with new commands and functionalities.

## Getting Started

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ntufar/mcp-gemini.git
    cd mcp-gemini
    ```
2.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

To run the MCP Server, navigate to the project root directory and execute:

```bash
uvicorn src.main:app --reload
```

The server will start on `http://127.0.0.1:8000` by default. You can then send JSON-RPC 2.0 requests to `http://127.0.0.1:8000/`.

### Python Client Example

For a practical demonstration of how to interact with the MCP Server's API using Python, refer to the `mcp_client_example.py` script in the `examples/` directory.

[View Python Client Example](examples/mcp_client_example.py)

## API

### List Directory

The `fs.listDirectory` method allows an LLM to list the contents of a specified directory.

- **Method**: `fs.listDirectory`
- **Request**:
  ```json
  {
    "jsonrpc": "2.0",
    "method": "fs.listDirectory",
    "params": {
      "path": "/path/to/directory"
    },
    "id": 1
  }
  ```
- **Response**:
  ```json
  {
    "jsonrpc": "2.0",
    "result": {
      "files": [
        {
          "name": "file.txt",
          "path": "/path/to/file.txt",
          "size": 1024,
          "modified_date": "2025-09-20T10:00:00Z"
        }
      ],
      "directories": [
        {
          "name": "subdir",
          "path": "/path/to/subdir"
        }
      ]
    },
    "id": 1
  }
  ```

### Read File

The `fs.readFile` method allows an LLM to read the contents of a specified file.

- **Method**: `fs.readFile`
- **Request**:
  ```json
  {
    "jsonrpc": "2.0",
    "method": "fs.readFile",
    "params": {
      "path": "/path/to/file.txt"
    },
    "id": 2
  }
  ```
- **Response**: The content of the file will be returned as a string in the `result` field.
  ```json
  {
    "jsonrpc": "2.0",
    "result": "This is the content of the file.",
    "id": 2
  }
  ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.

## Gemini AI Integration

Learn how to integrate the MCP Server with Gemini AI models to enable them to browse local directories and read files. This guide provides exact instructions and code examples for defining the MCP Server's functionalities as tools for Gemini.

[Read the Gemini AI Integration Guide](docs/gemini_integration.md)

### Python Client Example for Gemini Integration

For a runnable Python example demonstrating how to integrate and use the MCP Server with Gemini AI, refer to the `gemini_mcp_integration.py` script in the `examples/` directory.

[View Gemini Integration Example](examples/gemini_mcp_integration.py)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

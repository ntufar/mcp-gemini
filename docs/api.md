# MCP Server API Documentation

This document describes the JSON-RPC 2.0 API for the MCP Server, which allows Large Language Models (LLMs) to interact with the local file system.

## Base Endpoint

All requests are `POST` requests to the root endpoint (`/`). The request body must be a JSON-RPC 2.0 compliant object.

## Methods

### `fs.listDirectory`

Lists the contents (files and subdirectories) of a specified directory.

- **Description**: This method provides a secure way to enumerate the contents of a directory within the server's designated root directory. It returns metadata for files and directories, including names, paths, sizes, and modification dates for files.
- **Parameters**:
  - `path` (string, optional): The path to the directory to list, relative to the server's root directory. Defaults to `.` (the root directory itself).
- **Request Example**:
  ```json
  {
    "jsonrpc": "2.0",
    "method": "fs.listDirectory",
    "params": {
      "path": "/my/data"
    },
    "id": 1
  }
  ```
- **Response Example**:
  ```json
  {
    "jsonrpc": "2.0",
    "result": {
      "files": [
        {
          "name": "document.txt",
          "path": "/my/data/document.txt",
          "size": 12345,
          "modified_date": "2025-09-20T10:30:00Z"
        }
      ],
      "directories": [
        {
          "name": "reports",
          "path": "/my/data/reports"
        }
      ]
    },
    "id": 1
  }
  ```
- **Error Handling**:
  - `FileNotFoundError` (code: 404): If the specified `path` does not exist or is not a directory.
  - `ValueError` (code: 400): If the `path` attempts to access outside the sandboxed root directory.

### `fs.readFile`

Reads the content of a specified file.

- **Description**: This method provides a secure way to read the content of a file within the server's designated root directory. It handles both text and binary files, returning text content directly or base64-encoded content for binary files.
- **Parameters**:
  - `path` (string, required): The path to the file to read, relative to the server's root directory.
- **Request Example**:
  ```json
  {
    "jsonrpc": "2.0",
    "method": "fs.readFile",
    "params": {
      "path": "/my/data/document.txt"
    },
    "id": 2
  }
  ```
- **Response Example (Text File)**:
  ```json
  {
    "jsonrpc": "2.0",
    "result": "This is the content of the document.txt file.",
    "id": 2
  }
  ```
- **Response Example (Binary File)**:
  ```json
  {
    "jsonrpc": "2.0",
    "result": "SGVsbG8gV29ybGQh", // Base64 encoded content of "Hello World!"
    "id": 2
  }
  ```
- **Error Handling**:
  - `FileNotFoundError` (code: 404): If the specified `path` does not exist or is not a file.
  - `ValueError` (code: 400): If the `path` attempts to access outside the sandboxed root directory, or if the file size exceeds the configured limit (e.g., 10MB).

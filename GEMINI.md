# Gemini Code Assistant Context

This document provides context for the Gemini Code Assistant to understand and effectively assist with the **MCP Server** project.

## Project Overview

The **MCP Server** is a lightweight, secure server built with Python and FastAPI. Its primary purpose is to provide a secure and controlled way for Large Language Models (LLMs) to interact with a local file system. It exposes a JSON-RPC 2.0 API over HTTP, allowing LLMs to perform two main operations:

*   `fs.listDirectory`: List the contents of a specified directory.
*   `fs.readFile`: Read the contents of a specified file.

The server is designed with security in mind, sandboxing file access to a configurable root directory to prevent unauthorized access to the host system.

### Key Technologies

*   **Backend:** Python, FastAPI
*   **Server:** Uvicorn
*   **API:** JSON-RPC 2.0 over HTTP
*   **Testing:** pytest, pytest-benchmark

### Architecture

The application is structured as follows:

*   `src/main.py`: The main FastAPI application entry point. It handles incoming JSON-RPC requests, routes them to the appropriate service, and manages error handling.
*   `src/services/file_browser.py`: Contains the `FileBrowser` class, which implements the core file system logic (`list_directory` and `read_file`). It includes security checks to prevent directory traversal and other file-based vulnerabilities.
*   `src/services/mcp_compliance.py`: A service to check for JSON-RPC 2.0 compliance.
*   `src/utils/`: Contains utility modules for logging and security.
*   `tests/`: Contains unit, integration, and performance tests for the project.

## Building and Running

### Prerequisites

*   Python 3.9+
*   `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ntufar/mcp-gemini.git
    cd mcp-gemini
    ```
2.  **Install dependencies:**
    ```bash
    pip3 install -r requirements.txt
    ```

### Running the Server

To run the MCP Server for development with live reloading:

```bash
uvicorn src.main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

### Running Tests

To run the test suite:

```bash
pytest
```

## Development Conventions

*   **Code Style:** The project follows the PEP 8 style guide. The `.flake8` file is used for linting.
*   **API:** The API is defined using the JSON-RPC 2.0 specification.
*   **Security:** All file system access is sandboxed to the `ROOT_DIR` defined in `src/main.py`. The `is_path_safe` function in `src/utils/security.py` is used to prevent directory traversal attacks.
*   **Configuration:** The root directory for file access can be configured via the `MCP_SERVER_ROOT_DIR` environment variable.
*   **Logging:** The application uses Python's built-in `logging` module.

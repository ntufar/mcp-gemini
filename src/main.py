from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from src.services.file_browser import FileBrowser, PermissionDeniedError
from src.services.mcp_compliance import MCPCompliance
from src.utils.logger import get_logger
import os

app = FastAPI()
logger = get_logger(__name__)

# TODO: Make root_dir configurable (e.g., via environment variable or command line argument)
ROOT_DIR = os.getenv("MCP_SERVER_ROOT_DIR", os.getcwd())
file_browser = FileBrowser(root_dir=ROOT_DIR)
mcp_compliance = MCPCompliance()

def create_jsonrpc_error(request_id, code: int, message: str, data: any = None):
    error_response = {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": request_id
    }
    if data is not None:
        error_response["error"]["data"] = data
    return JSONResponse(status_code=status.HTTP_200_OK, content=error_response)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed", extra={"endpoint": "/"})
    return {"message": "MCP Server is running. Root directory: " + ROOT_DIR}

@app.post("/")
async def rpc_endpoint(request: dict):
    logger.info("Incoming RPC request", extra={"request_body": request})

    request_id = request.get("id") # Get ID early for error responses

    if not mcp_compliance.check_compliance(request):
        logger.warning("MCP compliance check failed", extra={"request_body": request})
        return create_jsonrpc_error(request_id, -32600, "Invalid Request", "Request does not comply with MCP specification")

    jsonrpc_version = request.get("jsonrpc")
    method = request.get("method")
    params = request.get("params", {})
    

    if jsonrpc_version != "2.0":
        logger.warning("Invalid JSON-RPC version", extra={"jsonrpc_version": jsonrpc_version})
        return create_jsonrpc_error(request_id, -32600, "Invalid Request", "Invalid JSON-RPC version")

    if method is None:
        logger.warning("Method not found in request", extra={"request_body": request})
        return create_jsonrpc_error(request_id, -32601, "Method not found", "'method' field is missing")

    try:
        if method == "fs.listDirectory":
            path = params.get("path", ".")
            result = file_browser.list_directory(path)
            response = {"jsonrpc": "2.0", "result": result, "id": request_id}
            logger.info("fs.listDirectory successful", extra={"path": path, "response": response})
            return response
        elif method == "fs.readFile":
            path = params.get("path")
            if path is None:
                return create_jsonrpc_error(request_id, -32602, "Invalid params", "Missing 'path' parameter for fs.readFile")
            content = file_browser.read_file(path)
            response = {"jsonrpc": "2.0", "result": content, "id": request_id}
            logger.info("fs.readFile successful", extra={"path": path, "response_length": len(content)}) # Log length for potentially large content
            return response
        else:
            logger.warning("Method not found", extra={"method": method})
            return create_jsonrpc_error(request_id, -32601, "Method not found", f"Method not found: {method}")
    except FileNotFoundError as e:
        logger.error("File not found error", extra={"error": str(e), "method": method, "path": params.get("path")})
        return create_jsonrpc_error(request_id, -32000, "Server error", str(e)) # Using a generic server error code for now
    except PermissionDeniedError as e:
        logger.error("Permission denied error", extra={"error": str(e), "method": method, "path": params.get("path")})
        return create_jsonrpc_error(request_id, -32000, "Server error", str(e)) # Using a generic server error code for now
    except ValueError as e:
        logger.error("Value error", extra={"error": str(e), "method": method, "path": params.get("path")})
        return create_jsonrpc_error(request_id, -32000, "Server error", str(e)) # Using a generic server error code for now

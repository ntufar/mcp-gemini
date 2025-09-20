from fastapi import FastAPI, HTTPException
from src.services.file_browser import FileBrowser
from src.services.mcp_compliance import MCPCompliance
from src.utils.logger import get_logger
import os

app = FastAPI()
logger = get_logger(__name__)

# TODO: Make root_dir configurable (e.g., via environment variable or command line argument)
ROOT_DIR = os.getcwd()
file_browser = FileBrowser(root_dir=ROOT_DIR)
mcp_compliance = MCPCompliance()

@app.get("/")
async def root():
    logger.info("Root endpoint accessed", extra={"endpoint": "/"})
    return {"message": "MCP Server is running. Root directory: " + ROOT_DIR}

@app.post("/")
async def rpc_endpoint(request: dict):
    logger.info("Incoming RPC request", extra={"request_body": request})

    if not mcp_compliance.check_compliance(request):
        logger.warning("MCP compliance check failed", extra={"request_body": request})
        raise HTTPException(status_code=400, detail="Request does not comply with MCP specification")

    jsonrpc_version = request.get("jsonrpc")
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")

    if jsonrpc_version != "2.0":
        logger.warning("Invalid JSON-RPC version", extra={"jsonrpc_version": jsonrpc_version})
        raise HTTPException(status_code=400, detail="Invalid JSON-RPC version")

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
                raise ValueError("Missing 'path' parameter for fs.readFile")
            content = file_browser.read_file(path)
            response = {"jsonrpc": "2.0", "result": content, "id": request_id}
            logger.info("fs.readFile successful", extra={"path": path, "response_length": len(content)}) # Log length for potentially large content
            return response
        else:
            logger.warning("Method not found", extra={"method": method})
            raise HTTPException(status_code=404, detail=f"Method not found: {method}")
    except FileNotFoundError as e:
        logger.error("File not found error", extra={"error": str(e), "method": method, "path": params.get("path")})
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error("Value error", extra={"error": str(e), "method": method, "path": params.get("path")})
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Unhandled exception during RPC request") # Use exception for full traceback
        raise HTTPException(status_code=500, detail=str(e))

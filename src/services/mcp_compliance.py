class MCPCompliance:
    def __init__(self):
        pass

    def check_compliance(self, request: dict) -> bool:
        # Check for required JSON-RPC 2.0 fields
        if "jsonrpc" not in request or request["jsonrpc"] != "2.0":
            return False
        # The 'method' field is checked in main.py for more granular error reporting (-32601)
        # if "method" not in request:
        #     return False
        if "id" not in request:
            # JSON-RPC 2.0 allows notifications (no id), but for this server, we require an id for responses
            # For now, we'll require an ID for simplicity in initial compliance.
            return False
        return True

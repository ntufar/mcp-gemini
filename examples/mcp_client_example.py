import requests
import json

MCP_SERVER_URL = "http://127.0.0.1:8000/"

def send_rpc_request(method: str, params: dict, request_id: int):
    """Constructs and sends a JSON-RPC 2.0 request to the MCP Server."""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending request: {json.dumps(payload, indent=2)}")
    try:
        response = requests.post(MCP_SERVER_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Server response: {e.response.text}")
        return None

def main():
    print("--- Listing contents of the root directory ---")
    list_dir_response = send_rpc_request("fs.listDirectory", {"path": "."}, 1)
    if list_dir_response:
        print("Response:")
        print(json.dumps(list_dir_response, indent=2))
        if "result" in list_dir_response:
            print(f"Found {len(list_dir_response['result']['files'])} files and {len(list_dir_response['result']['directories'])} directories.")
            # Example: Try to find README.md to read it later
            readme_found = any(f['name'] == 'README.md' for f in list_dir_response['result']['files'])
            if readme_found:
                print("README.md found in the root directory.")
            else:
                print("README.md not found in the root directory. Cannot proceed with reading example.")
                return
        else:
            print("Error in response:", list_dir_response.get("error"))

    print("\n--- Reading content of README.md ---")
    read_file_response = send_rpc_request("fs.readFile", {"path": "README.md"}, 2)
    if read_file_response:
        print("Response:")
        print(json.dumps(read_file_response, indent=2))
        if "result" in read_file_response:
            print("\n--- Content of README.md (first 500 chars) ---")
            print(read_file_response['result'][:500] + "..." if len(read_file_response['result']) > 500 else read_file_response['result'])
        else:
            print("Error in response:", read_file_response.get("error"))

if __name__ == "__main__":
    main()

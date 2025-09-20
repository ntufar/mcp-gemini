import google.generativeai as genai
import requests
import json
import os

# --- Configuration ---
# Replace with your actual MCP Server URL
MCP_SERVER_URL = "http://127.0.0.1:8000/"
# Configure Gemini API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# --- Tool Definitions for Gemini ---
fs_list_directory_tool = genai.protos.FunctionDeclaration(
    name="fs_listDirectory",
    description="Lists the contents (files and subdirectories) of a specified directory on the local file system via the MCP Server.",
    parameters=genai.protos.Schema(
        type=genai.protos.Schema.Type.OBJECT,
        properties={
            "path": genai.protos.Schema(
                type=genai.protos.Schema.Type.STRING,
                description="The path to the directory to list, relative to the server's root directory. Defaults to '.' (the server's configured root).",
            )
        },
        required=["path"], # Mark path as required, even if it has a default in your server
    ),
)

fs_read_file_tool = genai.protos.FunctionDeclaration(
    name="fs_readFile",
    description="Reads the content of a specified file on the local file system via the MCP Server.",
    parameters=genai.protos.Schema(
        type=genai.protos.Schema.Type.OBJECT,
        properties={
            "path": genai.protos.Schema(
                type=genai.protos.Schema.Type.STRING,
                description="The path to the file to read, relative to the server's root directory.",
            )
        },
        required=["path"],
    ),
)

# List of tools to provide to the Gemini model
available_tools = [fs_list_directory_tool, fs_read_file_tool]

# Initialize the Gemini model with tool configuration
# Use a model that supports function calling, e.g., 'gemini-pro'
model = genai.GenerativeModel(
    'gemini-pro',
    tools=available_tools
)

def execute_mcp_tool_call(function_call: genai.protos.FunctionCall):
    """
    Executes a tool call by making a JSON-RPC 2.0 request to the MCP Server.
    """
    method_name = function_call.name
    params = dict(function_call.args) # Convert protobuf map to dict

    # Map Gemini's tool name to MCP Server's method name
    mcp_method = None
    if method_name == "fs_listDirectory":
        mcp_method = "fs.listDirectory"
    elif method_name == "fs.readFile":
        mcp_method = "fs.readFile"
    else:
        return {"error": f"Unknown tool method: {method_name}"}

    payload = {
        "jsonrpc": "2.0",
        "method": mcp_method,
        "params": params,
        "id": 1 # Using a static ID for simplicity in this example
    }
    headers = {"Content-Type": "application/json"}

    print(f"\n--- Executing MCP Tool Call: {mcp_method} with params {params} ---")
    try:
        response = requests.post(MCP_SERVER_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        mcp_response = response.json()
        print(f"--- MCP Server Response: {json.dumps(mcp_response, indent=2)} ---")
        
        if "result" in mcp_response:
            return mcp_response["result"]
        elif "error" in mcp_response:
            return {"error": mcp_response["error"]}
        else:
            return {"error": "Invalid MCP Server response format"}
    except requests.exceptions.RequestException as e:
        error_message = f"Request to MCP Server failed: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f"\nServer response: {e.response.text}"
        print(f"--- Error executing MCP Tool Call: {error_message} ---")
        return {"error": error_message}

# --- Main Interaction Loop ---
def chat_with_gemini_using_mcp_server():
    chat = model.start_chat()

    while True:
        user_message = input("\nUser: ")
        if user_message.lower() == "exit":
            break

        # Send the user's message to Gemini
        response = chat.send_message(user_message)

        # Check if Gemini wants to call a tool
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            print(f"\nGemini wants to call tool: {function_call.name} with args: {function_call.args}")

            # Execute the tool call
            tool_output = execute_mcp_tool_call(function_call)

            # Send the tool's output back to Gemini
            print(f"\n--- Sending tool output back to Gemini ---")
            final_response = chat.send_message(
                genai.protos.Part(
                    function_response=genai.protos.FunctionResponse(
                        name=function_call.name,
                        response=tool_output
                    )
                )
            )
            print("\nGemini (final response):", final_response.text)
        else:
            # If no tool call, just print Gemini's response
            print("\nGemini:", response.text)

if __name__ == "__main__":
    print("MCP Server Integration with Gemini AI")
    print("Type 'exit' to end the conversation.")
    chat_with_gemini_using_mcp_server()
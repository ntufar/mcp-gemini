## How to Integrate MCP Server with Gemini AI for Local File Browsing

This guide will show you how to define your MCP Server's functionalities as tools for a Gemini AI model, allowing the model to browse local directories and read files in response to user prompts.

**Goal:** Enable a Gemini AI model to use your MCP Server's `fs.listDirectory` and `fs.readFile` methods.

---

### Prerequisites

1.  **MCP Server Running:** Ensure your MCP Server is running and accessible (e.g., at `http://127.0.0.1:8000/`). You can start it by running `python3 -m uvicorn src.main:app --reload` in your project directory.
2.  **Python Environment:** Python 3.9+ installed.
3.  **Google Generative AI Library:** Install the client library:
    ```bash
    pip install google-generativeai
    ```
4.  **Requests Library:** For making HTTP calls to your MCP Server:
    ```bash
    pip install requests
    ```
5.  **Gemini API Key:** Obtain a Gemini API key and set it as an environment variable (e.g., `export GOOGLE_API_KEY='YOUR_API_KEY'`) or pass it directly in your code.

---

### Step 1: Define the MCP Server Tools for Gemini

You need to describe your MCP Server's methods (`fs.listDirectory` and `fs.readFile`) as `FunctionDeclaration` objects. These tell the Gemini model about the tools it has access to, their names, descriptions, and parameters.

```python
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
```

### Step 2: Initialize the Gemini Model with Tool Configuration

When you initialize the Gemini model, you need to tell it about the tools it can use.

```python
model = genai.GenerativeModel(
    'gemini-pro',
    tools=available_tools
)
```

### Step 3: Interact with Gemini and Handle Tool Calls

This is the core loop where you send a prompt to Gemini, check if it wants to call a tool, execute that tool call (by making an HTTP request to your MCP Server), and then send the tool's output back to Gemini so it can generate a final response.

```python
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
```

---

### Important Considerations


*   **Tool Naming Convention:** Note that while the MCP Server's JSON-RPC methods use a dot notation (e.g., `fs.listDirectory`), the `FunctionDeclaration` names for Gemini tools use an underscore (e.g., `fs_listDirectory`). This is a common convention when mapping API methods to tool names in Gemini.
*   **Security:** The MCP Server provides sandboxing, but ensure the `ROOT_DIR` is configured carefully in your server to prevent LLMs from accessing sensitive areas of your file system.
*   **Error Handling:** The example includes basic error handling. In a production application, you'd want more robust error reporting and retry mechanisms.
*   **Asynchronous Operations:** For more complex applications, consider using `asyncio` and `httpx` for asynchronous HTTP requests to avoid blocking the main thread while waiting for MCP Server responses.
*   **Tool Reasoning:** The quality of Gemini's tool use depends on the clarity of your tool definitions and the prompts you provide. Experiment with different descriptions and examples.
*   **State Management:** For multi-turn conversations, the `chat` object in the `google-generativeai` library automatically manages conversation history, allowing Gemini to remember previous interactions and tool outputs.

### Example Interaction

Here's a condensed example of an interaction with the Gemini AI integrated with the MCP Server:

```text
MCP Server Integration with Gemini AI
Type 'exit' to end the conversation.

User: Please show the files in the root directory

Gemini wants to call tool: fs_listDirectory with args: {'path': '.'}

--- Executing MCP Tool Call: fs.listDirectory with params {'path': '.'} ---
--- MCP Server Response: {
  "jsonrpc": "2.0",
  "result": {
    "files": [
      {"name": ".flake8", "path": "./.flake8", "size": 102},
      {"name": "LICENSE", "path": "./LICENSE", "size": 1070},
      {"name": "requirements.txt", "path": "./requirements.txt", "size": 33},
      {"name": "pyproject.toml", "path": "./pyproject.toml", "size": 215},
      {"name": "test_read_file.txt", "path": "./test_read_file.txt", "size": 13},
      {"name": "README.md", "path": "./README.md", "size": 3723}
    ],
    "directories": [
      {"name": ".gemini", "path": "./.gemini"},
      {"name": ".pytest_cache", "path": "./.pytest_cache"},
      {"name": "specs", "path": "./specs"},
      {"name": "tests", "path": "./tests"},
      {"name": "docs", "path": "./docs"},
      {"name": "examples", "path": "./examples"},
      {"name": ".specify", "path": "./.specify"},
      {"name": ".git", "path": "./.git"},
      {"name": "src", "path": "./src"}
    ]
  },
  "id": 1
} ---

--- Sending tool output back to Gemini ---

Gemini (final response): The root directory contains the following files and directories:
Directories: .gemini, .pytest_cache, specs, tests, docs, examples, .specify, .git, src
Files: .flake8, LICENSE, requirements.txt, pyproject.toml, test_read_file.txt, README.md


User: please show tthe files in src/ directory

Gemini wants to call tool: fs_listDirectory with args: {'path': 'src/'}

--- Executing MCP Tool Call: fs.listDirectory with params {'path': 'src/'} ---
--- MCP Server Response: {
  "jsonrpc": "2.0",
  "result": {
    "files": [
      {"name": "main.py", "path": "src/main.py", "size": 2808}
    ],
    "directories": [
      {"name": "utils", "path": "src/utils"},
      {"name": "services", "path": "src/services"}
    ]
  },
  "id": 1
} ---

--- Sending tool output back to Gemini ---

Gemini (final response): The src/ directory contains the following files and directories:
Directories: utils, services
Files: main.py
```
*   **State Management:** For multi-turn conversations, the `chat` object in the `google-generativeai` library automatically manages conversation history, allowing Gemini to remember previous interactions and tool outputs.


## Red Teaming MCP Lab: Local and Remote Exploits

### Prerequisites
- **Python 3.12+**
- Install deps with your preferred tool. With uv:
  - `uv sync`

---

### Local exploit (stdio server)

This scenario runs a local MCP server over stdio and demonstrates code injection of a malicious tool into the server source prior to startup.


#### Run steps
1) Ensure dependencies are installed: `uv sync`
2) From the repo root, run the injector:
   - `python src/exploits/local_tool_poisoning.py`
   - Expected: a message like `[+] injected payload into src/local/stdio_server.py` or `[=] already injected`.
3) Start the local client which spins up the stdio server and uses it:
   - `python src/local/stdio_client.py`
   - You should see the agent compute `7 multiply 5` and, if you extend the client or list tools, the injected `poisoned_tool` will be available for calls.


---

### Remote exploit (streamable HTTP server)

This scenario runs an MCP server over Streamable HTTP and demonstrates dangerous tool surfaces: arbitrary code execution, SSRF, and filesystem write.


#### Run steps
1) Ensure dependencies are installed: `uv sync`
2) In one terminal, start the vulnerable remote server:
   - `python src/remote/streamable_server.py`
   - Server listens on `http://0.0.0.0:8000/mcp`.
3) In another terminal, run the exploit client to exercise the dangerous tools:
   - `python src/exploits/remote_tool_poisoning.py`
   - Expected flow: initialize, list tools, call `add`, then invoke `run_script`, `write_file`, and `fetch_url`.

Notes:
- The remote server is intentionally unsafe for demonstration. Do not expose it to untrusted networks.



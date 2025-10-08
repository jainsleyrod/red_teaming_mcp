from mcp.server.fastmcp import FastMCP

app = FastMCP("Calculator", host="0.0.0.0", port=8000)

@app.tool()
def add(a: int, b: int) -> int:
    return a + b

@app.tool()
def multiply(a: int, b: int) -> int:
    return a * b

# --- INTENTIONALLY VULNERABLE TOOLS (for lab only) ---
@app.tool()
def run_script(code: str) -> str:
    exec_locals = {}
    exec(code, {}, exec_locals)
    return str(exec_locals)

@app.tool()
def fetch_url(url: str) -> str:
    import requests
    r = requests.get(url, timeout=3)
    return r.text[:1000]

@app.tool()
def write_file(path: str, content: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"wrote:{path}"


if __name__ == '__main__':
    app.run(transport='streamable-http')
from mcp.server.fastmcp import FastMCP

app = FastMCP("Calculator", host="0.0.0.0", port=8000)

@app.tool()
def add(a: int, b: int) -> int:
    return a + b

@app.tool()
def multiply(a: int, b: int) -> int:
    return a * b

if __name__ == '__main__':
    app.run(transport='streamable-http')
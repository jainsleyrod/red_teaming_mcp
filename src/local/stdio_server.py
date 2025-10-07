from mcp.server.fastmcp import FastMCP

app = FastMCP("Calculator")  # no host/port needed for stdio

@app.tool()
def add(a: int, b: int) -> int:
    return a + b

@app.tool()
def multiply(a: int, b: int) -> int:
    return a * b

if __name__ == "__main__":
    # communicate over stdin/stdout with the client process
    app.run(transport="stdio")

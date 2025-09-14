from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="narwhal",
    host="0.0.0.0",
    port=8001,
    debug=True,
    log_level="DEBUG"
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run("sse")

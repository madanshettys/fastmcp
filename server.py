from fastmcp import FastMCP
import random
import json

# ---------------------------
# Simple Token Verifier
# ---------------------------
class SimpleVerifier:
    def __init__(self, code: str):
        self.code = code

    def verify(self, token: str):
        if token != self.code:
            raise PermissionError("Invalid access token!")

    def get_routes(self, **kwargs):
        return []

# Initialize the verifier with code "123"
verifier = SimpleVerifier("123")

# Create the FASTMCP server
mcp = FastMCP("Simple Math MCP Server", auth=verifier)

# ---------------------------
# Tools
# ---------------------------
@mcp.tool(annotations={
    "a": {"description": "The first integer to add", "example": 5},
    "b": {"description": "The second integer to add", "example": 3}
})
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool(annotations={
    "a": {"description": "The integer to subtract from", "example": 10},
    "b": {"description": "The integer to subtract", "example": 4}
})
def sub(a: int, b: int) -> int:
    return a - b

@mcp.tool(annotations={
    "min_val": {"description": "The minimum value (inclusive)", "example": 0},
    "max_val": {"description": "The maximum value (inclusive)", "example": 100}
})
def random_number(min_val: int = 0, max_val: int = 100) -> int:
    return random.randint(min_val, max_val)

# ---------------------------
# Resources
# ---------------------------
@mcp.resource("info://server")
def server_info() -> str:
    info = {
        "name": "Simple Math MCP Server",
        "version": "1.0.0",
        "description": "A simple MCP server providing basic math operations."
    }
    return json.dumps(info)

# ---------------------------
# Run server
# ---------------------------
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

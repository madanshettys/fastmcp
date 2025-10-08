from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
import random
import json
import os

from dotenv import load_dotenv, find_dotenv

# Load .env from this folder or any parent
load_dotenv(find_dotenv())

AUTH_SECRET="73ec69c46402ac9a82c0448d4bb40ce0813328d3864ebac8e013e1b58a5d0363"
AUTH_ISSUER="internal-auth-service"
AUTH_AUDIENCE="mcp-internal-api"

verifier = JWTVerifier(
    public_key=AUTH_SECRET,
    issuer=AUTH_ISSUER,
    audience=AUTH_AUDIENCE,
    algorithm="HS256"
)

# Create the FASTMCP
mcp = FastMCP("Simple Math MCP Server")

@mcp.tool(annotations={
    "a": {
        "description": "The first integer to add",
        "example": 5
    },
    "b": {
        "description": "The second integer to add",
        "example": 3
    }
})
def add(a: int, b: int) -> int:
    """
    Simple addition tool.
    Add two integers and return the result.
    Args:
        a (int): First integer.
        b (int): Second integer.
        
    Returns:
         int: The sum of a and b.
    """
    return a + b

@mcp.tool(annotations={
    "a": {
        "description": "The integer to subtract from",
        "example": 10
    },
    "b": {
        "description": "The integer to subtract",
        "example": 4
    }
})
def sub(a: int, b: int) -> int:
    """
    Simple subtraction tool.
    Subtract two integers and return the result.
    Args:
        a (int): First integer.
        b (int): Second integer.
        
    Returns:
         int: The difference of a and b.
    """
    return a - b

@mcp.tool(annotations={
    "min_val": {
        "description": "The minimum value (inclusive)",
        "example": 0
    },
    "max_val": {
        "description": "The maximum value (inclusive)",
        "example": 100
    }
})
def random_number(min_val: int = 0, max_val: int = 100) -> int:
    """
    Generate a random integer between min_val and max_val.
    Args:
        min_val (int): Minimum value (inclusive).
        max_val (int): Maximum value (inclusive).
        
    Returns:
         int: A random integer between min_val and max_val.
    """
    return random.randint(min_val, max_val)

#Resource: Server info
@mcp.resource("info://server")
def server_info() -> str:
    """
    Return server information as a JSON string.
    """
    info = {
        "name": "Simple Math MCP Server",
        "version": "1.0.0",
        "description": "A simple MCP server providing basic math operations."
    }
    return json.dumps(info)

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

##to execute this file, run: 
# fastmcp run server.py --transport http --host 127.0.0.1 --port 8000
# fastmcp run <filename> --transport <transport_type> --host <host_address> --port <port_number>


#how to run mcp inspector:
#<npx @modelcontextprotocol/inspector>

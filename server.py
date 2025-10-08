from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
import random
import json
import requests
from jose import jwt
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# -------------------------------
# Okta configuration
# -------------------------------
OKTA_DOMAIN = "https://integrator-3646450.okta.com"  # e.g., https://dev-123456.okta.com
CLIENT_ID = "0oav0d9wneeO6EvF4697"              # Okta App Client ID
ISSUER = f"{OKTA_DOMAIN}/oauth2/default"

# Fetch Okta JWKS keys (public keys for JWT verification)
JWKS = requests.get(f"{ISSUER}/v1/keys").json()

class OktaJWTVerifier(JWTVerifier):
    """
    Verifies JWT tokens issued by Okta.
    """
    def verify(self, token: str):
        try:
            claims = jwt.decode(
                token,
                JWKS,
                audience=CLIENT_ID,
                issuer=ISSUER
            )
            # Map Okta's "sub" claim to MCP user identity
            return claims["sub"]
        except Exception as e:
            raise Exception(f"Invalid token: {e}")

# Initialize FastMCP with Okta JWT authentication
verifier = OktaJWTVerifier()
mcp = FastMCP("Simple Math MCP Server", auth=verifier)

# -------------------------------
# MCP Tools
# -------------------------------
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

# -------------------------------
# MCP Resource
# -------------------------------
@mcp.resource("info://server")
def server_info() -> str:
    info = {
        "name": "Simple Math MCP Server",
        "version": "1.0.0",
        "description": "A simple MCP server providing basic math operations."
    }
    return json.dumps(info)

# -------------------------------
# Run MCP server
# -------------------------------
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

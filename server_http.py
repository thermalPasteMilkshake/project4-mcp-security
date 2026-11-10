"""
Project 4 - the SAME vulnerable MCP server, exposed over HTTP so an HTTP proxy
(Burp) can see the traffic. Reuses every tool from server.py.

Run from the project4-mcp-security folder:
    python server_http.py
Serves streamable-HTTP MCP at http://127.0.0.1:8000/mcp
"""
from server import mcp

if __name__ == "__main__":
    # streamable-http transport -> Uvicorn on 127.0.0.1:8000, MCP at /mcp
    mcp.run(transport="streamable-http")

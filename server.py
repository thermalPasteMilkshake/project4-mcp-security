import os
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("techcorp-tools")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@mcp.tool()
def read_file(path: str) -> str:
    """Read and return the contents of a file by path.

    VULNERABLE: no path allow-listing, so '../../etc/passwd' style traversal
    works. Risk: High.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError as e:
        return f"error: {e}"


@mcp.tool()
def execute_command(command: str) -> str:
    try:
        out = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15,
            stdin=subprocess.DEVNULL,
        )
        return (out.stdout or "") + (out.stderr or "")
    except Exception as e:  # noqa: BLE001 - lab
        return f"error: {e}"


@mcp.tool()
def query_db(query: str) -> str:

    rows = {
        "select * from users": "1,admin,admin@techcorp\n2,jdoe,jdoe@techcorp",
        "select * from secrets": "api_key=sk-techcorp-9f3a1c7e2b",
    }
    return rows.get(query.strip().lower(), "(0 rows)")


@mcp.tool()
def list_dir(path: str = ".") -> str:
    try:
        return "\n".join(sorted(os.listdir(path)))
    except OSError as e:
        return f"error: {e}"



@mcp.resource("file://company-handbook")
def company_handbook() -> str:
    path = os.path.join(BASE_DIR, "resources", "handbook.txt")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        return f"error: {e}"

@mcp.prompt()
def support_ticket(issue: str) -> str:
    return f"Please draft a support ticket for this issue: {issue}"


if __name__ == "__main__":
    mcp.run()

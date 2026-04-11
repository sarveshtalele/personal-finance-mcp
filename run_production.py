"""
Production server runner for SSE transport.

Usage:
    python run_production.py
    python run_production.py --host 0.0.0.0 --port 9000

Environment Variables:
    MCP_HOST  — Bind host (default: 127.0.0.1)
    MCP_PORT  — Bind port (default: 8000)
"""

import os
import sys


def main():
    host = os.environ.get("MCP_HOST", "127.0.0.1")
    port = int(os.environ.get("MCP_PORT", "8000"))

    # Allow CLI overrides
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--host" and i + 1 < len(args):
            host = args[i + 1]
            i += 2
        elif args[i] == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
            i += 2
        else:
            i += 1

    from src.server import mcp

    print("Starting Personal Finance MCP Server (SSE)")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Tools: {len(mcp._tool_manager._tools)}")
    print(f"  URL:  http://{host}:{port}/sse")
    print()

    mcp.run(transport="sse", host=host, port=port)


if __name__ == "__main__":
    main()

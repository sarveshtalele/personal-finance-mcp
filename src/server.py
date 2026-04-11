"""
Personal Finance MCP Server
Based on Core Financial Principles

A stateless MCP server providing deterministic personal finance calculations
for financial planning, investment analysis, and portfolio management.

Supports: Claude Desktop, Claude Code, and any MCP-compatible client.
Transport: stdio (default), SSE (optional).
"""

from mcp.server.fastmcp import FastMCP
from .tools import tvm, debt, planning, bonds, stocks, mutual_funds, portfolio

# Initialize the MCP server
mcp = FastMCP(
    "Personal Finance Advisor",
    instructions=(
        "Deterministic personal finance calculator based on Core Financial Principles "
        "(Level 1) curriculum. Provides tools for Time Value of Money, debt management, "
        "goal planning, stock/bond valuation, mutual fund analysis, portfolio analytics, "
        "retirement planning, and comprehensive financial health assessment."
    ),
)

# Register all tool modules

tvm.register(mcp)
debt.register(mcp)
planning.register(mcp)
bonds.register(mcp)
stocks.register(mcp)
mutual_funds.register(mcp)
portfolio.register(mcp)


def main():
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

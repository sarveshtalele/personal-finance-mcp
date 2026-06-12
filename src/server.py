"""
Personal Finance MCP Server
Based on Core Financial Principles

A stateless MCP server providing deterministic personal finance calculations
for financial planning, investment analysis, and portfolio management.

Supports: Claude Desktop, Claude Code, and any MCP-compatible client.
Transport: stdio (default), SSE (optional).
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from .tools import (
    tvm,
    debt,
    planning,
    bonds,
    stocks,
    mutual_funds,
    portfolio,
    derivatives,
    india_savings,
    cashflow,
    risk_profile,
    advisor,
    marketdata,
)

# Initialize the MCP server
mcp = FastMCP(
    "Personal Finance Advisor",
    instructions=(
        "Deterministic personal finance toolkit based on the NISM Investment Adviser "
        "(Level 1) curriculum. Covers Time Value of Money, cash-flow & budgeting, debt "
        "management, Indian small-savings (PPF/SSY/NSC/KVP/SCSS/RD/FD/EPF), goal & "
        "retirement planning, stock/bond valuation, derivatives, mutual funds, portfolio "
        "analytics, risk profiling, and live market data (mutual-fund NAVs, FX, quotes).\n\n"
        "HOW TO ROUTE A USER STORY TO TOOLS:\n"
        "- The user will NOT name tools. Infer intent from their situation and pick tools "
        "by what they're trying to achieve.\n"
        "- When someone describes their finances broadly ('I'm 30, earn 1L/month, have a "
        "home loan, want to retire at 60'), START with `create_financial_plan` to get a "
        "prioritised action plan, then drill into specific calculators for detail.\n"
        "- Follow the planning order: evaluate position -> protect (emergency fund, "
        "insurance) -> reduce debt -> profile risk -> invest for goals.\n"
        "- Chain tools freely: e.g. assess_risk_profile -> suggest_asset_allocation -> "
        "calculate_sip_needed. Always show the numbers and the formula used."
    ),
    # Public HTTP connector: allow any host/origin (e.g. the Hugging Face Space
    # domain) and run stateless so it works behind a proxy / multiple workers.
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
        allowed_hosts=["*"],
        allowed_origins=["*"],
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
derivatives.register(mcp)
india_savings.register(mcp)
cashflow.register(mcp)
risk_profile.register(mcp)
advisor.register(mcp)
marketdata.register(mcp)


def main():
    """Run the MCP server with stdio transport."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

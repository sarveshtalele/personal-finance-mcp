"""
Personal Finance MCP Server

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
        "Deterministic personal finance toolkit grounded in core financial-planning "
        "principles. Covers Time Value of Money, cash-flow & budgeting, debt "
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
        "calculate_sip_needed. Always show the numbers and the formula used.\n\n"
        "GOVERNANCE — STRICTLY FOLLOW (non-negotiable):\n"
        "1. Use ONLY numbers returned by these tools. Never invent, estimate, round "
        "differently, or substitute your own figures for a tool's output.\n"
        "2. Present allocations, percentages, EMIs, corpus and SIP amounts EXACTLY as "
        "the tool returned them. If you show a split, it must match the tool verbatim.\n"
        "3. Do NOT fabricate things the tools do not return: specific fund names or "
        "tickers, expected-return ranges, CAGR assumptions, tax rates, or multi-year "
        "projection tables. If the user wants a projection, call the relevant tool "
        "(e.g. plan_retirement, calculate_sip_returns) and report ITS numbers.\n"
        "4. There is ONE source of truth for an equity/debt/gold split: "
        "suggest_asset_allocation. assess_risk_profile returns the same split. If you "
        "have both, they will agree — never blend them or present a third number.\n"
        "5. If two tool results appear to conflict, do not silently pick one. Re-run "
        "with consistent inputs and surface the discrepancy to the user.\n"
        "6. Recompute via a tool whenever inputs change; never carry an earlier answer "
        "forward as if it still applies. State which tool produced each number."
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

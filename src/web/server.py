"""
Unified HTTP server for Hugging Face (or any host).

Serves three things from one ASGI app on a single port:
  /mcp        -> the MCP server over streamable-HTTP (use this URL as a connector)
  /api/*      -> JSON endpoints for the website (tool catalog, calculators, live data)
  /           -> the exported Next.js website (static files)

Run:  python -m src.web         (PORT env var, defaults to 7860 for HF Spaces)
"""

import inspect
import os
from pathlib import Path

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from ..server import mcp
from ..tools import tvm, debt, mutual_funds, india_savings, advisor, marketdata

# --------------------------------------------------------------------------- #
# Calculator registry — maps a website calculator id to a pure function.
# Only the numeric kwargs in each request body are forwarded.
# --------------------------------------------------------------------------- #
CALCULATORS = {
    "future_value": tvm.future_value,
    "present_value": tvm.present_value,
    "future_value_annuity": tvm.future_value_annuity,
    "rule_of_72": tvm.rule_of_72,
    "inflation_impact": tvm.inflation_adjusted_amount,
    "required_monthly_savings": tvm.required_monthly_savings,
    "emi": debt.calculate_emi,
    "sip_returns": mutual_funds.sip_calculator,
    "sip_needed": mutual_funds.sip_required_for_target,
    "ppf": india_savings.ppf_maturity,
    "fixed_deposit": india_savings.fixed_deposit,
    "nsc": india_savings.nsc_maturity,
    "epf": india_savings.epf_corpus,
    "financial_plan": advisor.create_financial_plan,
}


def _category(module_name: str) -> str:
    key = module_name.rsplit(".", 1)[-1]
    return {
        "tvm": "Time Value of Money",
        "debt": "Debt & Loans",
        "cashflow": "Cash Flow & Budgeting",
        "planning": "Financial Planning",
        "bonds": "Fixed Income",
        "stocks": "Equity Valuation",
        "mutual_funds": "Mutual Funds",
        "portfolio": "Portfolio Analytics",
        "derivatives": "Derivatives",
        "india_savings": "Small Savings (India)",
        "risk_profile": "Risk Profiling",
        "advisor": "Advisor",
        "marketdata": "Live Market Data",
    }.get(key, key.title())


# --------------------------------------------------------------------------- #
# API handlers
# --------------------------------------------------------------------------- #
async def health(_: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "tools": len(mcp._tool_manager._tools)})


async def list_tools(_: Request) -> JSONResponse:
    tools = []
    for name, tool in mcp._tool_manager._tools.items():
        module = getattr(tool.fn, "__module__", "")
        desc = (tool.description or "").strip().split("\n")[0]
        tools.append({"name": name, "category": _category(module), "description": desc})
    tools.sort(key=lambda t: (t["category"], t["name"]))
    categories: dict[str, int] = {}
    for t in tools:
        categories[t["category"]] = categories.get(t["category"], 0) + 1
    return JSONResponse(
        {"count": len(tools), "categories": categories, "tools": tools}
    )


async def run_calc(request: Request) -> JSONResponse:
    body = await request.json()
    name = body.get("calculator")
    fn = CALCULATORS.get(name)
    if fn is None:
        return JSONResponse(
            {"error": f"Unknown calculator '{name}'", "available": list(CALCULATORS)},
            status_code=400,
        )
    params = body.get("params", {})
    sig = inspect.signature(fn)
    allowed = {k: v for k, v in params.items() if k in sig.parameters}
    try:
        result = fn(**allowed)
        return JSONResponse({"calculator": name, "result": result})
    except Exception as e:  # noqa: BLE001
        return JSONResponse({"error": str(e)}, status_code=400)


async def api_nav(request: Request) -> JSONResponse:
    code = request.query_params.get("code")
    if code:
        return JSONResponse(marketdata.get_mf_nav(int(code)))
    q = request.query_params.get("q", "")
    return JSONResponse(marketdata.search_mutual_funds(q))


async def api_fx(request: Request) -> JSONResponse:
    base = request.query_params.get("base", "USD")
    symbols = request.query_params.get("symbols", "INR")
    return JSONResponse(marketdata.get_fx_rate(base, symbols))


async def api_quote(request: Request) -> JSONResponse:
    symbol = request.query_params.get("symbol", "^nsei")
    return JSONResponse(marketdata.get_quote(symbol))


# --------------------------------------------------------------------------- #
# App assembly: extend the MCP streamable-HTTP app (keeps its lifespan intact)
# --------------------------------------------------------------------------- #
def build_app():
    app = mcp.streamable_http_app()  # Starlette app exposing /mcp + session lifespan

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_routes = [
        Route("/api/health", health),
        Route("/api/tools", list_tools),
        Route("/api/calc", run_calc, methods=["POST"]),
        Route("/api/nav", api_nav),
        Route("/api/fx", api_fx),
        Route("/api/quote", api_quote),
    ]
    # Insert API routes before any static catch-all.
    app.router.routes[:0] = api_routes

    # Serve the exported website if present (mounted last as catch-all).
    static_dir = Path(__file__).resolve().parents[2] / "web" / "out"
    if static_dir.is_dir():
        app.router.routes.append(
            Mount("/", app=StaticFiles(directory=str(static_dir), html=True))
        )
    return app


app = build_app()


def main():
    import uvicorn

    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()

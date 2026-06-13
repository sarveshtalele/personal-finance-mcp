"""
Unified, hardened HTTP server for Hugging Face (or any host).

Serves three things from one ASGI app on a single port:
  /mcp        -> the MCP server over streamable-HTTP (use this URL as a connector)
  /api/*      -> JSON endpoints for the website (tool catalog, calculators, live data)
  /           -> the exported Next.js website (static files)

Security: a transparent ASGI middleware adds security headers (incl. CSP) to every
response, caps request bodies, and rate-limits the JSON API. The calculator endpoint
validates and bounds all inputs (the calculators contain loops, so unbounded inputs
would be a denial-of-service vector).

Run:  python -m src.web         (PORT env var, defaults to 7860 for HF Spaces)
"""

import inspect
import math
import os
import re
import time
from collections import deque
from pathlib import Path

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from ..server import mcp
from ..tools import tvm, debt, mutual_funds, india_savings, advisor, marketdata

# --------------------------------------------------------------------------- #
# Calculator registry — maps a website calculator id to a pure function.
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

# --------------------------------------------------------------------------- #
# Security configuration
# --------------------------------------------------------------------------- #
MAX_BODY = 16 * 1024  # 16 KB — calculator payloads are tiny
RATE_LIMIT = 90  # requests ...
RATE_WINDOW = 10.0  # ... per 10 s per client IP, on /api/*
ABS_MAX = 1e13  # reject absurd numeric magnitudes

# Cap the inputs that drive loops in the calculators (DoS protection).
PARAM_CAPS = {
    "years": 120,
    "tenure_years": 120,
    "deposit_years": 120,
    "maturity_years": 130,
    "months": 2400,
    "age": 120,
    "retirement_age": 120,
    "life_expectancy": 130,
    "dependents": 50,
    "compounding_periods": 365,
}

CSP = (
    "default-src 'self'; base-uri 'self'; object-src 'none'; "
    "img-src 'self' data:; font-src 'self' data:; "
    "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; "
    "connect-src 'self'; "
    "frame-ancestors 'self' https://huggingface.co https://*.hf.space"
)
SEC_HEADERS = [
    (b"x-content-type-options", b"nosniff"),
    (b"referrer-policy", b"strict-origin-when-cross-origin"),
    (b"permissions-policy", b"geolocation=(), microphone=(), camera=()"),
    (b"strict-transport-security", b"max-age=63072000; includeSubDomains"),
    (b"cross-origin-opener-policy", b"same-origin"),
    (b"content-security-policy", CSP.encode()),
]

# Per-IP sliding-window counters. Pruned periodically so the dict cannot grow
# without bound (a memory-exhaustion vector under spoofed/rotating IPs).
_hits: dict[str, deque] = {}
_MAX_TRACKED_IPS = 20_000
_prune_counter = 0


def _prune(now: float) -> None:
    stale = [ip for ip, q in _hits.items() if not q or now - q[-1] > RATE_WINDOW]
    for ip in stale:
        _hits.pop(ip, None)
    # Hard cap as a backstop against a flood of distinct IPs in one window.
    if len(_hits) > _MAX_TRACKED_IPS:
        _hits.clear()


_SYMBOL_RE = re.compile(r"^[A-Za-z0-9.^=:-]{1,15}$")
_CCY_RE = re.compile(r"^[A-Za-z, ]{1,40}$")


def _client_ip(scope) -> str:
    for k, v in scope.get("headers", []):
        if k == b"x-forwarded-for":
            return v.decode().split(",")[0].strip()
    client = scope.get("client")
    return client[0] if client else "unknown"


async def _send_json(send, status: int, payload: bytes):
    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [(b"content-type", b"application/json")] + SEC_HEADERS,
        }
    )
    await send({"type": "http.response.body", "body": payload})


class SecurityMiddleware:
    """Transparent ASGI middleware: header injection + body cap + rate limit.

    Implemented at the ASGI layer (not BaseHTTPMiddleware) so it never buffers
    the streaming /mcp (SSE) responses.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope.get("path", "")
        if path.startswith("/api"):
            headers = dict(scope.get("headers", []))
            cl = headers.get(b"content-length")
            if cl and cl.isdigit() and int(cl) > MAX_BODY:
                return await _send_json(send, 413, b'{"error":"payload too large"}')

            global _prune_counter
            ip = _client_ip(scope)
            now = time.monotonic()
            _prune_counter += 1
            if _prune_counter % 500 == 0:
                _prune(now)
            q = _hits.setdefault(ip, deque())
            while q and now - q[0] > RATE_WINDOW:
                q.popleft()
            if len(q) >= RATE_LIMIT:
                return await _send_json(
                    send, 429, b'{"error":"rate limit exceeded, slow down"}'
                )
            q.append(now)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", [])
                message["headers"].extend(SEC_HEADERS)
            await send(message)

        await self.app(scope, receive, send_wrapper)


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


def _sanitize_params(params: dict) -> dict:
    """Validate and bound calculator inputs. Raises ValueError on bad input."""
    if not isinstance(params, dict) or len(params) > 30:
        raise ValueError("invalid parameters")
    clean = {}
    for k, v in params.items():
        if not isinstance(k, str) or len(k) > 40:
            raise ValueError("invalid parameter name")
        if isinstance(v, bool):
            clean[k] = v
        elif isinstance(v, (int, float)):
            if not math.isfinite(v):
                raise ValueError(f"'{k}' must be a finite number")
            if abs(v) > ABS_MAX:
                raise ValueError(f"'{k}' is out of range")
            cap = PARAM_CAPS.get(k)
            if cap is not None and v > cap:
                raise ValueError(f"'{k}' must be ≤ {cap}")
            clean[k] = v
        elif isinstance(v, str):
            if len(v) > 40:
                raise ValueError(f"'{k}' is too long")
            clean[k] = v
        # silently drop nulls / nested structures
    return clean


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
    return JSONResponse({"count": len(tools), "categories": categories, "tools": tools})


async def run_calc(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid JSON"}, status_code=400)

    name = body.get("calculator")
    fn = CALCULATORS.get(name)
    if fn is None:
        return JSONResponse(
            {"error": f"unknown calculator '{name}'", "available": list(CALCULATORS)},
            status_code=400,
        )
    try:
        params = _sanitize_params(body.get("params", {}))
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    sig = inspect.signature(fn)
    allowed = {k: v for k, v in params.items() if k in sig.parameters}
    try:
        return JSONResponse({"calculator": name, "result": fn(**allowed)})
    except (ValueError, ZeroDivisionError, KeyError, TypeError) as e:
        # Expected domain errors — safe, actionable message.
        return JSONResponse({"error": f"invalid inputs: {e}"}, status_code=400)
    except Exception:  # noqa: BLE001
        # Never leak internals/stack traces to the client.
        import logging

        logging.getLogger("personal-finance").exception("calc failed: %s", name)
        return JSONResponse({"error": "calculation failed"}, status_code=400)


async def api_nav(request: Request) -> JSONResponse:
    code = request.query_params.get("code")
    if code:
        if not code.isdigit() or len(code) > 9:
            return JSONResponse({"error": "invalid scheme code"}, status_code=400)
        return JSONResponse(marketdata.get_mf_nav(int(code)))
    q = (request.query_params.get("q") or "").strip()
    if not q or len(q) > 80:
        return JSONResponse({"error": "query must be 1–80 characters"}, status_code=400)
    return JSONResponse(marketdata.search_mutual_funds(q))


async def api_fx(request: Request) -> JSONResponse:
    base = request.query_params.get("base", "USD")
    symbols = request.query_params.get("symbols", "INR")
    if not _CCY_RE.match(base) or not _CCY_RE.match(symbols):
        return JSONResponse({"error": "invalid currency code"}, status_code=400)
    return JSONResponse(marketdata.get_fx_rate(base, symbols))


async def api_quote(request: Request) -> JSONResponse:
    symbol = request.query_params.get("symbol", "^NSEI")
    if not _SYMBOL_RE.match(symbol):
        return JSONResponse({"error": "invalid symbol"}, status_code=400)
    return JSONResponse(marketdata.get_quote(symbol))


# --------------------------------------------------------------------------- #
# App assembly: extend the MCP streamable-HTTP app (keeps its lifespan intact)
# --------------------------------------------------------------------------- #
def build_app():
    app = mcp.streamable_http_app()  # Starlette app exposing /mcp + session lifespan

    # Public, read-only JSON API: allow cross-origin GET/POST, no credentials.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["content-type"],
        allow_credentials=False,
        max_age=3600,
    )
    app.add_middleware(SecurityMiddleware)

    api_routes = [
        Route("/api/health", health),
        Route("/api/tools", list_tools),
        Route("/api/calc", run_calc, methods=["POST"]),
        Route("/api/nav", api_nav),
        Route("/api/fx", api_fx),
        Route("/api/quote", api_quote),
    ]
    app.router.routes[:0] = api_routes

    static_dir = Path(__file__).resolve().parents[2] / "web" / "out"
    if static_dir.is_dir():
        # Next exports the OG image without a file extension; serve it as PNG so
        # social scrapers (LinkedIn/X/PH) accept it.
        og = static_dir / "opengraph-image"
        if og.is_file():

            async def opengraph_image(_request):
                return FileResponse(str(og), media_type="image/png")

            app.router.routes.insert(0, Route("/opengraph-image", opengraph_image))

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

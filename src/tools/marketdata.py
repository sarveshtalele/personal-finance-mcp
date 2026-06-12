"""
Live Market Data (keyless public sources)

Wraps free, no-API-key endpoints so the MCP tools and the website dashboard share
one implementation:
  - Mutual-fund NAVs : api.mfapi.in (AMFI data)        -> get_mf_nav / search
  - FX rates         : api.frankfurter.app (ECB data)   -> get_fx_rate
  - Equity/index quote: stooq.com CSV                    -> get_quote

Network calls are best-effort and return {"error": ...} on failure so callers
never crash. These are the only non-deterministic tools in the server.
"""

import httpx

_TIMEOUT = httpx.Timeout(8.0)
_UA = {"User-Agent": "personal-finance-mcp/1.1 (+https://github.com/sarveshtalele)"}


def search_mutual_funds(query: str, limit: int = 10) -> dict:
    """Search AMFI mutual-fund schemes by name; returns scheme codes + names."""
    try:
        r = httpx.get(
            "https://api.mfapi.in/mf/search",
            params={"q": query}, timeout=_TIMEOUT, headers=_UA,
        )
        r.raise_for_status()
        data = r.json()[:limit]
        return {
            "query": query,
            "count": len(data),
            "schemes": [
                {"scheme_code": d["schemeCode"], "scheme_name": d["schemeName"]}
                for d in data
            ],
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"Mutual-fund search failed: {e}"}


def get_mf_nav(scheme_code: int) -> dict:
    """Latest NAV for an AMFI scheme code (use search_mutual_funds to find the code)."""
    try:
        r = httpx.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=_TIMEOUT, headers=_UA)
        r.raise_for_status()
        j = r.json()
        meta = j.get("meta", {})
        latest = (j.get("data") or [{}])[0]
        return {
            "scheme_code": scheme_code,
            "scheme_name": meta.get("scheme_name"),
            "fund_house": meta.get("fund_house"),
            "category": meta.get("scheme_category"),
            "nav": latest.get("nav"),
            "date": latest.get("date"),
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"NAV fetch failed: {e}"}


def get_fx_rate(base: str = "USD", symbols: str = "INR") -> dict:
    """Latest reference FX rates from the ECB (via Frankfurter)."""
    try:
        r = httpx.get(
            "https://api.frankfurter.dev/v1/latest",
            params={"base": base.upper(), "symbols": symbols.upper()},
            timeout=_TIMEOUT, headers=_UA, follow_redirects=True,
        )
        r.raise_for_status()
        j = r.json()
        return {"base": j.get("base"), "date": j.get("date"), "rates": j.get("rates", {})}
    except Exception as e:  # noqa: BLE001
        return {"error": f"FX fetch failed: {e}"}


def get_quote(symbol: str) -> dict:
    """Equity/index quote from Yahoo Finance. Examples: '^NSEI' (Nifty 50),
    '^BSESN' (Sensex), 'AAPL', 'RELIANCE.NS'."""
    sym = symbol.strip().upper()
    try:
        r = httpx.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}",
            params={"interval": "1d", "range": "1d"},
            timeout=_TIMEOUT, headers=_UA, follow_redirects=True,
        )
        r.raise_for_status()
        result = (r.json().get("chart", {}).get("result") or [None])[0]
        if not result:
            return {"error": f"No quote for '{symbol}'"}
        meta = result.get("meta", {})
        price = meta.get("regularMarketPrice")
        if price is None:
            return {"error": f"No price for '{symbol}'"}
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        change_pct = round((price / prev - 1) * 100, 2) if prev else None
        return {
            "symbol": meta.get("symbol", sym),
            "price": price,
            "currency": meta.get("currency"),
            "previous_close": prev,
            "change_pct": change_pct,
            "exchange": meta.get("exchangeName"),
        }
    except Exception as e:  # noqa: BLE001
        return {"error": f"Quote fetch failed: {e}"}


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="search_mutual_funds")
    def search_mutual_funds_tool(query: str, limit: int = 10) -> str:
        """Search Indian mutual-fund schemes by name (AMFI data) and get their scheme
        codes. Use when a user names a fund ('Parag Parikh Flexi Cap') and you need
        its code before fetching the live NAV."""
        return format_tool_response("Mutual Fund Search", search_mutual_funds(query, limit))

    @mcp.tool(name="get_mutual_fund_nav")
    def get_mf_nav_tool(scheme_code: int) -> str:
        """Latest live NAV for an AMFI mutual-fund scheme code. Use for 'what's the
        current NAV of fund X' (first find the code with search_mutual_funds)."""
        return format_tool_response("Live Mutual Fund NAV", get_mf_nav(scheme_code))

    @mcp.tool(name="get_fx_rate")
    def get_fx_rate_tool(base: str = "USD", symbols: str = "INR") -> str:
        """Live currency exchange rates (ECB reference, via Frankfurter). Use for
        'what's the USD/INR rate', converting amounts, or FX-impact questions.
        symbols can be comma-separated, e.g. 'INR,EUR,GBP'."""
        return format_tool_response("Live FX Rates", get_fx_rate(base, symbols))

    @mcp.tool(name="get_stock_quote")
    def get_quote_tool(symbol: str) -> str:
        """Live equity/index quote (Yahoo Finance). Use for 'current price/level of X'.
        Examples: '^NSEI' Nifty 50, '^BSESN' Sensex, 'RELIANCE.NS', 'AAPL'."""
        return format_tool_response("Live Quote", get_quote(symbol))

"""
Stock Valuation Models

Models:
  Gordon Growth (DDM): P = D1 / (r - g)
  Multi-stage DDM: P = Σ[D_t/(1+r)^t] + P_n/(1+r)^n
  P/E Valuation: Fair Price = EPS × Industry P/E
  DCF: P = Σ[FCF_t/(1+WACC)^t] + TV/(1+WACC)^n
  PEG Ratio = P/E / Earnings Growth Rate
"""


def gordon_growth_model(
    current_dividend: float, growth_rate: float, required_return: float
) -> dict:
    """
    Gordon Growth Model (Constant Growth DDM).
    P = D1 / (r - g) where D1 = D0 × (1 + g)
    """
    g = growth_rate / 100
    r = required_return / 100

    if r <= g:
        return {"error": "Required return must be greater than growth rate"}

    d1 = current_dividend * (1 + g)
    price = d1 / (r - g)
    dividend_yield = d1 / price * 100

    return {
        "intrinsic_value": round(price, 2),
        "next_year_dividend": round(d1, 2),
        "dividend_yield": round(dividend_yield, 2),
        "growth_rate": growth_rate,
        "required_return": required_return,
        "formula": f"P = D1 / (r - g) = {d1:.2f} / ({r} - {g})",
    }


def multi_stage_ddm(
    current_dividend: float,
    high_growth_rate: float,
    high_growth_years: int,
    stable_growth_rate: float,
    required_return: float,
) -> dict:
    """
    Two-stage Dividend Discount Model.
    Stage 1: High growth period with DDM
    Stage 2: Stable growth with Gordon model
    """
    r = required_return / 100
    g1 = high_growth_rate / 100
    g2 = stable_growth_rate / 100

    if r <= g2:
        return {"error": "Required return must exceed stable growth rate"}

    # Stage 1: PV of dividends during high growth
    pv_stage1 = 0
    dividend = current_dividend
    dividends = []

    for t in range(1, high_growth_years + 1):
        dividend = dividend * (1 + g1)
        pv = dividend / (1 + r) ** t
        pv_stage1 += pv
        dividends.append(
            {"year": t, "dividend": round(dividend, 2), "pv": round(pv, 2)}
        )

    # Stage 2: Terminal value using Gordon Growth
    d_stable = dividend * (1 + g2)
    terminal_value = d_stable / (r - g2)
    pv_terminal = terminal_value / (1 + r) ** high_growth_years

    intrinsic_value = pv_stage1 + pv_terminal

    return {
        "intrinsic_value": round(intrinsic_value, 2),
        "pv_high_growth_dividends": round(pv_stage1, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_terminal_value": round(pv_terminal, 2),
        "high_growth_dividends": dividends,
        "formula": "P = Σ[D_t/(1+r)^t] + [D_(n+1)/(r-g₂)] / (1+r)^n",
    }


def pe_valuation(
    eps: float,
    industry_pe: float,
    company_growth: float = 0,
    industry_growth: float = 0,
) -> dict:
    """
    P/E Relative Valuation.
    Fair Price = EPS × P/E ratio
    PEG Ratio = P/E / Growth Rate
    """
    fair_price = eps * industry_pe

    result = {
        "fair_price": round(fair_price, 2),
        "eps": eps,
        "pe_ratio": industry_pe,
        "formula": f"Fair Price = EPS × P/E = {eps} × {industry_pe}",
    }

    if company_growth > 0:
        peg = industry_pe / company_growth
        result["peg_ratio"] = round(peg, 2)
        result["peg_interpretation"] = (
            "Undervalued (PEG < 1)"
            if peg < 1
            else "Fairly valued (PEG ≈ 1)"
            if peg <= 1.5
            else "Overvalued (PEG > 1.5)"
        )

    if industry_growth > 0 and company_growth > 0:
        relative_pe = industry_pe * (company_growth / industry_growth)
        result["relative_pe_adjusted_price"] = round(eps * relative_pe, 2)

    return result


def dcf_valuation(
    free_cash_flows: list[float],
    wacc: float,
    terminal_growth: float,
    shares_outstanding: float = 1,
    net_debt: float = 0,
) -> dict:
    """
    Discounted Cash Flow Valuation.
    Enterprise Value = Σ[FCF_t/(1+WACC)^t] + TV/(1+WACC)^n
    Equity Value = Enterprise Value - Net Debt
    Fair Price = Equity Value / Shares Outstanding
    """
    r = wacc / 100
    g = terminal_growth / 100

    if r <= g:
        return {"error": "WACC must exceed terminal growth rate"}

    # PV of projected FCFs
    pv_fcfs = []
    total_pv_fcf = 0
    for t, fcf in enumerate(free_cash_flows, 1):
        pv = fcf / (1 + r) ** t
        total_pv_fcf += pv
        pv_fcfs.append({"year": t, "fcf": fcf, "pv": round(pv, 2)})

    # Terminal Value
    last_fcf = free_cash_flows[-1]
    terminal_fcf = last_fcf * (1 + g)
    terminal_value = terminal_fcf / (r - g)
    pv_terminal = terminal_value / (1 + r) ** len(free_cash_flows)

    enterprise_value = total_pv_fcf + pv_terminal
    equity_value = enterprise_value - net_debt
    fair_price = equity_value / shares_outstanding

    return {
        "enterprise_value": round(enterprise_value, 2),
        "equity_value": round(equity_value, 2),
        "fair_price_per_share": round(fair_price, 2),
        "pv_of_fcfs": round(total_pv_fcf, 2),
        "terminal_value": round(terminal_value, 2),
        "pv_of_terminal_value": round(pv_terminal, 2),
        "terminal_value_pct": round(pv_terminal / enterprise_value * 100, 2),
        "projected_fcfs": pv_fcfs,
        "formula": "EV = Σ[FCF_t/(1+WACC)^t] + [FCF_(n+1)/(WACC-g)] / (1+WACC)^n",
    }


def dividend_yield(dividend_per_share: float, market_price: float) -> dict:
    """Dividend Yield = Annual Dividend / Market Price × 100"""
    dy = (dividend_per_share / market_price) * 100

    return {
        "dividend_yield": round(dy, 2),
        "dividend_per_share": dividend_per_share,
        "market_price": market_price,
        "formula": f"DY = {dividend_per_share} / {market_price} × 100 = {dy:.2f}%",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="value_stock_ddm")
    def value_stock_ddm_tool(
        current_dividend: float,
        growth_rate: float,
        required_return: float,
    ) -> str:
        """Value a stock using Gordon Growth Model (Dividend Discount Model).
        P = D1 / (r - g). For stable, dividend-paying companies.
        required_return must be > growth_rate."""
        result = gordon_growth_model(current_dividend, growth_rate, required_return)
        return format_tool_response("Gordon Growth Model (DDM)", result)

    @mcp.tool(name="value_stock_two_stage_ddm")
    def value_stock_two_stage_ddm_tool(
        current_dividend: float,
        high_growth_rate: float,
        high_growth_years: int,
        stable_growth_rate: float,
        required_return: float,
    ) -> str:
        """Two-stage DDM for companies with initial high growth transitioning to stable growth.
        Stage 1: High growth dividends discounted. Stage 2: Gordon model terminal value."""
        result = multi_stage_ddm(
            current_dividend,
            high_growth_rate,
            high_growth_years,
            stable_growth_rate,
            required_return,
        )
        return format_tool_response("Two-Stage DDM Valuation", result)

    @mcp.tool(name="value_stock_pe")
    def value_stock_pe_tool(
        eps: float,
        industry_pe: float,
        company_growth: float = 0,
        industry_growth: float = 0,
    ) -> str:
        """Value stock using P/E ratio relative valuation.
        Fair Price = EPS × Industry P/E.
        Optionally calculates PEG ratio for growth-adjusted valuation."""
        result = pe_valuation(eps, industry_pe, company_growth, industry_growth)
        return format_tool_response("P/E Ratio Valuation", result)

    @mcp.tool(name="value_stock_dcf")
    def value_stock_dcf_tool(
        free_cash_flows_json: str,
        wacc: float,
        terminal_growth: float,
        shares_outstanding: float = 1,
        net_debt: float = 0,
    ) -> str:
        """Discounted Cash Flow (DCF) valuation.
        Input projected Free Cash Flows as JSON array: [100, 120, 140, 160, 180].
        EV = Σ[FCF/(1+WACC)^t] + Terminal Value. Equity = EV - Net Debt."""
        import json

        fcfs = json.loads(free_cash_flows_json)
        result = dcf_valuation(
            fcfs, wacc, terminal_growth, shares_outstanding, net_debt
        )
        return format_tool_response("DCF Valuation", result)

    @mcp.tool(name="calculate_dividend_yield")
    def calculate_dividend_yield_tool(
        dividend_per_share: float,
        market_price: float,
    ) -> str:
        """Calculate dividend yield = Annual Dividend / Market Price × 100."""
        result = dividend_yield(dividend_per_share, market_price)
        return format_tool_response("Dividend Yield", result)

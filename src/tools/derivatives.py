"""
Derivatives Calculations (NISM Level 1, Chapter 10: Understanding Derivatives)

Core formulas:
  Futures fair value (cost-of-carry):
      F = S × e^((r - q)×t)            -- continuous
      F = S × (1 + r - q)^t            -- discrete (annual)
  Option intrinsic value:
      Call = max(S - K, 0)
      Put  = max(K - S, 0)
  Put-Call parity:
      C - P = S - K × e^(-r×t)
  Black-Scholes (European):
      C = S×N(d1) - K×e^(-r×t)×N(d2)
      P = K×e^(-r×t)×N(-d2) - S×N(-d1)
      d1 = [ln(S/K) + (r + σ²/2)×t] / (σ×√t),  d2 = d1 - σ×√t
  Beta hedge (number of index-futures contracts):
      N = (β × Portfolio Value) / (Index Level × Lot Size)
"""

import math


def _norm_cdf(x: float) -> float:
    """Standard normal CDF via the error function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def futures_fair_value(
    spot: float,
    annual_rate: float,
    years: float,
    dividend_yield: float = 0.0,
    continuous: bool = True,
) -> dict:
    """Cost-of-carry fair value of a futures/forward contract."""
    r = annual_rate / 100
    q = dividend_yield / 100
    if continuous:
        fair = spot * math.exp((r - q) * years)
        formula = f"F = S × e^((r-q)×t) = {spot:,.2f} × e^(({r}-{q})×{years})"
    else:
        fair = spot * (1 + r - q) ** years
        formula = f"F = S × (1+r-q)^t = {spot:,.2f} × (1+{r}-{q})^{years}"
    return {
        "futures_fair_value": round(fair, 2),
        "spot_price": spot,
        "cost_of_carry": round(fair - spot, 2),
        "carry_pct": round((fair / spot - 1) * 100, 4),
        "formula": formula,
    }


def option_payoff(
    option_type: str,
    position: str,
    strike: float,
    premium: float,
    spot_at_expiry: float,
) -> dict:
    """Payoff and profit of a single option leg at expiry."""
    option_type = option_type.lower()
    position = position.lower()
    if option_type == "call":
        intrinsic = max(spot_at_expiry - strike, 0)
        breakeven = strike + premium
    else:
        intrinsic = max(strike - spot_at_expiry, 0)
        breakeven = strike - premium

    if position == "long":
        profit = intrinsic - premium
        max_loss = premium
        max_profit = "Unlimited" if option_type == "call" else round(strike - premium, 2)
    else:  # short / writer
        profit = premium - intrinsic
        max_profit = premium
        max_loss = "Unlimited" if option_type == "call" else round(strike - premium, 2)

    return {
        "option_type": option_type,
        "position": position,
        "intrinsic_value": round(intrinsic, 2),
        "premium": premium,
        "profit_loss": round(profit, 2),
        "breakeven_price": round(breakeven, 2),
        "max_profit": max_profit,
        "max_loss": max_loss,
        "formula": f"{'Call' if option_type=='call' else 'Put'} intrinsic = max("
        + (f"S-K" if option_type == "call" else "K-S")
        + ", 0)",
    }


def put_call_parity(
    spot: float,
    strike: float,
    annual_rate: float,
    years: float,
    call_price: float = None,
    put_price: float = None,
) -> dict:
    """Solve the missing option price via put-call parity: C - P = S - K·e^(-rt)."""
    r = annual_rate / 100
    pv_strike = strike * math.exp(-r * years)
    rhs = spot - pv_strike  # = C - P

    result = {
        "pv_of_strike": round(pv_strike, 2),
        "intrinsic_forward": round(rhs, 2),
        "formula": "C - P = S - K×e^(-r×t)",
    }
    if call_price is not None and put_price is None:
        result["implied_put_price"] = round(call_price - rhs, 2)
    elif put_price is not None and call_price is None:
        result["implied_call_price"] = round(put_price + rhs, 2)
    elif call_price is not None and put_price is not None:
        arb = (call_price - put_price) - rhs
        result["parity_difference"] = round(arb, 2)
        result["arbitrage_present"] = abs(arb) > 0.01
    return result


def black_scholes(
    spot: float,
    strike: float,
    annual_rate: float,
    volatility: float,
    years: float,
    option_type: str = "call",
) -> dict:
    """European option price and Greeks (delta) via Black-Scholes."""
    r = annual_rate / 100
    sigma = volatility / 100
    if years <= 0 or sigma <= 0:
        return {"error": "Time to expiry and volatility must be positive."}

    d1 = (math.log(spot / strike) + (r + sigma**2 / 2) * years) / (sigma * math.sqrt(years))
    d2 = d1 - sigma * math.sqrt(years)

    if option_type.lower() == "call":
        price = spot * _norm_cdf(d1) - strike * math.exp(-r * years) * _norm_cdf(d2)
        delta = _norm_cdf(d1)
    else:
        price = strike * math.exp(-r * years) * _norm_cdf(-d2) - spot * _norm_cdf(-d1)
        delta = _norm_cdf(d1) - 1

    return {
        "option_type": option_type.lower(),
        "option_price": round(price, 4),
        "d1": round(d1, 4),
        "d2": round(d2, 4),
        "delta": round(delta, 4),
        "spot": spot,
        "strike": strike,
        "formula": "C = S×N(d1) - K×e^(-r×t)×N(d2)",
    }


def beta_hedge(
    portfolio_value: float,
    portfolio_beta: float,
    index_level: float,
    lot_size: int,
) -> dict:
    """Number of index-futures contracts to fully hedge an equity portfolio."""
    contract_value = index_level * lot_size
    contracts = (portfolio_beta * portfolio_value) / contract_value
    return {
        "contracts_to_short": round(contracts, 2),
        "contracts_rounded": round(contracts),
        "contract_value": round(contract_value, 2),
        "portfolio_value": portfolio_value,
        "portfolio_beta": portfolio_beta,
        "note": "Short index futures to hedge a long portfolio (sell to protect downside).",
        "formula": "N = (β × Portfolio Value) / (Index Level × Lot Size)",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_futures_price")
    def calculate_futures_price_tool(
        spot_price: float,
        annual_rate: float,
        years: float,
        dividend_yield: float = 0.0,
        compounding: str = "continuous",
    ) -> str:
        """Fair value of a futures/forward contract using cost-of-carry.
        Use when a user asks 'what should the futures/forward price be', about
        carry, contango/backwardation, or arbitrage-free pricing of index/stock futures.
        F = Spot × e^((r-q)×t). Set dividend_yield for stocks/indices."""
        result = futures_fair_value(
            spot_price, annual_rate, years, dividend_yield,
            continuous=(compounding == "continuous"),
        )
        return format_tool_response("Futures Fair Value (Cost of Carry)", result)

    @mcp.tool(name="calculate_option_payoff")
    def calculate_option_payoff_tool(
        option_type: str,
        position: str,
        strike: float,
        premium: float,
        spot_at_expiry: float,
    ) -> str:
        """Payoff, profit/loss and breakeven of an option leg at expiry.
        Use for 'if I buy/sell a call/put at strike X for premium Y, what is my P&L
        if the stock ends at Z', options breakeven, max profit/loss questions.
        option_type: call|put. position: long|short."""
        result = option_payoff(option_type, position, strike, premium, spot_at_expiry)
        return format_tool_response("Option Payoff at Expiry", result)

    @mcp.tool(name="calculate_put_call_parity")
    def calculate_put_call_parity_tool(
        spot: float,
        strike: float,
        annual_rate: float,
        years: float,
        call_price: float = -1,
        put_price: float = -1,
    ) -> str:
        """Put-call parity: derive the fair call or put price, or detect arbitrage.
        Provide whichever option price you know; leave the other at -1 to solve it.
        C - P = S - K×e^(-r×t)."""
        c = None if call_price < 0 else call_price
        p = None if put_price < 0 else put_price
        result = put_call_parity(spot, strike, annual_rate, years, c, p)
        return format_tool_response("Put-Call Parity", result)

    @mcp.tool(name="calculate_black_scholes")
    def calculate_black_scholes_tool(
        spot: float,
        strike: float,
        annual_rate: float,
        volatility: float,
        years: float,
        option_type: str = "call",
    ) -> str:
        """Theoretical European option price (Black-Scholes) and delta.
        Use for 'what is a fair option premium', option valuation, implied pricing.
        volatility is annualised in percent (e.g. 20 for 20%)."""
        result = black_scholes(spot, strike, annual_rate, volatility, years, option_type)
        return format_tool_response("Black-Scholes Option Price", result)

    @mcp.tool(name="calculate_futures_hedge")
    def calculate_futures_hedge_tool(
        portfolio_value: float,
        portfolio_beta: float,
        index_level: float,
        lot_size: int,
    ) -> str:
        """Number of index-futures contracts needed to hedge an equity portfolio.
        Use for 'how do I protect/hedge my portfolio against a market fall',
        beta hedging, downside protection. N = (β × Value) / (Index × Lot Size)."""
        result = beta_hedge(portfolio_value, portfolio_beta, index_level, lot_size)
        return format_tool_response("Portfolio Beta Hedge", result)

"""
Portfolio Analytics and Modern Portfolio Theory

Core formulas:
  Expected Return: E(Rp) = Σ w_i × E(R_i)
  Portfolio Variance: σ²p = ΣΣ w_i × w_j × σ_i × σ_j × ρ_ij
  Beta: β = Cov(R_i, R_m) / Var(R_m)
  CAPM: E(R_i) = R_f + β × (E(R_m) - R_f)
  Sharpe Ratio: (R_p - R_f) / σ_p
  Treynor Ratio: (R_p - R_f) / β_p
  Jensen's Alpha: α = R_p - [R_f + β × (R_m - R_f)]
  Information Ratio: (R_p - R_b) / Tracking Error
  Sortino Ratio: (R_p - R_f) / Downside Deviation
"""

import math


def portfolio_expected_return(weights: list[float], returns: list[float]) -> dict:
    """E(Rp) = Σ w_i × E(R_i)"""
    if len(weights) != len(returns):
        return {"error": "Weights and returns must have same length"}

    portfolio_return = sum(w * r for w, r in zip(weights, returns))
    total_weight = sum(weights)

    contributions = [
        {"weight": round(w, 4), "return": r, "contribution": round(w * r, 4)}
        for w, r in zip(weights, returns)
    ]

    return {
        "portfolio_expected_return": round(portfolio_return, 4),
        "total_weight": round(total_weight, 4),
        "contributions": contributions,
        "formula": "E(Rp) = Σ w_i × E(R_i)",
    }


def portfolio_risk(
    weights: list[float],
    std_devs: list[float],
    correlations: list[list[float]],
) -> dict:
    """
    Portfolio variance and standard deviation.
    σ²p = ΣΣ w_i × w_j × σ_i × σ_j × ρ_ij
    """
    n = len(weights)
    if len(std_devs) != n or len(correlations) != n:
        return {"error": "Dimensions mismatch"}

    variance = 0
    for i in range(n):
        for j in range(n):
            variance += (
                weights[i] * weights[j] * std_devs[i] * std_devs[j] * correlations[i][j]
            )

    std_dev = math.sqrt(variance)

    # Individual contributions
    risk_contributions = []
    for i in range(n):
        marginal = 0
        for j in range(n):
            marginal += weights[j] * std_devs[i] * std_devs[j] * correlations[i][j]
        marginal *= weights[i]
        risk_contributions.append(
            {
                "asset": i + 1,
                "weight": round(weights[i], 4),
                "individual_risk": round(std_devs[i], 4),
                "risk_contribution": round(marginal, 4),
                "pct_of_total_risk": round(marginal / variance * 100, 2)
                if variance > 0
                else 0,
            }
        )

    # Diversification benefit
    weighted_avg_risk = sum(w * s for w, s in zip(weights, std_devs))
    diversification_benefit = weighted_avg_risk - std_dev

    return {
        "portfolio_variance": round(variance, 6),
        "portfolio_std_dev": round(std_dev, 4),
        "weighted_avg_risk": round(weighted_avg_risk, 4),
        "diversification_benefit": round(diversification_benefit, 4),
        "risk_contributions": risk_contributions,
        "formula": "σ²p = ΣΣ w_i × w_j × σ_i × σ_j × ρ_ij",
    }


def two_asset_portfolio(
    w1: float,
    r1: float,
    s1: float,
    r2: float,
    s2: float,
    correlation: float,
) -> dict:
    """
    Simplified two-asset portfolio analysis.
    Common case from standardized financial models.
    """
    w2 = 1 - w1
    portfolio_return = w1 * r1 + w2 * r2
    portfolio_var = (
        (w1**2) * (s1**2) + (w2**2) * (s2**2) + 2 * w1 * w2 * s1 * s2 * correlation
    )
    portfolio_std = math.sqrt(portfolio_var)

    # Minimum variance portfolio weights
    if s1**2 + s2**2 - 2 * s1 * s2 * correlation != 0:
        w1_min_var = (s2**2 - s1 * s2 * correlation) / (
            s1**2 + s2**2 - 2 * s1 * s2 * correlation
        )
    else:
        w1_min_var = 0.5
    w2_min_var = 1 - w1_min_var
    min_var_return = w1_min_var * r1 + w2_min_var * r2
    min_var_risk = math.sqrt(
        (w1_min_var**2) * (s1**2)
        + (w2_min_var**2) * (s2**2)
        + 2 * w1_min_var * w2_min_var * s1 * s2 * correlation
    )

    return {
        "portfolio_return": round(portfolio_return, 4),
        "portfolio_risk": round(portfolio_std, 4),
        "portfolio_variance": round(portfolio_var, 6),
        "asset_1": {"weight": w1, "return": r1, "risk": s1},
        "asset_2": {"weight": w2, "return": r2, "risk": s2},
        "correlation": correlation,
        "minimum_variance_portfolio": {
            "weight_asset_1": round(w1_min_var, 4),
            "weight_asset_2": round(w2_min_var, 4),
            "return": round(min_var_return, 4),
            "risk": round(min_var_risk, 4),
        },
        "formula": "σ²p = w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂",
    }


def capm(risk_free_rate: float, beta: float, market_return: float) -> dict:
    """
    Capital Asset Pricing Model.
    E(R_i) = R_f + β × (E(R_m) - R_f)
    """
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    market_risk_premium = market_return - risk_free_rate
    stock_risk_premium = beta * market_risk_premium

    return {
        "expected_return": round(expected_return, 4),
        "risk_free_rate": risk_free_rate,
        "beta": beta,
        "market_return": market_return,
        "market_risk_premium": round(market_risk_premium, 4),
        "stock_risk_premium": round(stock_risk_premium, 4),
        "beta_interpretation": (
            "Defensive (β < 1)"
            if beta < 1
            else "Market-neutral (β = 1)"
            if beta == 1
            else "Aggressive (β > 1)"
        ),
        "formula": f"E(R) = {risk_free_rate} + {beta} × ({market_return} - {risk_free_rate})",
    }


def sharpe_ratio(
    portfolio_return: float, risk_free_rate: float, portfolio_std_dev: float
) -> dict:
    """Sharpe Ratio = (Rp - Rf) / σp"""
    if portfolio_std_dev == 0:
        return {"error": "Standard deviation cannot be zero"}

    sharpe = (portfolio_return - risk_free_rate) / portfolio_std_dev

    return {
        "sharpe_ratio": round(sharpe, 4),
        "portfolio_return": portfolio_return,
        "risk_free_rate": risk_free_rate,
        "portfolio_std_dev": portfolio_std_dev,
        "excess_return": round(portfolio_return - risk_free_rate, 4),
        "interpretation": (
            "Excellent (>1)"
            if sharpe > 1
            else "Good (0.5-1)"
            if sharpe > 0.5
            else "Acceptable (0-0.5)"
            if sharpe > 0
            else "Poor (<0)"
        ),
        "formula": f"Sharpe = ({portfolio_return} - {risk_free_rate}) / {portfolio_std_dev}",
    }


def treynor_ratio(portfolio_return: float, risk_free_rate: float, beta: float) -> dict:
    """Treynor Ratio = (Rp - Rf) / βp"""
    if beta == 0:
        return {"error": "Beta cannot be zero"}

    treynor = (portfolio_return - risk_free_rate) / beta

    return {
        "treynor_ratio": round(treynor, 4),
        "portfolio_return": portfolio_return,
        "risk_free_rate": risk_free_rate,
        "beta": beta,
        "excess_return": round(portfolio_return - risk_free_rate, 4),
        "formula": f"Treynor = ({portfolio_return} - {risk_free_rate}) / {beta}",
    }


def jensens_alpha(
    portfolio_return: float,
    risk_free_rate: float,
    beta: float,
    market_return: float,
) -> dict:
    """Jensen's Alpha = Rp - [Rf + β × (Rm - Rf)]"""
    expected_return = risk_free_rate + beta * (market_return - risk_free_rate)
    alpha = portfolio_return - expected_return

    return {
        "jensens_alpha": round(alpha, 4),
        "portfolio_return": portfolio_return,
        "expected_return_capm": round(expected_return, 4),
        "outperformance": round(alpha, 4),
        "interpretation": (
            "Positive alpha - portfolio outperformed CAPM expectation"
            if alpha > 0
            else "Negative alpha - portfolio underperformed CAPM expectation"
        ),
        "formula": f"α = {portfolio_return} - [{risk_free_rate} + {beta} × ({market_return} - {risk_free_rate})]",
    }


def information_ratio(
    portfolio_return: float,
    benchmark_return: float,
    tracking_error: float,
) -> dict:
    """Information Ratio = (Rp - Rb) / Tracking Error"""
    if tracking_error == 0:
        return {"error": "Tracking error cannot be zero"}

    ir = (portfolio_return - benchmark_return) / tracking_error

    return {
        "information_ratio": round(ir, 4),
        "active_return": round(portfolio_return - benchmark_return, 4),
        "tracking_error": tracking_error,
        "interpretation": (
            "Excellent (>0.5)"
            if ir > 0.5
            else "Good (0.25-0.5)"
            if ir > 0.25
            else "Poor (<0.25)"
        ),
        "formula": f"IR = ({portfolio_return} - {benchmark_return}) / {tracking_error}",
    }


def sortino_ratio(
    portfolio_return: float,
    risk_free_rate: float,
    downside_deviation: float,
) -> dict:
    """Sortino Ratio = (Rp - Rf) / Downside Deviation"""
    if downside_deviation == 0:
        return {"error": "Downside deviation cannot be zero"}

    sortino = (portfolio_return - risk_free_rate) / downside_deviation

    return {
        "sortino_ratio": round(sortino, 4),
        "excess_return": round(portfolio_return - risk_free_rate, 4),
        "downside_deviation": downside_deviation,
        "interpretation": (
            "Excellent (>2)"
            if sortino > 2
            else "Good (1-2)"
            if sortino > 1
            else "Acceptable (0-1)"
            if sortino > 0
            else "Poor (<0)"
        ),
        "formula": f"Sortino = ({portfolio_return} - {risk_free_rate}) / {downside_deviation}",
    }


def asset_allocation_suggestion(
    age: int,
    risk_profile: str,
    investment_horizon_years: float,
) -> dict:
    """
    Suggest asset allocation based on age, risk profile, and horizon.
    """
    # Age-based equity rule: 100 - age = equity %
    age_based_equity = max(100 - age, 10)

    # Risk profile adjustment
    risk_adjustments = {
        "conservative": -20,
        "moderately_conservative": -10,
        "moderate": 0,
        "moderately_aggressive": 10,
        "aggressive": 20,
    }
    adjustment = risk_adjustments.get(risk_profile, 0)

    # Horizon adjustment
    if investment_horizon_years < 3:
        horizon_adj = -20
    elif investment_horizon_years < 5:
        horizon_adj = -10
    elif investment_horizon_years < 10:
        horizon_adj = 0
    else:
        horizon_adj = 10

    equity_pct = max(min(age_based_equity + adjustment + horizon_adj, 90), 10)
    debt_pct = max(100 - equity_pct - 10, 5)  # minimum 5% in debt
    gold_alternatives = 100 - equity_pct - debt_pct

    return {
        "recommended_allocation": {
            "equity": round(equity_pct, 1),
            "debt": round(debt_pct, 1),
            "gold_and_alternatives": round(gold_alternatives, 1),
        },
        "age_based_equity_rule": f"100 - {age} = {age_based_equity}%",
        "risk_profile": risk_profile,
        "investment_horizon": investment_horizon_years,
        "rationale": {
            "base_equity": age_based_equity,
            "risk_adjustment": adjustment,
            "horizon_adjustment": horizon_adj,
            "final_equity": equity_pct,
        },
        "reference": "Modern Portfolio Theory",
    }


def portfolio_rebalancing(
    target_allocation: dict[str, float],
    current_values: dict[str, float],
    additional_investment: float = 0,
) -> dict:
    """
    Calculate rebalancing trades needed.
    """
    total_current = sum(current_values.values())
    total_with_new = total_current + additional_investment

    trades = {}
    current_allocation = {}
    deviation = {}

    for asset, target_pct in target_allocation.items():
        current_val = current_values.get(asset, 0)
        current_pct = (current_val / total_current * 100) if total_current > 0 else 0
        target_val = total_with_new * target_pct / 100
        trade = target_val - current_val

        current_allocation[asset] = round(current_pct, 2)
        deviation[asset] = round(current_pct - target_pct, 2)
        trades[asset] = {
            "current_value": round(current_val, 2),
            "current_pct": round(current_pct, 2),
            "target_pct": target_pct,
            "target_value": round(target_val, 2),
            "action": "Buy" if trade > 0 else "Sell" if trade < 0 else "Hold",
            "amount": round(abs(trade), 2),
        }

    return {
        "total_portfolio_value": round(total_with_new, 2),
        "additional_investment": additional_investment,
        "trades": trades,
        "max_deviation": max(abs(v) for v in deviation.values()),
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_portfolio_return")
    def calculate_portfolio_return_tool(
        weights_json: str,
        returns_json: str,
    ) -> str:
        """Calculate expected portfolio return. E(Rp) = Σ w_i × E(R_i).
        weights: [0.6, 0.4], returns: [15, 8] (percentages)."""
        import json

        weights = json.loads(weights_json)
        returns = json.loads(returns_json)
        result = portfolio_expected_return(weights, returns)
        return format_tool_response("Portfolio Expected Return", result)

    @mcp.tool(name="calculate_portfolio_risk")
    def calculate_portfolio_risk_tool(
        weights_json: str,
        std_devs_json: str,
        correlations_json: str,
    ) -> str:
        """Calculate portfolio risk (variance and standard deviation).
        Shows diversification benefit.
        correlations: NxN matrix, e.g., [[1, 0.3], [0.3, 1]]."""
        import json

        weights = json.loads(weights_json)
        std_devs = json.loads(std_devs_json)
        correlations = json.loads(correlations_json)
        result = portfolio_risk(weights, std_devs, correlations)
        return format_tool_response("Portfolio Risk Analysis", result)

    @mcp.tool(name="analyze_two_asset_portfolio")
    def analyze_two_asset_portfolio_tool(
        weight_asset1: float,
        return_asset1: float,
        risk_asset1: float,
        return_asset2: float,
        risk_asset2: float,
        correlation: float,
    ) -> str:
        """Analyze a two-asset portfolio — return, risk, and minimum variance weights.
        Also finds the optimal minimum variance portfolio allocation."""
        result = two_asset_portfolio(
            weight_asset1,
            return_asset1,
            risk_asset1,
            return_asset2,
            risk_asset2,
            correlation,
        )
        return format_tool_response("Two-Asset Portfolio Analysis", result)

    @mcp.tool(name="calculate_capm_return")
    def calculate_capm_return_tool(
        risk_free_rate: float,
        beta: float,
        market_return: float,
    ) -> str:
        """Calculate expected return using CAPM.
        E(R) = Rf + β × (Rm - Rf).
        Beta < 1: defensive, Beta > 1: aggressive."""
        result = capm(risk_free_rate, beta, market_return)
        return format_tool_response("CAPM Expected Return", result)

    @mcp.tool(name="calculate_sharpe_ratio")
    def calculate_sharpe_ratio_tool(
        portfolio_return: float,
        risk_free_rate: float,
        portfolio_std_dev: float,
    ) -> str:
        """Calculate Sharpe Ratio = (Rp - Rf) / σp.
        Measures risk-adjusted return per unit of total risk."""
        result = sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std_dev)
        return format_tool_response("Sharpe Ratio", result)

    @mcp.tool(name="calculate_treynor_ratio")
    def calculate_treynor_ratio_tool(
        portfolio_return: float,
        risk_free_rate: float,
        beta: float,
    ) -> str:
        """Calculate Treynor Ratio = (Rp - Rf) / β.
        Measures excess return per unit of systematic risk (beta)."""
        result = treynor_ratio(portfolio_return, risk_free_rate, beta)
        return format_tool_response("Treynor Ratio", result)

    @mcp.tool(name="calculate_jensens_alpha")
    def calculate_jensens_alpha_tool(
        portfolio_return: float,
        risk_free_rate: float,
        beta: float,
        market_return: float,
    ) -> str:
        """Calculate Jensen's Alpha = Rp - [Rf + β(Rm - Rf)].
        Measures portfolio manager's skill — excess return over CAPM expectation."""
        result = jensens_alpha(portfolio_return, risk_free_rate, beta, market_return)
        return format_tool_response("Jensen's Alpha", result)

    @mcp.tool(name="calculate_information_ratio")
    def calculate_information_ratio_tool(
        portfolio_return: float,
        benchmark_return: float,
        tracking_error: float,
    ) -> str:
        """Calculate Information Ratio = Active Return / Tracking Error.
        Measures consistency of outperformance vs benchmark."""
        result = information_ratio(portfolio_return, benchmark_return, tracking_error)
        return format_tool_response("Information Ratio", result)

    @mcp.tool(name="calculate_sortino_ratio")
    def calculate_sortino_ratio_tool(
        portfolio_return: float,
        risk_free_rate: float,
        downside_deviation: float,
    ) -> str:
        """Calculate Sortino Ratio = (Rp - Rf) / Downside Deviation.
        Like Sharpe but only penalizes downside volatility, not upside."""
        result = sortino_ratio(portfolio_return, risk_free_rate, downside_deviation)
        return format_tool_response("Sortino Ratio", result)

    @mcp.tool(name="suggest_asset_allocation")
    def suggest_asset_allocation_tool(
        age: int,
        risk_profile: str,
        investment_horizon_years: float,
    ) -> str:
        """Suggest asset allocation based on age, risk profile, and investment horizon.
        Uses 100-age equity rule with adjustments.
        risk_profile: conservative, moderately_conservative, moderate, moderately_aggressive, aggressive."""
        result = asset_allocation_suggestion(
            age, risk_profile, investment_horizon_years
        )
        return format_tool_response("Asset Allocation Recommendation", result)

    @mcp.tool(name="rebalance_portfolio")
    def rebalance_portfolio_tool(
        target_allocation_json: str,
        current_values_json: str,
        additional_investment: float = 0,
    ) -> str:
        """Calculate trades needed to rebalance portfolio to target allocation.
        target_allocation: {"equity": 60, "debt": 30, "gold": 10} (percentages).
        current_values: {"equity": 700000, "debt": 250000, "gold": 50000} (amounts)."""
        import json

        target = json.loads(target_allocation_json)
        current = json.loads(current_values_json)
        result = portfolio_rebalancing(target, current, additional_investment)

        output = f"""
══════════════════════════════════════════════════
  Portfolio Rebalancing
══════════════════════════════════════════════════

  Total Portfolio: ₹{result["total_portfolio_value"]:,.2f}
  Additional Investment: ₹{result["additional_investment"]:,.2f}
  Max Deviation: {result["max_deviation"]:.2f}%

  Trades Required:
"""
        for asset, trade in result["trades"].items():
            output += f"    {asset.title()}:\n"
            output += f"      Current: ₹{trade['current_value']:,.2f} ({trade['current_pct']}%)\n"
            output += f"      Target:  ₹{trade['target_value']:,.2f} ({trade['target_pct']}%)\n"
            output += f"      Action:  {trade['action']} ₹{trade['amount']:,.2f}\n\n"

        output += "  Reference: Modern Portfolio Theory\n"
        return output

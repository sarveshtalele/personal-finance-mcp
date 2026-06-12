"""
Risk Profiling & Suitability (NISM Level 1, Ch 15: Portfolio Construction Process)

Bridges a client's risk *tolerance* (willingness) and risk *capacity* (ability)
into a profile and a suggested equity/debt split — the suitability step that must
precede any asset-allocation recommendation.
"""


def risk_profile_score(
    age: int,
    horizon_years: float,
    income_stability: int,
    investment_knowledge: int,
    loss_reaction: int,
    dependents: int = 0,
) -> dict:
    """
    Composite risk score (0-100) from capacity + tolerance factors.
      income_stability:    1 (very unstable) .. 5 (very stable)
      investment_knowledge:1 (none) .. 5 (expert)
      loss_reaction:       1 (sell in panic) .. 5 (buy more)
    """
    # Capacity (ability to take risk)
    age_score = max(0, min(100, (60 - age) / 40 * 100))      # younger -> higher
    horizon_score = max(0, min(100, horizon_years / 20 * 100))
    stability_score = (income_stability - 1) / 4 * 100
    dependents_score = max(0, 100 - dependents * 20)
    capacity = (age_score + horizon_score + stability_score + dependents_score) / 4

    # Tolerance (willingness to take risk)
    knowledge_score = (investment_knowledge - 1) / 4 * 100
    reaction_score = (loss_reaction - 1) / 4 * 100
    tolerance = (knowledge_score + reaction_score) / 2

    # Suitability uses the lower of the two as a guardrail, blended.
    score = round(0.5 * capacity + 0.5 * tolerance)
    score = min(score, round(capacity) + 15)  # cannot greatly exceed capacity

    if score >= 75:
        profile, equity = "Aggressive", 80
    elif score >= 55:
        profile, equity = "Moderately Aggressive", 65
    elif score >= 40:
        profile, equity = "Moderate", 50
    elif score >= 25:
        profile, equity = "Conservative", 30
    else:
        profile, equity = "Very Conservative", 15

    return {
        "risk_score": score,
        "risk_profile": profile,
        "risk_capacity": round(capacity),
        "risk_tolerance": round(tolerance),
        "suggested_equity_pct": equity,
        "suggested_debt_pct": 100 - equity,
        "guidance": (
            f"{profile} investor: target ~{equity}% growth assets (equity) and "
            f"{100 - equity}% stability assets (debt/cash). "
            "Re-profile after major life events."
        ),
        "formula": "Score = blend(capacity, tolerance), capped near capacity for suitability",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="assess_risk_profile")
    def assess_risk_profile_tool(
        age: int,
        horizon_years: float,
        income_stability: int = 3,
        investment_knowledge: int = 3,
        loss_reaction: int = 3,
        dependents: int = 0,
    ) -> str:
        """Determine an investor's risk profile (conservative→aggressive) and a
        suggested equity/debt split from age, horizon, income stability, knowledge,
        and reaction to losses. Use when a user asks 'what kind of investor am I',
        'how much risk should I take', or before recommending an asset allocation.
        Scales 1-5 for income_stability, investment_knowledge, loss_reaction."""
        return format_tool_response(
            "Risk Profile Assessment",
            risk_profile_score(
                age, horizon_years, income_stability,
                investment_knowledge, loss_reaction, dependents,
            ),
        )

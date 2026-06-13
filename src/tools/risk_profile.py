"""
Risk Profiling & Suitability

Bridges a client's risk *tolerance* (willingness) and risk *capacity* (ability)
into a profile and a suggested equity/debt split — the suitability step that must
precede any asset-allocation recommendation.

The equity/debt/gold split is NOT computed here independently. It is delegated to
the single allocation engine (`asset_allocation_suggestion`) so that this tool and
`suggest_asset_allocation` can never disagree for the same person.
"""

from .portfolio import asset_allocation_suggestion

# Risk-score band -> (label, allocation-engine profile key)
_PROFILE_BANDS = [
    (75, "Aggressive", "aggressive"),
    (55, "Moderately Aggressive", "moderately_aggressive"),
    (40, "Moderate", "moderate"),
    (25, "Conservative", "moderately_conservative"),
    (0, "Very Conservative", "conservative"),
]


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
    age_score = max(0, min(100, (60 - age) / 40 * 100))  # younger -> higher
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

    for threshold, label, key in _PROFILE_BANDS:
        if score >= threshold:
            profile, profile_key = label, key
            break

    # Single source of truth for the split — the allocation engine.
    alloc = asset_allocation_suggestion(age, profile_key, horizon_years)
    split = alloc["recommended_allocation"]
    equity = split["equity"]
    debt = split["debt"]
    gold = split["gold_and_alternatives"]

    return {
        "risk_score": score,
        "risk_profile": profile,
        "risk_capacity": round(capacity),
        "risk_tolerance": round(tolerance),
        "suggested_equity_pct": equity,
        "suggested_debt_pct": debt,
        "suggested_gold_pct": gold,
        "guidance": (
            f"{profile} investor: target {equity}% equity, {debt}% debt, {gold}% "
            f"gold/alternatives. Re-profile after major life events."
        ),
        "allocation_source": "asset_allocation_suggestion (canonical engine)",
        "presentation_note": (
            "Present these exact percentages. They match suggest_asset_allocation "
            "for the same age/horizon/profile — do not substitute other numbers."
        ),
        "formula": "Score = blend(capacity, tolerance); split delegated to allocation engine",
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
                age,
                horizon_years,
                income_stability,
                investment_knowledge,
                loss_reaction,
                dependents,
            ),
        )

"""Governance invariants: tools must not disagree with each other."""

import pytest

from src.tools.risk_profile import risk_profile_score
from src.tools.portfolio import asset_allocation_suggestion

PROFILE_KEY = {
    "Aggressive": "aggressive",
    "Moderately Aggressive": "moderately_aggressive",
    "Moderate": "moderate",
    "Conservative": "moderately_conservative",
    "Very Conservative": "conservative",
}


@pytest.mark.parametrize(
    "age,horizon,stab,know,react,deps",
    [
        (30, 30, 4, 3, 3, 0),
        (45, 15, 3, 3, 3, 2),
        (25, 35, 5, 5, 5, 0),
        (55, 8, 2, 2, 1, 3),
        (35, 25, 3, 4, 4, 1),
    ],
)
def test_risk_profile_matches_allocation_engine(age, horizon, stab, know, react, deps):
    """assess_risk_profile and suggest_asset_allocation must return the SAME split."""
    rp = risk_profile_score(age, horizon, stab, know, react, deps)
    alloc = asset_allocation_suggestion(age, PROFILE_KEY[rp["risk_profile"]], horizon)
    split = alloc["recommended_allocation"]
    assert rp["suggested_equity_pct"] == split["equity"]
    assert rp["suggested_debt_pct"] == split["debt"]
    assert rp["suggested_gold_pct"] == split["gold_and_alternatives"]


def test_allocation_sums_to_100():
    a = asset_allocation_suggestion(30, "moderately_aggressive", 30)[
        "recommended_allocation"
    ]
    assert round(a["equity"] + a["debt"] + a["gold_and_alternatives"]) == 100


def test_monthly_breakdown_matches_percentages():
    r = asset_allocation_suggestion(30, "aggressive", 30, monthly_investment=20000)
    mb = r["monthly_breakdown"]
    assert round(mb["equity"] + mb["debt"] + mb["gold_and_alternatives"], 2) == 20000.0


def test_allocation_carries_presentation_note():
    r = asset_allocation_suggestion(40, "moderate", 20)
    assert "presentation_note" in r

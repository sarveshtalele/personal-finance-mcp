"""Tests for the tool modules added in v1.1 (derivatives, India savings,
cash flow, risk profiling, advisor)."""

import math

from src.tools.derivatives import (
    futures_fair_value,
    option_payoff,
    black_scholes,
    beta_hedge,
    put_call_parity,
)
from src.tools.india_savings import (
    ppf_maturity,
    nsc_maturity,
    fixed_deposit,
    kvp_maturity,
    recurring_deposit,
)
from src.tools.cashflow import cash_flow_statement, debt_to_income, contingency_fund
from src.tools.risk_profile import risk_profile_score
from src.tools.advisor import create_financial_plan


class TestDerivatives:
    def test_futures_cost_of_carry(self):
        # S=100, r=8%, q=2%, t=1, continuous -> 100*e^0.06
        r = futures_fair_value(100, 8, 1, 2, continuous=True)
        assert abs(r["futures_fair_value"] - 100 * math.exp(0.06)) < 0.01

    def test_long_call_payoff(self):
        r = option_payoff("call", "long", 100, 5, 120)
        assert r["intrinsic_value"] == 20
        assert r["profit_loss"] == 15
        assert r["breakeven_price"] == 105

    def test_black_scholes_atm_call(self):
        r = black_scholes(100, 100, 5, 20, 1, "call")
        assert 10 < r["option_price"] < 11  # ~10.45

    def test_put_call_parity_solves_put(self):
        r = put_call_parity(100, 100, 5, 1, call_price=10)
        # P = C - (S - K e^-rt)
        assert abs(r["implied_put_price"] - (10 - (100 - 100 * math.exp(-0.05)))) < 0.01

    def test_beta_hedge(self):
        r = beta_hedge(1_000_000, 1.2, 20_000, 50)
        assert r["contracts_rounded"] == 1


class TestIndiaSavings:
    def test_nsc_compounding(self):
        r = nsc_maturity(100000, 7.7, 5)
        assert abs(r["maturity_value"] - 100000 * 1.077**5) < 0.01

    def test_ppf_positive_growth(self):
        r = ppf_maturity(150000, 7.1, 15)
        assert r["maturity_value"] > r["total_deposited"] > 0

    def test_fd_quarterly(self):
        r = fixed_deposit(100000, 7, 5, "quarterly")
        assert abs(r["maturity_value"] - 100000 * (1 + 0.07 / 4) ** 20) < 0.01

    def test_kvp_doubles(self):
        r = kvp_maturity(1000, 7.5)
        assert r["maturity_value"] == 2000
        assert r["years_to_double"] > 0

    def test_rd_beats_deposits(self):
        r = recurring_deposit(5000, 7, 12)
        assert r["maturity_value"] > r["total_deposited"]


class TestCashFlow:
    def test_savings_rate(self):
        r = cash_flow_statement(100000, 50000, 0, 15000)
        assert r["monthly_surplus"] == 35000
        assert r["savings_rate"] == 35.0

    def test_dti(self):
        r = debt_to_income(40000, 100000)
        assert r["debt_to_income_ratio"] == 40.0

    def test_contingency_gap(self):
        r = contingency_fund(50000, 6, 100000)
        assert r["target_fund"] == 300000
        assert r["shortfall"] == 200000


class TestRiskProfile:
    def test_young_aggressive(self):
        r = risk_profile_score(25, 35, 5, 4, 5, 0)
        assert r["suggested_equity_pct"] + r["suggested_debt_pct"] == 100
        assert r["risk_score"] >= 55

    def test_old_conservative(self):
        r = risk_profile_score(62, 3, 2, 1, 1, 2)
        assert r["suggested_equity_pct"] < 50


class TestAdvisor:
    def test_plan_returns_actions(self):
        p = create_financial_plan(30, 100000, 55000, 20000, 1, 50000)
        assert "prioritised_actions" in p
        assert isinstance(p["prioritised_actions"], list)
        assert p["monthly_surplus"] == 25000

    def test_deficit_flagged(self):
        p = create_financial_plan(40, 50000, 55000, 5000)
        assert any("deficit" in a.lower() for a in p["prioritised_actions"])

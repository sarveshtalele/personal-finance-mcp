"""Tests for Mutual Fund calculations — Financial Models"""

from src.tools.mutual_funds import (
    sip_calculator,
    sip_required_for_target,
    lumpsum_vs_sip,
    expense_ratio_impact,
    swp_calculator,
    cagr,
    nav_calculation,
)


class TestSIP:
    def test_basic_sip(self):
        result = sip_calculator(10000, 12, 10)
        assert result["future_value"] > 0
        assert result["total_invested"] == 1200000
        assert result["wealth_gained"] > 0

    def test_step_up_sip(self):
        basic = sip_calculator(10000, 12, 10, 0)
        stepped = sip_calculator(10000, 12, 10, 10)
        assert stepped["future_value"] > basic["future_value"]


class TestSIPRequired:
    def test_sip_for_target(self):
        result = sip_required_for_target(10000000, 12, 15)
        assert result["monthly_sip_needed"] > 0
        # Verify the SIP actually reaches the target
        verify = sip_calculator(result["monthly_sip_needed"], 12, 15)
        assert abs(verify["future_value"] - 10000000) < 100


class TestLumpsumVsSIP:
    def test_comparison(self):
        result = lumpsum_vs_sip(1200000, 12, 10)
        assert result["lumpsum_future_value"] > 0
        assert result["sip_future_value"] > 0
        assert result["better_option"] in ("Lump Sum", "SIP")


class TestExpenseRatio:
    def test_expense_impact(self):
        result = expense_ratio_impact(1000000, 12, 2, 20)
        assert result["fv_after_expenses"] < result["fv_without_expenses"]
        assert result["total_expense_cost"] > 0

    def test_comparison(self):
        result = expense_ratio_impact(1000000, 12, 2, 20, 0.5)
        assert "comparison_fv" in result


class TestSWP:
    def test_corpus_lasts(self):
        result = swp_calculator(10000000, 100000, 6)
        assert isinstance(result["years_lasted"], (int, float))
        assert result["years_lasted"] > 0

    def test_perpetual(self):
        result = swp_calculator(10000000, 10000, 8)
        assert result["months_lasted"] == "Perpetual"


class TestCAGR:
    def test_basic_cagr(self):
        result = cagr(100000, 300000, 10)
        assert abs(result["cagr"] - 11.6123) < 0.1

    def test_growth_multiple(self):
        result = cagr(100000, 200000, 7)
        assert result["growth_multiple"] == 2.0


class TestNAV:
    def test_nav(self):
        result = nav_calculation(100000000, 500000, 5000000)
        assert result["nav"] == 19.9

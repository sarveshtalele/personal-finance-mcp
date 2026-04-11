"""Tests for Time Value of Money calculations — Financial Models"""

from src.tools.tvm import (
    future_value,
    present_value,
    future_value_annuity,
    present_value_annuity,
    perpetuity_value,
    rule_of_72,
    effective_annual_rate,
    real_rate_of_return,
    inflation_adjusted_amount,
    required_monthly_savings,
)


class TestFutureValue:
    def test_annual_compounding(self):
        result = future_value(100000, 10, 5, 1)
        assert result["future_value"] == 161051.00

    def test_monthly_compounding(self):
        result = future_value(100000, 12, 10, 12)
        assert result["future_value"] == 330038.69

    def test_continuous_compounding(self):
        result = future_value(100000, 10, 5, 0)
        assert abs(result["future_value"] - 164872.13) < 0.01

    def test_compounding_benefit(self):
        result = future_value(100000, 12, 10, 12)
        assert result["compounding_benefit"] > 0
        assert result["simple_interest"] == 120000.0


class TestPresentValue:
    def test_basic_pv(self):
        result = present_value(161051, 10, 5, 1)
        assert abs(result["present_value"] - 100000) < 1

    def test_discount_factor(self):
        result = present_value(200000, 10, 5, 1)
        assert result["discount_factor"] < 1


class TestAnnuity:
    def test_fv_ordinary_annuity(self):
        result = future_value_annuity(10000, 12, 10, 12, "ordinary")
        assert result["future_value"] > 0
        assert result["total_invested"] == 1200000

    def test_fv_annuity_due(self):
        ordinary = future_value_annuity(10000, 12, 10, 12, "ordinary")
        due = future_value_annuity(10000, 12, 10, 12, "due")
        assert due["future_value"] > ordinary["future_value"]

    def test_pv_annuity(self):
        result = present_value_annuity(10000, 12, 10, 12, "ordinary")
        assert result["present_value"] > 0


class TestPerpetuity:
    def test_simple_perpetuity(self):
        result = perpetuity_value(10000, 10)
        assert result["present_value"] == 100000.0

    def test_growing_perpetuity(self):
        result = perpetuity_value(10000, 10, 3)
        assert abs(result["present_value"] - 142857.14) < 1

    def test_growing_perpetuity_invalid(self):
        result = perpetuity_value(10000, 5, 10)
        assert "error" in result


class TestRuleOf72:
    def test_at_12_percent(self):
        result = rule_of_72(12)
        assert result["years_to_double_approx"] == 6.0

    def test_at_8_percent(self):
        result = rule_of_72(8)
        assert result["years_to_double_approx"] == 9.0


class TestEffectiveRate:
    def test_monthly_compounding(self):
        result = effective_annual_rate(12, 12)
        assert result["effective_annual_rate"] > 12
        assert abs(result["effective_annual_rate"] - 12.6825) < 0.01

    def test_annual_equals_nominal(self):
        result = effective_annual_rate(10, 1)
        assert result["effective_annual_rate"] == 10.0


class TestRealReturn:
    def test_positive_real_return(self):
        result = real_rate_of_return(12, 6)
        assert result["real_rate"] > 0
        assert abs(result["real_rate"] - 5.6604) < 0.01


class TestInflation:
    def test_inflation_impact(self):
        result = inflation_adjusted_amount(100000, 6, 10)
        assert result["future_amount"] > 100000
        assert abs(result["future_amount"] - 179084.77) < 1


class TestSavingsNeeded:
    def test_monthly_savings(self):
        result = required_monthly_savings(10000000, 12, 20)
        assert result["monthly_savings_needed"] > 0

    def test_existing_savings_sufficient(self):
        result = required_monthly_savings(100000, 12, 10, 200000)
        assert result["monthly_savings_needed"] == 0

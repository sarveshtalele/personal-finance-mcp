"""Tests for Debt Management calculations — Financial Models"""

from src.tools.debt import (
    calculate_emi,
    loan_amortization_schedule,
    loan_comparison,
    prepayment_impact,
    invest_vs_prepay,
)


class TestEMI:
    def test_home_loan(self):
        result = calculate_emi(5000000, 8.5, 20)
        assert abs(result["emi"] - 43391.16) < 1

    def test_total_interest(self):
        result = calculate_emi(5000000, 8.5, 20)
        assert result["total_interest"] > result["principal"]

    def test_zero_rate(self):
        result = calculate_emi(1200000, 0, 10)
        assert result["emi"] == 10000.0

    def test_short_tenure(self):
        result = calculate_emi(100000, 12, 1)
        assert result["emi"] > 0
        assert result["tenure_months"] == 12


class TestAmortization:
    def test_schedule_generated(self):
        result = loan_amortization_schedule(1000000, 10, 5)
        assert len(result["schedule"]) > 0
        assert result["schedule"][0]["month"] == 1

    def test_balance_decreases(self):
        result = loan_amortization_schedule(1000000, 10, 5)
        balances = [r["balance"] for r in result["schedule"]]
        # First balance should be less than principal
        assert balances[0] < 1000000

    def test_final_balance_zero(self):
        result = loan_amortization_schedule(1000000, 10, 5)
        last = result["schedule"][-1]
        assert last["balance"] == 0


class TestLoanComparison:
    def test_comparison(self):
        loans = [
            {
                "principal": 5000000,
                "annual_rate": 8.5,
                "tenure_years": 20,
                "name": "Bank A",
            },
            {
                "principal": 5000000,
                "annual_rate": 9.0,
                "tenure_years": 20,
                "name": "Bank B",
            },
        ]
        result = loan_comparison(loans)
        assert result["comparison"][0]["name"] == "Bank A"  # Lower rate = lower cost


class TestPrepayment:
    def test_prepayment_saves(self):
        result = prepayment_impact(5000000, 8.5, 20, 5000)
        assert result["interest_saved"] > 0
        assert result["months_saved"] > 0


class TestInvestVsPrepay:
    def test_high_return_invest(self):
        result = invest_vs_prepay(8.5, 15, 30, True)
        assert "INVEST" in result["recommendation"]

    def test_low_return_prepay(self):
        result = invest_vs_prepay(12, 8, 30, False)
        assert "PREPAY" in result["recommendation"]

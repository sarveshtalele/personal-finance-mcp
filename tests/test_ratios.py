"""Tests for Financial Ratios — Financial Models"""

from src.tools.planning import (
    calculate_net_worth,
    calculate_financial_ratios,
    emergency_fund_calculator,
    budget_analysis,
    financial_health_score,
)


class TestNetWorth:
    def test_positive_net_worth(self):
        assets = {"house": 5000000, "fd": 300000, "stocks": 200000}
        liabilities = {"home_loan": 3000000}
        result = calculate_net_worth(assets, liabilities)
        assert result["net_worth"] == 2500000

    def test_negative_net_worth(self):
        assets = {"car": 500000}
        liabilities = {"car_loan": 600000, "personal_loan": 200000}
        result = calculate_net_worth(assets, liabilities)
        assert result["net_worth"] < 0


class TestFinancialRatios:
    def test_healthy_ratios(self):
        result = calculate_financial_ratios(
            monthly_income=200000,
            monthly_expenses=100000,
            monthly_emis=30000,
            monthly_savings=50000,
            total_assets=10000000,
            total_liabilities=3000000,
            liquid_assets=500000,
        )
        assert result["savings_ratio"] == 25.0
        assert result["debt_to_income_ratio"] == 15.0
        assert "Healthy" in result["assessments"]["savings_ratio"]

    def test_unhealthy_dti(self):
        result = calculate_financial_ratios(
            monthly_income=100000,
            monthly_expenses=60000,
            monthly_emis=45000,
            monthly_savings=5000,
            total_assets=2000000,
            total_liabilities=1800000,
            liquid_assets=50000,
        )
        assert "Danger" in result["assessments"]["debt_to_income"]


class TestEmergencyFund:
    def test_adequate_fund(self):
        result = emergency_fund_calculator(50000, 20000, 2, "stable", 250000)
        assert "Adequate" in result["status"]

    def test_shortfall(self):
        result = emergency_fund_calculator(50000, 20000, 2, "unstable", 100000)
        assert result["gap"] > 0


class TestBudgetAnalysis:
    def test_budget_50_30_20(self):
        result = budget_analysis(
            monthly_income=100000,
            expenses={
                "rent": 25000,
                "food": 15000,
                "entertainment": 5000,
                "shopping": 5000,
            },
            existing_emis=10000,
            existing_sips=15000,
        )
        assert result["surplus"] > 0
        assert result["savings_rate"] > 0


class TestFinancialHealthScore:
    def test_excellent_score(self):
        result = financial_health_score(
            monthly_income=300000,
            monthly_expenses=120000,
            total_assets=50000000,
            total_liabilities=5000000,
            liquid_assets=2000000,
            monthly_emis=30000,
            monthly_savings=100000,
            emergency_fund=1000000,
            insurance_cover=30000000,
            age=40,
        )
        assert result["total_score"] >= 60
        assert result["rating"] in ("Excellent", "Good")

    def test_poor_score(self):
        result = financial_health_score(
            monthly_income=50000,
            monthly_expenses=45000,
            total_assets=200000,
            total_liabilities=500000,
            liquid_assets=10000,
            monthly_emis=25000,
            monthly_savings=2000,
            emergency_fund=0,
            insurance_cover=0,
            age=35,
        )
        assert result["total_score"] < 40
        assert len(result["recommendations"]) > 0

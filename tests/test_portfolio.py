"""Tests for Portfolio Analytics — Financial Models-16"""

from src.tools.portfolio import (
    portfolio_expected_return,
    portfolio_risk,
    two_asset_portfolio,
    capm,
    sharpe_ratio,
    treynor_ratio,
    jensens_alpha,
    information_ratio,
    sortino_ratio,
    asset_allocation_suggestion,
    portfolio_rebalancing,
)


class TestPortfolioReturn:
    def test_expected_return(self):
        result = portfolio_expected_return([0.6, 0.4], [15, 8])
        assert abs(result["portfolio_expected_return"] - 12.2) < 0.01

    def test_dimension_mismatch(self):
        result = portfolio_expected_return([0.6], [15, 8])
        assert "error" in result


class TestPortfolioRisk:
    def test_two_asset_risk(self):
        result = portfolio_risk([0.6, 0.4], [20, 10], [[1, 0.3], [0.3, 1]])
        assert result["portfolio_std_dev"] > 0
        assert result["diversification_benefit"] > 0

    def test_perfect_correlation(self):
        result = portfolio_risk([0.5, 0.5], [10, 10], [[1, 1], [1, 1]])
        # With perfect correlation, diversification benefit = 0
        assert abs(result["diversification_benefit"]) < 0.01


class TestTwoAsset:
    def test_basic(self):
        result = two_asset_portfolio(0.6, 15, 20, 8, 10, 0.3)
        assert result["portfolio_return"] > 0
        assert result["portfolio_risk"] > 0
        assert "minimum_variance_portfolio" in result


class TestCAPM:
    def test_capm(self):
        result = capm(6, 1.2, 15)
        assert abs(result["expected_return"] - 16.8) < 0.01

    def test_defensive_beta(self):
        result = capm(6, 0.8, 15)
        assert "Defensive" in result["beta_interpretation"]


class TestSharpeRatio:
    def test_good_sharpe(self):
        result = sharpe_ratio(15, 6, 8)
        assert result["sharpe_ratio"] == 1.125
        assert "Excellent" in result["interpretation"]

    def test_poor_sharpe(self):
        result = sharpe_ratio(5, 6, 8)
        assert result["sharpe_ratio"] < 0


class TestTreynorRatio:
    def test_treynor(self):
        result = treynor_ratio(15, 6, 1.2)
        assert abs(result["treynor_ratio"] - 7.5) < 0.01


class TestJensensAlpha:
    def test_positive_alpha(self):
        result = jensens_alpha(18, 6, 1.2, 15)
        assert result["jensens_alpha"] > 0

    def test_negative_alpha(self):
        result = jensens_alpha(10, 6, 1.2, 15)
        assert result["jensens_alpha"] < 0


class TestInformationRatio:
    def test_ir(self):
        result = information_ratio(15, 12, 4)
        assert result["information_ratio"] == 0.75


class TestSortinoRatio:
    def test_sortino(self):
        result = sortino_ratio(15, 6, 5)
        assert result["sortino_ratio"] == 1.8


class TestAssetAllocation:
    def test_young_aggressive(self):
        result = asset_allocation_suggestion(25, "aggressive", 20)
        assert result["recommended_allocation"]["equity"] >= 70

    def test_old_conservative(self):
        result = asset_allocation_suggestion(60, "conservative", 5)
        assert result["recommended_allocation"]["equity"] <= 30


class TestRebalancing:
    def test_rebalance(self):
        result = portfolio_rebalancing(
            {"equity": 60, "debt": 30, "gold": 10},
            {"equity": 700000, "debt": 250000, "gold": 50000},
        )
        assert len(result["trades"]) == 3
        assert result["total_portfolio_value"] == 1000000

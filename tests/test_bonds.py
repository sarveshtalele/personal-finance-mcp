"""Tests for Bond calculations — Financial Models"""

from src.tools.bonds import (
    bond_price,
    current_yield,
    yield_to_maturity,
    bond_duration,
    bond_convexity,
    zero_coupon_bond_price,
)


class TestBondPrice:
    def test_premium_bond(self):
        # Coupon > YTM → premium
        result = bond_price(1000, 10, 8, 5, 2)
        assert result["bond_price"] > 1000
        assert "Premium" in result["premium_or_discount"]

    def test_discount_bond(self):
        # Coupon < YTM → discount
        result = bond_price(1000, 8, 10, 5, 2)
        assert result["bond_price"] < 1000
        assert "Discount" in result["premium_or_discount"]

    def test_par_bond(self):
        # Coupon = YTM → par
        result = bond_price(1000, 8, 8, 5, 2)
        assert abs(result["bond_price"] - 1000) < 0.01


class TestCurrentYield:
    def test_calculation(self):
        result = current_yield(80, 950)
        assert abs(result["current_yield"] - 8.4211) < 0.01


class TestYTM:
    def test_ytm_calculation(self):
        result = yield_to_maturity(1000, 8, 922.78, 5, 2)
        assert abs(result["ytm"] - 10.0) < 0.1

    def test_ytm_premium_bond(self):
        result = yield_to_maturity(1000, 10, 1081.11, 5, 2)
        assert result["ytm"] < 10  # YTM < coupon for premium


class TestDuration:
    def test_duration_less_than_maturity(self):
        result = bond_duration(1000, 8, 10, 5, 2)
        assert result["macaulay_duration_years"] < 5

    def test_modified_duration(self):
        result = bond_duration(1000, 8, 10, 5, 2)
        assert result["modified_duration"] < result["macaulay_duration_years"]


class TestConvexity:
    def test_convexity_positive(self):
        result = bond_convexity(1000, 8, 10, 5, 2)
        assert result["convexity_years"] > 0


class TestZeroCoupon:
    def test_zero_coupon_discount(self):
        result = zero_coupon_bond_price(1000, 10, 5)
        assert result["price"] < 1000
        assert abs(result["price"] - 620.92) < 1

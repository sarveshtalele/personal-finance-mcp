"""Tests for Stock Valuation — Financial Models"""

from src.tools.stocks import (
    gordon_growth_model,
    multi_stage_ddm,
    pe_valuation,
    dcf_valuation,
    dividend_yield,
)


class TestGordonGrowth:
    def test_basic_ddm(self):
        result = gordon_growth_model(5, 8, 15)
        # D1 = 5 * 1.08 = 5.4, P = 5.4 / (0.15 - 0.08) = 77.14
        assert abs(result["intrinsic_value"] - 77.14) < 1

    def test_invalid_growth_exceeds_return(self):
        result = gordon_growth_model(5, 15, 10)
        assert "error" in result


class TestMultiStageDDM:
    def test_two_stage(self):
        result = multi_stage_ddm(5, 20, 5, 5, 15)
        assert result["intrinsic_value"] > 0
        assert result["pv_high_growth_dividends"] > 0
        assert result["pv_terminal_value"] > 0


class TestPEValuation:
    def test_basic_pe(self):
        result = pe_valuation(50, 25)
        assert result["fair_price"] == 1250

    def test_peg_ratio(self):
        result = pe_valuation(50, 25, company_growth=20)
        assert result["peg_ratio"] == 1.25


class TestDCF:
    def test_dcf_basic(self):
        fcfs = [100, 120, 140, 160, 180]
        result = dcf_valuation(fcfs, 12, 3, 100, 200)
        assert result["enterprise_value"] > 0
        assert result["fair_price_per_share"] > 0

    def test_dcf_invalid(self):
        result = dcf_valuation([100], 3, 5)
        assert "error" in result


class TestDividendYield:
    def test_yield(self):
        result = dividend_yield(10, 200)
        assert result["dividend_yield"] == 5.0

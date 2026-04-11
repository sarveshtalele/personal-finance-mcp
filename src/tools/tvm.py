"""
Time Value of Money Calculations

Core formulas:
  FV = PV × (1 + r/n)^(n×t)           -- Future Value with compounding
  PV = FV / (1 + r/n)^(n×t)           -- Present Value
  FV_continuous = PV × e^(r×t)         -- Continuous compounding
  FV_annuity = PMT × [((1+r)^n - 1)/r]  -- Future Value of Annuity
  PV_annuity = PMT × [(1 - (1+r)^-n)/r] -- Present Value of Annuity
  PV_perpetuity = PMT / r             -- Present Value of Perpetuity
  PV_growing_perpetuity = PMT / (r-g) -- Growing Perpetuity
  Rule of 72: Years to double ≈ 72 / rate
"""

import math


def future_value(
    pv: float, annual_rate: float, years: float, compounding_periods: int = 1
) -> dict:
    """Calculate Future Value with compounding. FV = PV × (1 + r/n)^(n×t)"""
    r = annual_rate / 100
    n = compounding_periods
    t = years

    if n == 0:  # continuous compounding
        fv = pv * math.exp(r * t)
        formula = f"FV = PV × e^(r×t) = {pv:,.2f} × e^({r}×{t})"
    else:
        fv = pv * (1 + r / n) ** (n * t)
        formula = f"FV = PV × (1 + r/n)^(n×t) = {pv:,.2f} × (1 + {r}/{n})^({n}×{t})"

    simple_interest = pv * r * t
    compound_benefit = fv - pv - simple_interest

    return {
        "future_value": round(fv, 2),
        "present_value": pv,
        "total_interest": round(fv - pv, 2),
        "simple_interest": round(simple_interest, 2),
        "compounding_benefit": round(compound_benefit, 2),
        "growth_multiple": round(fv / pv, 4),
        "formula": formula,
    }


def present_value(
    fv: float, annual_rate: float, years: float, compounding_periods: int = 1
) -> dict:
    """Calculate Present Value. PV = FV / (1 + r/n)^(n×t)"""
    r = annual_rate / 100
    n = compounding_periods
    t = years

    if n == 0:  # continuous
        pv = fv * math.exp(-r * t)
        formula = f"PV = FV × e^(-r×t) = {fv:,.2f} × e^(-{r}×{t})"
    else:
        pv = fv / (1 + r / n) ** (n * t)
        formula = f"PV = FV / (1 + r/n)^(n×t) = {fv:,.2f} / (1 + {r}/{n})^({n}×{t})"

    discount = fv - pv

    return {
        "present_value": round(pv, 2),
        "future_value": fv,
        "discount": round(discount, 2),
        "discount_factor": round(pv / fv, 6),
        "formula": formula,
    }


def future_value_annuity(
    pmt: float,
    annual_rate: float,
    years: float,
    compounding_periods: int = 12,
    annuity_type: str = "ordinary",
) -> dict:
    """
    Future Value of Annuity.
    Ordinary: FV = PMT × [((1+r)^n - 1) / r]
    Due:      FV = PMT × [((1+r)^n - 1) / r] × (1+r)
    """
    r = annual_rate / 100 / compounding_periods
    n = int(years * compounding_periods)
    total_invested = pmt * n

    if r == 0:
        fv = pmt * n
    else:
        fv = pmt * (((1 + r) ** n - 1) / r)
        if annuity_type == "due":
            fv *= 1 + r

    wealth_gained = fv - total_invested

    return {
        "future_value": round(fv, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(wealth_gained, 2),
        "total_payments": n,
        "payment_amount": pmt,
        "effective_annual_rate": round((1 + r) ** compounding_periods - 1, 6) * 100,
        "formula": f"FV = PMT × [((1+r)^n - 1) / r] = {pmt:,.2f} × [((1+{r:.6f})^{n} - 1) / {r:.6f}]",
    }


def present_value_annuity(
    pmt: float,
    annual_rate: float,
    years: float,
    compounding_periods: int = 12,
    annuity_type: str = "ordinary",
) -> dict:
    """
    Present Value of Annuity.
    Ordinary: PV = PMT × [(1 - (1+r)^-n) / r]
    Due:      PV = PMT × [(1 - (1+r)^-n) / r] × (1+r)
    """
    r = annual_rate / 100 / compounding_periods
    n = int(years * compounding_periods)

    if r == 0:
        pv = pmt * n
    else:
        pv = pmt * ((1 - (1 + r) ** (-n)) / r)
        if annuity_type == "due":
            pv *= 1 + r

    total_payments = pmt * n

    return {
        "present_value": round(pv, 2),
        "total_payments": round(total_payments, 2),
        "total_interest": round(total_payments - pv, 2),
        "num_payments": n,
        "formula": f"PV = PMT × [(1 - (1+r)^-n) / r] = {pmt:,.2f} × [(1 - (1+{r:.6f})^-{n}) / {r:.6f}]",
    }


def perpetuity_value(pmt: float, annual_rate: float, growth_rate: float = 0) -> dict:
    """
    Present Value of Perpetuity.
    Simple:  PV = PMT / r
    Growing: PV = PMT / (r - g)  where r > g
    """
    r = annual_rate / 100
    g = growth_rate / 100

    if growth_rate > 0:
        if r <= g:
            return {
                "error": "Required return must be greater than growth rate for growing perpetuity"
            }
        pv = pmt / (r - g)
        formula = f"PV = PMT / (r - g) = {pmt:,.2f} / ({r} - {g})"
        perpetuity_type = "growing"
    else:
        pv = pmt / r
        formula = f"PV = PMT / r = {pmt:,.2f} / {r}"
        perpetuity_type = "simple"

    return {
        "present_value": round(pv, 2),
        "annual_payment": pmt,
        "perpetuity_type": perpetuity_type,
        "formula": formula,
    }


def rule_of_72(annual_rate: float) -> dict:
    """Rule of 72: Approximate years to double an investment."""
    years_approx = 72 / annual_rate
    years_exact = math.log(2) / math.log(1 + annual_rate / 100)

    return {
        "years_to_double_approx": round(years_approx, 2),
        "years_to_double_exact": round(years_exact, 2),
        "rate": annual_rate,
        "formula": f"Years ≈ 72 / {annual_rate} = {years_approx:.2f}",
    }


def effective_annual_rate(nominal_rate: float, compounding_periods: int) -> dict:
    """EAR = (1 + r/n)^n - 1"""
    r = nominal_rate / 100
    n = compounding_periods

    if n == 0:  # continuous
        ear = math.exp(r) - 1
        formula = f"EAR = e^r - 1 = e^{r} - 1"
    else:
        ear = (1 + r / n) ** n - 1
        formula = f"EAR = (1 + r/n)^n - 1 = (1 + {r}/{n})^{n} - 1"

    return {
        "effective_annual_rate": round(ear * 100, 4),
        "nominal_rate": nominal_rate,
        "compounding_periods": n,
        "rate_difference": round((ear * 100) - nominal_rate, 4),
        "formula": formula,
    }


def real_rate_of_return(nominal_rate: float, inflation_rate: float) -> dict:
    """Fisher equation: (1 + real) = (1 + nominal) / (1 + inflation)"""
    r_nom = nominal_rate / 100
    r_inf = inflation_rate / 100

    real = ((1 + r_nom) / (1 + r_inf)) - 1
    approx = r_nom - r_inf

    return {
        "real_rate": round(real * 100, 4),
        "approximate_real_rate": round(approx * 100, 4),
        "nominal_rate": nominal_rate,
        "inflation_rate": inflation_rate,
        "formula": f"Real = ((1 + {r_nom}) / (1 + {r_inf})) - 1",
    }


def inflation_adjusted_amount(
    current_amount: float, inflation_rate: float, years: float
) -> dict:
    """Calculate the future cost of something accounting for inflation."""
    r = inflation_rate / 100
    future_amount = current_amount * (1 + r) ** years
    purchasing_power_loss = future_amount - current_amount

    return {
        "future_amount": round(future_amount, 2),
        "current_amount": current_amount,
        "purchasing_power_loss": round(purchasing_power_loss, 2),
        "inflation_multiplier": round((1 + r) ** years, 4),
        "formula": f"Future = {current_amount:,.2f} × (1 + {r})^{years}",
    }


def required_monthly_savings(
    target_amount: float,
    annual_rate: float,
    years: float,
    current_savings: float = 0,
) -> dict:
    """Calculate monthly savings needed to reach a target corpus."""
    r = annual_rate / 100 / 12
    n = int(years * 12)

    # Future value of current savings
    fv_current = current_savings * (1 + r) ** n if current_savings > 0 else 0
    remaining_target = target_amount - fv_current

    if remaining_target <= 0:
        return {
            "monthly_savings_needed": 0,
            "message": "Current savings will exceed the target!",
            "future_value_of_current_savings": round(fv_current, 2),
        }

    if r == 0:
        monthly = remaining_target / n
    else:
        monthly = remaining_target * r / ((1 + r) ** n - 1)

    total_invested = monthly * n + current_savings

    return {
        "monthly_savings_needed": round(monthly, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(target_amount - total_invested, 2),
        "future_value_of_current_savings": round(fv_current, 2),
        "target_amount": target_amount,
        "formula": f"PMT = FV × r / ((1+r)^n - 1) = {remaining_target:,.2f} × {r:.6f} / ((1+{r:.6f})^{n} - 1)",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_future_value")
    def calculate_future_value_tool(
        present_value: float,
        annual_rate: float,
        years: float,
        compounding: str = "annually",
    ) -> str:
        """Calculate Future Value of a lump sum investment with compounding.
        FV = PV × (1 + r/n)^(n×t). Use compounding: annually, semi_annually, quarterly, monthly, daily, continuous."""
        freq_map = {
            "annually": 1,
            "semi_annually": 2,
            "quarterly": 4,
            "monthly": 12,
            "daily": 365,
            "continuous": 0,
        }
        n = freq_map.get(compounding, 1)
        result = future_value(present_value, annual_rate, years, n)
        return format_tool_response("Future Value Calculation", result)

    @mcp.tool(name="calculate_present_value")
    def calculate_present_value_tool(
        future_value: float,
        annual_rate: float,
        years: float,
        compounding: str = "annually",
    ) -> str:
        """Calculate Present Value — what a future sum is worth today.
        PV = FV / (1 + r/n)^(n×t)."""
        freq_map = {
            "annually": 1,
            "semi_annually": 2,
            "quarterly": 4,
            "monthly": 12,
            "daily": 365,
            "continuous": 0,
        }
        n = freq_map.get(compounding, 1)
        result = present_value(future_value, annual_rate, years, n)
        return format_tool_response("Present Value Calculation", result)

    @mcp.tool(name="calculate_annuity_fv")
    def calculate_annuity_fv_tool(
        payment: float,
        annual_rate: float,
        years: float,
        frequency: str = "monthly",
        annuity_type: str = "ordinary",
    ) -> str:
        """Calculate Future Value of regular periodic payments (annuity/SIP).
        Ordinary annuity: payments at end of period. Due: at beginning."""
        freq_map = {"annually": 1, "semi_annually": 2, "quarterly": 4, "monthly": 12}
        n = freq_map.get(frequency, 12)
        result = future_value_annuity(payment, annual_rate, years, n, annuity_type)
        return format_tool_response("Future Value of Annuity", result)

    @mcp.tool(name="calculate_annuity_pv")
    def calculate_annuity_pv_tool(
        payment: float,
        annual_rate: float,
        years: float,
        frequency: str = "monthly",
        annuity_type: str = "ordinary",
    ) -> str:
        """Calculate Present Value of regular periodic payments.
        Useful for valuing loan payments, pension, lease payments."""
        freq_map = {"annually": 1, "semi_annually": 2, "quarterly": 4, "monthly": 12}
        n = freq_map.get(frequency, 12)
        result = present_value_annuity(payment, annual_rate, years, n, annuity_type)
        return format_tool_response("Present Value of Annuity", result)

    @mcp.tool(name="calculate_perpetuity")
    def calculate_perpetuity_tool(
        payment: float,
        annual_rate: float,
        growth_rate: float = 0,
    ) -> str:
        """Calculate Present Value of perpetuity (infinite periodic payments).
        Simple: PV = PMT/r. Growing: PV = PMT/(r-g)."""
        result = perpetuity_value(payment, annual_rate, growth_rate)
        return format_tool_response("Perpetuity Valuation", result)

    @mcp.tool(name="calculate_rule_of_72")
    def calculate_rule_of_72_tool(annual_rate: float) -> str:
        """Rule of 72: Approximate how many years to double your money.
        Years ≈ 72 / annual_rate."""
        result = rule_of_72(annual_rate)
        return format_tool_response("Rule of 72", result)

    @mcp.tool(name="calculate_effective_rate")
    def calculate_effective_rate_tool(
        nominal_rate: float,
        compounding: str = "monthly",
    ) -> str:
        """Calculate Effective Annual Rate from nominal rate.
        EAR = (1 + r/n)^n - 1. Compare rates with different compounding."""
        freq_map = {
            "annually": 1,
            "semi_annually": 2,
            "quarterly": 4,
            "monthly": 12,
            "daily": 365,
            "continuous": 0,
        }
        n = freq_map.get(compounding, 12)
        result = effective_annual_rate(nominal_rate, n)
        return format_tool_response("Effective Annual Rate", result)

    @mcp.tool(name="calculate_real_return")
    def calculate_real_return_tool(
        nominal_rate: float,
        inflation_rate: float,
    ) -> str:
        """Calculate real (inflation-adjusted) rate of return using Fisher equation.
        (1 + real) = (1 + nominal) / (1 + inflation)."""
        result = real_rate_of_return(nominal_rate, inflation_rate)
        return format_tool_response("Real Rate of Return", result)

    @mcp.tool(name="calculate_inflation_impact")
    def calculate_inflation_impact_tool(
        current_amount: float,
        inflation_rate: float,
        years: float,
    ) -> str:
        """Calculate future cost of something after inflation.
        Shows how much more you'll need in the future for the same expense."""
        result = inflation_adjusted_amount(current_amount, inflation_rate, years)
        return format_tool_response("Inflation Impact", result)

    @mcp.tool(name="calculate_savings_needed")
    def calculate_savings_needed_tool(
        target_amount: float,
        annual_rate: float,
        years: float,
        current_savings: float = 0,
    ) -> str:
        """Calculate monthly savings required to reach a financial target.
        Accounts for existing savings and expected returns."""
        result = required_monthly_savings(
            target_amount, annual_rate, years, current_savings
        )
        return format_tool_response("Monthly Savings Calculator", result)

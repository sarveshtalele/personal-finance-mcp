"""
Mutual Fund Calculations

Key formulas:
  NAV = (Total Assets - Total Liabilities) / Units Outstanding
  SIP FV = PMT × [((1+r)^n - 1) / r] × (1+r)
  CAGR = (End Value / Start Value)^(1/n) - 1
  Expense Ratio Impact on returns
  Step-up SIP: Annual increase in SIP amount
"""


def sip_calculator(
    monthly_investment: float,
    annual_return: float,
    years: float,
    step_up_percentage: float = 0,
) -> dict:
    """
    SIP (Systematic Investment Plan) calculator.
    FV = PMT × [((1+r)^n - 1) / r] × (1+r)
    With optional annual step-up.
    """
    r = annual_return / 100 / 12
    total_months = int(years * 12)

    if step_up_percentage == 0:
        # Simple SIP
        if r == 0:
            fv = monthly_investment * total_months
        else:
            fv = monthly_investment * (((1 + r) ** total_months - 1) / r) * (1 + r)
        total_invested = monthly_investment * total_months
    else:
        # Step-up SIP: increase monthly amount annually
        fv = 0
        total_invested = 0
        current_sip = monthly_investment
        remaining_months = total_months

        for year in range(int(years)):
            months_this_year = min(12, remaining_months)
            if r == 0:
                year_fv = current_sip * months_this_year
            else:
                year_fv = (
                    current_sip * (((1 + r) ** months_this_year - 1) / r) * (1 + r)
                )

            # Compound previous FV for this year
            fv = fv * (1 + r) ** months_this_year + year_fv
            total_invested += current_sip * months_this_year
            remaining_months -= months_this_year
            current_sip *= 1 + step_up_percentage / 100

    wealth_gained = fv - total_invested

    return {
        "future_value": round(fv, 2),
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(wealth_gained, 2),
        "monthly_sip": monthly_investment,
        "annual_return": annual_return,
        "years": years,
        "step_up": step_up_percentage,
        "wealth_ratio": round(fv / total_invested, 2) if total_invested > 0 else 0,
        "formula": "FV = PMT × [((1+r)^n - 1) / r] × (1+r)"
        + (" with annual step-up" if step_up_percentage > 0 else ""),
    }


def sip_required_for_target(
    target_amount: float,
    annual_return: float,
    years: float,
) -> dict:
    """Calculate the monthly SIP needed to reach a target corpus."""
    r = annual_return / 100 / 12
    n = int(years * 12)

    if r == 0:
        monthly = target_amount / n
    else:
        monthly = target_amount / ((((1 + r) ** n - 1) / r) * (1 + r))

    total_invested = monthly * n
    wealth_gained = target_amount - total_invested

    return {
        "monthly_sip_needed": round(monthly, 2),
        "target_amount": target_amount,
        "total_invested": round(total_invested, 2),
        "wealth_gained": round(wealth_gained, 2),
        "years": years,
        "annual_return": annual_return,
        "formula": "SIP = Target / [((1+r)^n - 1)/r × (1+r)]",
    }


def lumpsum_vs_sip(
    total_amount: float,
    annual_return: float,
    years: float,
) -> dict:
    """Compare lump sum investing vs SIP over same period."""
    r_monthly = annual_return / 100 / 12
    n = int(years * 12)
    monthly_sip = total_amount / n

    # Lump sum
    fv_lumpsum = total_amount * (1 + annual_return / 100) ** years

    # SIP
    if r_monthly == 0:
        fv_sip = monthly_sip * n
    else:
        fv_sip = (
            monthly_sip * (((1 + r_monthly) ** n - 1) / r_monthly) * (1 + r_monthly)
        )

    return {
        "lumpsum_future_value": round(fv_lumpsum, 2),
        "sip_future_value": round(fv_sip, 2),
        "lumpsum_gain": round(fv_lumpsum - total_amount, 2),
        "sip_gain": round(fv_sip - total_amount, 2),
        "difference": round(fv_lumpsum - fv_sip, 2),
        "better_option": "Lump Sum" if fv_lumpsum > fv_sip else "SIP",
        "note": "Lump sum usually wins in rising markets; SIP provides rupee cost averaging in volatile markets",
    }


def expense_ratio_impact(
    investment_amount: float,
    annual_return: float,
    expense_ratio: float,
    years: float,
    comparison_expense_ratio: float = 0,
) -> dict:
    """
    Show impact of expense ratio on returns.
    Net Return = Gross Return - Expense Ratio
    """
    net_return = annual_return - expense_ratio
    fv_with_expense = investment_amount * (1 + net_return / 100) ** years
    fv_without_expense = investment_amount * (1 + annual_return / 100) ** years
    cost_of_expense = fv_without_expense - fv_with_expense

    result = {
        "gross_return": annual_return,
        "expense_ratio": expense_ratio,
        "net_return": round(net_return, 2),
        "fv_after_expenses": round(fv_with_expense, 2),
        "fv_without_expenses": round(fv_without_expense, 2),
        "total_expense_cost": round(cost_of_expense, 2),
        "expense_as_pct_of_gains": round(
            cost_of_expense / (fv_without_expense - investment_amount) * 100, 2
        )
        if fv_without_expense > investment_amount
        else 0,
    }

    if comparison_expense_ratio > 0:
        net_return_2 = annual_return - comparison_expense_ratio
        fv_2 = investment_amount * (1 + net_return_2 / 100) ** years
        result["comparison_expense_ratio"] = comparison_expense_ratio
        result["comparison_fv"] = round(fv_2, 2)
        result["savings_by_lower_expense"] = round(abs(fv_with_expense - fv_2), 2)

    return result


def swp_calculator(
    corpus: float,
    monthly_withdrawal: float,
    annual_return: float,
) -> dict:
    """
    Systematic Withdrawal Plan - how long will corpus last?
    """
    r = annual_return / 100 / 12
    balance = corpus
    months = 0

    if r > 0 and monthly_withdrawal <= corpus * r:
        return {
            "corpus": corpus,
            "monthly_withdrawal": monthly_withdrawal,
            "annual_return": annual_return,
            "months_lasted": "Perpetual",
            "years_lasted": "Perpetual",
            "message": "Monthly return exceeds withdrawal - corpus will grow indefinitely",
        }

    while balance > 0 and months < 1200:  # cap at 100 years
        balance = balance * (1 + r) - monthly_withdrawal
        months += 1
        if balance <= 0:
            break

    return {
        "corpus": corpus,
        "monthly_withdrawal": monthly_withdrawal,
        "annual_return": annual_return,
        "months_lasted": months,
        "years_lasted": round(months / 12, 1),
        "total_withdrawn": round(monthly_withdrawal * months, 2),
    }


def cagr(start_value: float, end_value: float, years: float) -> dict:
    """CAGR = (End/Start)^(1/n) - 1"""
    if start_value <= 0:
        return {"error": "Start value must be positive"}

    cagr_val = (end_value / start_value) ** (1 / years) - 1
    absolute_return = (end_value - start_value) / start_value * 100

    return {
        "cagr": round(cagr_val * 100, 4),
        "absolute_return": round(absolute_return, 2),
        "start_value": start_value,
        "end_value": end_value,
        "years": years,
        "growth_multiple": round(end_value / start_value, 4),
        "formula": f"CAGR = ({end_value}/{start_value})^(1/{years}) - 1",
    }


def nav_calculation(
    total_assets: float, total_liabilities: float, units_outstanding: float
) -> dict:
    """NAV = (Total Assets - Total Liabilities) / Units Outstanding"""
    nav = (total_assets - total_liabilities) / units_outstanding

    return {
        "nav": round(nav, 4),
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "units_outstanding": units_outstanding,
        "formula": f"NAV = ({total_assets} - {total_liabilities}) / {units_outstanding}",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_sip_returns")
    def calculate_sip_returns_tool(
        monthly_investment: float,
        annual_return: float,
        years: float,
        step_up_percentage: float = 0,
    ) -> str:
        """Calculate SIP (Systematic Investment Plan) returns.
        Shows future value, total invested, and wealth gained.
        Optional step_up_percentage: annual increase in SIP amount (e.g., 10 for 10%)."""
        result = sip_calculator(
            monthly_investment, annual_return, years, step_up_percentage
        )
        return format_tool_response("SIP Calculator", result)

    @mcp.tool(name="calculate_sip_needed")
    def calculate_sip_needed_tool(
        target_amount: float,
        annual_return: float,
        years: float,
    ) -> str:
        """Calculate monthly SIP needed to reach a target corpus.
        Inverse SIP calculation — find the monthly amount for a given goal."""
        result = sip_required_for_target(target_amount, annual_return, years)
        return format_tool_response("SIP Required for Target", result)

    @mcp.tool(name="compare_lumpsum_vs_sip")
    def compare_lumpsum_vs_sip_tool(
        total_amount: float,
        annual_return: float,
        years: float,
    ) -> str:
        """Compare lump sum investment vs SIP for the same total amount.
        Lump sum: invest everything today. SIP: spread equally over the period."""
        result = lumpsum_vs_sip(total_amount, annual_return, years)
        return format_tool_response("Lump Sum vs SIP Comparison", result)

    @mcp.tool(name="analyze_expense_ratio_impact")
    def analyze_expense_ratio_impact_tool(
        investment_amount: float,
        annual_return: float,
        expense_ratio: float,
        years: float,
        comparison_expense_ratio: float = 0,
    ) -> str:
        """Show how expense ratio eats into your mutual fund returns over time.
        Optionally compare two funds with different expense ratios."""
        result = expense_ratio_impact(
            investment_amount,
            annual_return,
            expense_ratio,
            years,
            comparison_expense_ratio,
        )
        return format_tool_response("Expense Ratio Impact Analysis", result)

    @mcp.tool(name="calculate_swp")
    def calculate_swp_tool(
        corpus: float,
        monthly_withdrawal: float,
        annual_return: float,
    ) -> str:
        """Systematic Withdrawal Plan — how long will your corpus last?
        Calculate sustainability of regular withdrawals from an investment corpus."""
        result = swp_calculator(corpus, monthly_withdrawal, annual_return)
        return format_tool_response("SWP Calculator", result)

    @mcp.tool(name="calculate_cagr")
    def calculate_cagr_tool(
        start_value: float,
        end_value: float,
        years: float,
    ) -> str:
        """Calculate CAGR (Compound Annual Growth Rate).
        CAGR = (End/Start)^(1/n) - 1. Standard measure for investment returns."""
        result = cagr(start_value, end_value, years)
        return format_tool_response("CAGR Calculator", result)

    @mcp.tool(name="calculate_nav")
    def calculate_nav_tool(
        total_assets: float,
        total_liabilities: float,
        units_outstanding: float,
    ) -> str:
        """Calculate Mutual Fund NAV (Net Asset Value).
        NAV = (Total Assets - Total Liabilities) / Units Outstanding."""
        result = nav_calculation(total_assets, total_liabilities, units_outstanding)
        return format_tool_response("NAV Calculation", result)

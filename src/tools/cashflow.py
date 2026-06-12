"""
Cash Flow & Budgeting (NISM Level 1, Ch 3: Evaluating the Financial Position of Clients)

Tools for household cash-flow analysis, savings rate, debt servicing capacity
and contingency (emergency) fund adequacy — the building blocks of evaluating
a client's financial position before any investing advice.
"""


def cash_flow_statement(
    monthly_income: float,
    fixed_expenses: float,
    variable_expenses: float,
    emi: float = 0.0,
) -> dict:
    """Monthly surplus, savings rate and expense ratio from a household cash flow."""
    total_outflow = fixed_expenses + variable_expenses + emi
    surplus = monthly_income - total_outflow
    savings_rate = (surplus / monthly_income * 100) if monthly_income else 0
    expense_ratio = (total_outflow / monthly_income * 100) if monthly_income else 0

    if savings_rate >= 30:
        verdict = "Excellent — strong surplus to invest"
    elif savings_rate >= 20:
        verdict = "Healthy savings rate"
    elif savings_rate >= 10:
        verdict = "Adequate, aim for 20%+"
    elif savings_rate >= 0:
        verdict = "Thin surplus — review variable spending"
    else:
        verdict = "Deficit — outflows exceed income"

    return {
        "monthly_income": monthly_income,
        "total_outflow": round(total_outflow, 2),
        "monthly_surplus": round(surplus, 2),
        "savings_rate": round(savings_rate, 2),
        "expense_ratio": round(expense_ratio, 2),
        "annual_surplus": round(surplus * 12, 2),
        "verdict": verdict,
        "formula": "Surplus = Income - (Fixed + Variable + EMI); Savings rate = Surplus / Income",
    }


def debt_to_income(monthly_emi_total: float, monthly_income: float) -> dict:
    """Debt-to-income (debt servicing) ratio and borrowing-capacity verdict."""
    dti = (monthly_emi_total / monthly_income * 100) if monthly_income else 0
    if dti <= 30:
        verdict = "Comfortable — room to borrow if needed"
    elif dti <= 40:
        verdict = "Acceptable upper limit (lenders' typical cap ~40%)"
    elif dti <= 50:
        verdict = "Stretched — avoid new debt"
    else:
        verdict = "Over-leveraged — prioritise debt reduction"
    return {
        "debt_to_income_ratio": round(dti, 2),
        "monthly_emi_total": monthly_emi_total,
        "monthly_income": monthly_income,
        "verdict": verdict,
        "max_prudent_emi": round(monthly_income * 0.40, 2),
        "additional_emi_capacity": round(max(monthly_income * 0.40 - monthly_emi_total, 0), 2),
        "formula": "DTI = Total EMI / Monthly Income; prudent cap ≈ 40%",
    }


def contingency_fund(
    monthly_expenses: float,
    months_target: int = 6,
    existing_fund: float = 0.0,
) -> dict:
    """Contingency / emergency fund target, gap and current coverage."""
    target = monthly_expenses * months_target
    gap = max(target - existing_fund, 0)
    months_covered = (existing_fund / monthly_expenses) if monthly_expenses else 0
    return {
        "target_fund": round(target, 2),
        "existing_fund": existing_fund,
        "shortfall": round(gap, 2),
        "months_currently_covered": round(months_covered, 1),
        "months_target": months_target,
        "status": "Funded" if gap == 0 else "Underfunded",
        "formula": "Target = Monthly Expenses × Months (3-6 typical, 12 if income volatile)",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="analyze_cash_flow")
    def analyze_cash_flow_tool(
        monthly_income: float,
        fixed_expenses: float,
        variable_expenses: float,
        emi: float = 0.0,
    ) -> str:
        """Household cash-flow analysis: monthly surplus, savings rate, expense ratio.
        Use when a user describes their income and spending and asks 'how am I doing',
        'how much can I save/invest', or wants a budget health check."""
        return format_tool_response(
            "Household Cash Flow",
            cash_flow_statement(monthly_income, fixed_expenses, variable_expenses, emi),
        )

    @mcp.tool(name="calculate_debt_to_income")
    def calculate_dti_tool(monthly_emi_total: float, monthly_income: float) -> str:
        """Debt-to-income (debt servicing) ratio and how much more EMI is prudent.
        Use for 'can I afford another loan', 'am I over-leveraged', loan eligibility."""
        return format_tool_response(
            "Debt-to-Income Ratio", debt_to_income(monthly_emi_total, monthly_income)
        )

    @mcp.tool(name="calculate_contingency_fund")
    def calculate_contingency_tool(
        monthly_expenses: float, months_target: int = 6, existing_fund: float = 0.0
    ) -> str:
        """Contingency / emergency fund target and shortfall.
        Use for 'how big should my emergency fund be', 'am I covered if I lose my job'.
        Recommend 3-6 months of expenses (12 if income is irregular)."""
        return format_tool_response(
            "Contingency Fund Plan",
            contingency_fund(monthly_expenses, months_target, existing_fund),
        )

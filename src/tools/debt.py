"""
Debt Management and Loan Calculations

Core formulas:
  EMI = P × r × (1+r)^n / ((1+r)^n - 1)
  Total Interest = (EMI × n) - P
  Outstanding = P × (1+r)^k - EMI × ((1+r)^k - 1) / r
  Debt-to-Income Ratio = Total Monthly Debt / Gross Monthly Income
"""


def calculate_emi(principal: float, annual_rate: float, tenure_years: float) -> dict:
    """
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    where P = principal, r = monthly rate, n = total months
    """
    r = annual_rate / 100 / 12
    n = int(tenure_years * 12)

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    total_payment = emi * n
    total_interest = total_payment - principal

    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "interest_to_principal_ratio": round(total_interest / principal, 4),
        "principal": principal,
        "annual_rate": annual_rate,
        "tenure_months": n,
        "formula": f"EMI = {principal:,.2f} × {r:.6f} × (1+{r:.6f})^{n} / ((1+{r:.6f})^{n} - 1)",
    }


def loan_amortization_schedule(
    principal: float, annual_rate: float, tenure_years: float, max_rows: int = 24
) -> dict:
    """Generate loan amortization schedule showing principal and interest split."""
    r = annual_rate / 100 / 12
    n = int(tenure_years * 12)

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    schedule = []
    balance = principal
    total_interest_paid = 0
    total_principal_paid = 0

    for month in range(1, n + 1):
        interest_component = balance * r
        principal_component = emi - interest_component
        balance -= principal_component
        total_interest_paid += interest_component
        total_principal_paid += principal_component

        if month <= max_rows or month == n or month % 12 == 0:
            schedule.append(
                {
                    "month": month,
                    "emi": round(emi, 2),
                    "principal": round(principal_component, 2),
                    "interest": round(interest_component, 2),
                    "balance": round(max(balance, 0), 2),
                    "total_interest_paid": round(total_interest_paid, 2),
                    "total_principal_paid": round(total_principal_paid, 2),
                }
            )

    return {
        "emi": round(emi, 2),
        "schedule": schedule,
        "total_interest": round(total_interest_paid, 2),
        "total_payment": round(emi * n, 2),
    }


def loan_comparison(loans: list[dict]) -> dict:
    """
    Compare multiple loan options.
    Each loan: {principal, annual_rate, tenure_years, name}
    """
    results = []
    for loan in loans:
        emi_result = calculate_emi(
            loan["principal"], loan["annual_rate"], loan["tenure_years"]
        )
        results.append(
            {
                "name": loan.get("name", f"Loan {len(results) + 1}"),
                "principal": loan["principal"],
                "rate": loan["annual_rate"],
                "tenure_years": loan["tenure_years"],
                "emi": emi_result["emi"],
                "total_interest": emi_result["total_interest"],
                "total_payment": emi_result["total_payment"],
                "interest_ratio": emi_result["interest_to_principal_ratio"],
            }
        )

    # Sort by total cost
    results.sort(key=lambda x: x["total_payment"])
    best = results[0]["name"]

    return {
        "comparison": results,
        "recommendation": f"'{best}' has the lowest total cost",
    }


def prepayment_impact(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    monthly_prepayment: float,
    lump_sum_prepayment: float = 0,
    lump_sum_month: int = 0,
) -> dict:
    """Calculate impact of prepaying a loan — savings in interest and time."""
    r = annual_rate / 100 / 12
    n = int(tenure_years * 12)

    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

    # Without prepayment
    total_without = emi * n
    interest_without = total_without - principal

    # With prepayment
    balance = principal
    months_with = 0
    total_paid = 0
    total_interest_with = 0

    for month in range(1, n * 2):  # safety limit
        if balance <= 0:
            break

        if month == lump_sum_month and lump_sum_prepayment > 0:
            balance -= lump_sum_prepayment
            total_paid += lump_sum_prepayment

        interest = balance * r
        total_interest_with += interest
        actual_payment = min(emi + monthly_prepayment, balance + interest)
        balance -= actual_payment - interest
        total_paid += actual_payment
        months_with += 1

        if balance <= 0.01:
            break

    interest_saved = interest_without - total_interest_with
    months_saved = n - months_with

    return {
        "original_tenure_months": n,
        "new_tenure_months": months_with,
        "months_saved": months_saved,
        "years_saved": round(months_saved / 12, 1),
        "emi": round(emi, 2),
        "interest_without_prepayment": round(interest_without, 2),
        "interest_with_prepayment": round(total_interest_with, 2),
        "interest_saved": round(interest_saved, 2),
        "total_saved": round(interest_saved, 2),
    }


def debt_consolidation_analysis(
    debts: list[dict], consolidated_rate: float, consolidated_tenure: float
) -> dict:
    """
    Analyze whether consolidating multiple debts makes sense.
    debts: [{name, balance, rate, emi}]
    """
    total_balance = sum(d["balance"] for d in debts)
    total_current_emi = sum(d["emi"] for d in debts)

    consolidated = calculate_emi(total_balance, consolidated_rate, consolidated_tenure)

    monthly_savings = total_current_emi - consolidated["emi"]

    return {
        "current_total_emi": round(total_current_emi, 2),
        "consolidated_emi": consolidated["emi"],
        "monthly_savings": round(monthly_savings, 2),
        "consolidated_total_interest": consolidated["total_interest"],
        "consolidated_total_payment": consolidated["total_payment"],
        "total_balance": total_balance,
        "debts": debts,
        "recommendation": "Consolidation saves money"
        if monthly_savings > 0
        else "Consolidation costs more",
    }


def invest_vs_prepay(
    loan_rate: float,
    investment_return: float,
    tax_bracket: float = 30,
    loan_tax_deduction: bool = True,
) -> dict:
    """
    Should you invest surplus money or prepay the loan?
    """
    effective_loan_rate = loan_rate
    if loan_tax_deduction:
        effective_loan_rate = loan_rate * (1 - tax_bracket / 100)

    post_tax_investment_return = investment_return * (1 - tax_bracket / 100)

    net_benefit = post_tax_investment_return - effective_loan_rate

    if net_benefit > 2:
        recommendation = "INVEST: Post-tax investment return significantly exceeds effective loan cost"
    elif net_benefit > 0:
        recommendation = "INVEST (marginal): Slight advantage to investing, but prepayment gives guaranteed savings"
    elif net_benefit > -2:
        recommendation = (
            "PREPAY (marginal): Slight advantage to prepaying, guarantees savings"
        )
    else:
        recommendation = "PREPAY: Effective loan cost significantly exceeds post-tax investment return"

    return {
        "loan_rate": loan_rate,
        "effective_loan_rate": round(effective_loan_rate, 2),
        "investment_return": investment_return,
        "post_tax_investment_return": round(post_tax_investment_return, 2),
        "net_benefit_of_investing": round(net_benefit, 2),
        "recommendation": recommendation,
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_emi")
    def calculate_emi_tool(
        principal: float,
        annual_rate: float,
        tenure_years: float,
    ) -> str:
        """Calculate EMI (Equated Monthly Instalment) for a loan.
        EMI = P × r × (1+r)^n / ((1+r)^n - 1).
        Also shows total interest paid and interest-to-principal ratio."""
        result = calculate_emi(principal, annual_rate, tenure_years)
        return format_tool_response("EMI Calculation", result)

    @mcp.tool(name="loan_amortization")
    def loan_amortization_tool(
        principal: float,
        annual_rate: float,
        tenure_years: float,
    ) -> str:
        """Generate loan amortization schedule showing month-wise principal/interest split.
        Shows how the interest component decreases and principal component increases over time."""
        result = loan_amortization_schedule(principal, annual_rate, tenure_years)
        output = format_tool_response(
            "Loan Amortization Schedule",
            {
                "emi": result["emi"],
                "total_interest": result["total_interest"],
                "total_payment": result["total_payment"],
            },
        )

        # Add schedule table
        output += "\n\n  Monthly Breakdown (key months):\n"
        output += f"  {'Month':>6} | {'EMI':>12} | {'Principal':>12} | {'Interest':>12} | {'Balance':>14}\n"
        output += f"  {'-' * 6}-+-{'-' * 12}-+-{'-' * 12}-+-{'-' * 12}-+-{'-' * 14}\n"
        for row in result["schedule"][:30]:
            output += (
                f"  {row['month']:>6} | ₹{row['emi']:>10,.2f} | "
                f"₹{row['principal']:>10,.2f} | ₹{row['interest']:>10,.2f} | "
                f"₹{row['balance']:>12,.2f}\n"
            )

        return output

    @mcp.tool(name="compare_loans")
    def compare_loans_tool(
        loans_json: str,
    ) -> str:
        """Compare multiple loan options to find the best deal.
        Input: JSON array of loans, each with: principal, annual_rate, tenure_years, name.
        Example: [{"principal": 5000000, "annual_rate": 8.5, "tenure_years": 20, "name": "Bank A"}]"""
        import json

        loans = json.loads(loans_json)
        result = loan_comparison(loans)
        output = format_tool_response(
            "Loan Comparison", {"recommendation": result["recommendation"]}
        )

        output += "\n\n"
        for loan in result["comparison"]:
            output += f"  {loan['name']}:\n"
            output += (
                f"    Rate: {loan['rate']}% | Tenure: {loan['tenure_years']} yrs\n"
            )
            output += f"    EMI: ₹{loan['emi']:,.2f} | Total Interest: ₹{loan['total_interest']:,.2f}\n"
            output += f"    Total Payment: ₹{loan['total_payment']:,.2f}\n\n"

        return output

    @mcp.tool(name="calculate_prepayment_savings")
    def calculate_prepayment_savings_tool(
        principal: float,
        annual_rate: float,
        tenure_years: float,
        monthly_prepayment: float = 0,
        lump_sum_prepayment: float = 0,
        lump_sum_month: int = 0,
    ) -> str:
        """Calculate how much you save by prepaying a loan (extra EMI or lump sum).
        Shows interest saved and tenure reduction."""
        result = prepayment_impact(
            principal,
            annual_rate,
            tenure_years,
            monthly_prepayment,
            lump_sum_prepayment,
            lump_sum_month,
        )
        return format_tool_response("Loan Prepayment Impact", result)

    @mcp.tool(name="invest_or_prepay_loan")
    def invest_or_prepay_loan_tool(
        loan_rate: float,
        investment_return: float,
        tax_bracket: float = 30,
        loan_has_tax_benefit: bool = True,
    ) -> str:
        """Should you invest surplus money or prepay an existing loan?
        Compares post-tax investment return vs effective loan cost."""
        result = invest_vs_prepay(
            loan_rate, investment_return, tax_bracket, loan_has_tax_benefit
        )
        return format_tool_response("Invest vs Prepay Analysis", result)

    @mcp.tool(name="analyze_debt_consolidation")
    def analyze_debt_consolidation_tool(
        debts_json: str,
        consolidated_rate: float,
        consolidated_tenure_years: float,
    ) -> str:
        """Analyze if consolidating multiple debts into one loan makes sense.
        Input debts_json: [{"name": "Credit Card", "balance": 100000, "rate": 36, "emi": 5000}]"""
        import json

        debts = json.loads(debts_json)
        result = debt_consolidation_analysis(
            debts, consolidated_rate, consolidated_tenure_years
        )
        return format_tool_response("Debt Consolidation Analysis", result)

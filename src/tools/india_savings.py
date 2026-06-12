"""
Indian Small Savings & Deposit Instruments

Deterministic maturity calculators for the popular government/bank schemes
commonly used in Indian personal finance: PPF, Sukanya Samriddhi, NSC, KVP,
SCSS, Recurring Deposit, Fixed Deposit and EPF.

All rates are entered as annual percentages.
"""


def ppf_maturity(annual_deposit: float, annual_rate: float, years: int = 15) -> dict:
    """Public Provident Fund: yearly deposit, annual compounding, deposit at start of year."""
    r = annual_rate / 100
    balance = 0.0
    total_deposited = 0.0
    for _ in range(years):
        balance = (balance + annual_deposit) * (1 + r)
        total_deposited += annual_deposit
    return {
        "maturity_value": round(balance, 2),
        "total_deposited": round(total_deposited, 2),
        "total_interest": round(balance - total_deposited, 2),
        "years": years,
        "annual_rate": annual_rate,
        "formula": "Each year: balance = (balance + deposit) × (1 + r)",
    }


def sukanya_samriddhi(
    annual_deposit: float,
    annual_rate: float,
    deposit_years: int = 15,
    maturity_years: int = 21,
) -> dict:
    """Sukanya Samriddhi Yojana: deposits for 15 yrs, matures in 21 yrs, annual compounding."""
    r = annual_rate / 100
    balance = 0.0
    total_deposited = 0.0
    for year in range(1, maturity_years + 1):
        if year <= deposit_years:
            balance += annual_deposit
            total_deposited += annual_deposit
        balance *= 1 + r
    return {
        "maturity_value": round(balance, 2),
        "total_deposited": round(total_deposited, 2),
        "total_interest": round(balance - total_deposited, 2),
        "deposit_years": deposit_years,
        "maturity_years": maturity_years,
        "formula": "Deposit for 15 yrs, compound annually until year 21",
    }


def nsc_maturity(principal: float, annual_rate: float, years: int = 5) -> dict:
    """National Savings Certificate: lump sum, annual compounding, interest reinvested."""
    r = annual_rate / 100
    maturity = principal * (1 + r) ** years
    return {
        "maturity_value": round(maturity, 2),
        "principal": principal,
        "total_interest": round(maturity - principal, 2),
        "years": years,
        "formula": f"M = P × (1+r)^t = {principal:,.2f} × (1+{r})^{years}",
    }


def kvp_maturity(principal: float, annual_rate: float) -> dict:
    """Kisan Vikas Patra: doubles money; tenure derived from the prevailing rate."""
    import math

    r = annual_rate / 100
    years_to_double = math.log(2) / math.log(1 + r)
    return {
        "maturity_value": round(principal * 2, 2),
        "principal": principal,
        "years_to_double": round(years_to_double, 2),
        "months_to_double": round(years_to_double * 12),
        "annual_rate": annual_rate,
        "formula": "Solve (1+r)^t = 2  →  t = ln2 / ln(1+r)",
    }


def scss_payout(principal: float, annual_rate: float, years: int = 5) -> dict:
    """Senior Citizens Savings Scheme: quarterly interest payout, principal returned at maturity."""
    quarterly_interest = principal * (annual_rate / 100) / 4
    annual_income = quarterly_interest * 4
    return {
        "quarterly_payout": round(quarterly_interest, 2),
        "annual_income": round(annual_income, 2),
        "total_interest": round(annual_income * years, 2),
        "principal_returned": principal,
        "years": years,
        "formula": "Quarterly payout = Principal × rate / 4 (simple, paid out each quarter)",
    }


def recurring_deposit(monthly_deposit: float, annual_rate: float, months: int) -> dict:
    """Recurring Deposit maturity using quarterly compounding convention."""
    # Standard RD: interest compounded quarterly; approximate with monthly annuity FV.
    i = annual_rate / 100 / 4  # quarterly rate
    maturity = 0.0
    total_deposited = monthly_deposit * months
    for m in range(1, months + 1):
        quarters_remaining = (months - m + 1) / 3
        maturity += monthly_deposit * (1 + i) ** quarters_remaining
    return {
        "maturity_value": round(maturity, 2),
        "total_deposited": round(total_deposited, 2),
        "total_interest": round(maturity - total_deposited, 2),
        "monthly_deposit": monthly_deposit,
        "months": months,
        "formula": "Sum of each installment compounded quarterly to maturity",
    }


def fixed_deposit(
    principal: float, annual_rate: float, years: float, compounding: str = "quarterly"
) -> dict:
    """Fixed Deposit maturity with selectable compounding frequency."""
    freq = {"annually": 1, "half_yearly": 2, "quarterly": 4, "monthly": 12}.get(
        compounding, 4
    )
    r = annual_rate / 100
    maturity = principal * (1 + r / freq) ** (freq * years)
    return {
        "maturity_value": round(maturity, 2),
        "principal": principal,
        "total_interest": round(maturity - principal, 2),
        "effective_yield": round(((maturity / principal) ** (1 / years) - 1) * 100, 4),
        "compounding": compounding,
        "formula": f"M = P × (1 + r/n)^(n×t), n={freq}",
    }


def epf_corpus(
    monthly_basic: float,
    annual_rate: float,
    years: float,
    employee_pct: float = 12.0,
    employer_pct: float = 3.67,
    annual_increment: float = 5.0,
) -> dict:
    """Employees' Provident Fund corpus with salary growth and monthly compounding."""
    r = annual_rate / 100 / 12
    g = annual_increment / 100
    basic = monthly_basic
    balance = 0.0
    total_contrib = 0.0
    months = int(years * 12)
    for m in range(months):
        if m > 0 and m % 12 == 0:
            basic *= 1 + g
        contribution = basic * (employee_pct + employer_pct) / 100
        balance = (balance + contribution) * (1 + r)
        total_contrib += contribution
    return {
        "epf_corpus": round(balance, 2),
        "total_contributed": round(total_contrib, 2),
        "total_interest": round(balance - total_contrib, 2),
        "years": years,
        "formula": "Monthly: balance = (balance + (employee%+employer%)×basic) × (1+r/12)",
    }


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_ppf")
    def calculate_ppf_tool(
        annual_deposit: float, annual_rate: float = 7.1, years: int = 15
    ) -> str:
        """PPF (Public Provident Fund) maturity value for a fixed yearly deposit.
        Use for 'how much will my PPF grow to', PPF maturity/corpus, tax-free
        long-term government savings. Annual compounding over (default) 15 years."""
        return format_tool_response("PPF Maturity", ppf_maturity(annual_deposit, annual_rate, years))

    @mcp.tool(name="calculate_sukanya_samriddhi")
    def calculate_ssy_tool(
        annual_deposit: float, annual_rate: float = 8.2,
        deposit_years: int = 15, maturity_years: int = 21,
    ) -> str:
        """Sukanya Samriddhi Yojana (SSY) maturity for a girl child.
        Use for daughter education/marriage savings, SSY corpus. Deposits for 15
        years, matures in 21 years, annual compounding."""
        return format_tool_response(
            "Sukanya Samriddhi Maturity",
            sukanya_samriddhi(annual_deposit, annual_rate, deposit_years, maturity_years),
        )

    @mcp.tool(name="calculate_nsc")
    def calculate_nsc_tool(principal: float, annual_rate: float = 7.7, years: int = 5) -> str:
        """NSC (National Savings Certificate) maturity. Lump-sum, interest reinvested,
        annual compounding (typically 5-year tenure)."""
        return format_tool_response("NSC Maturity", nsc_maturity(principal, annual_rate, years))

    @mcp.tool(name="calculate_kvp")
    def calculate_kvp_tool(principal: float, annual_rate: float = 7.5) -> str:
        """KVP (Kisan Vikas Patra) — doubles your money; returns the tenure required
        at the given interest rate. Use for 'how long to double my money in KVP'."""
        return format_tool_response("KVP Doubling", kvp_maturity(principal, annual_rate))

    @mcp.tool(name="calculate_scss")
    def calculate_scss_tool(principal: float, annual_rate: float = 8.2, years: int = 5) -> str:
        """SCSS (Senior Citizens Savings Scheme) — quarterly interest income and the
        principal returned at maturity. Use for retiree regular-income planning."""
        return format_tool_response("SCSS Income", scss_payout(principal, annual_rate, years))

    @mcp.tool(name="calculate_recurring_deposit")
    def calculate_rd_tool(monthly_deposit: float, annual_rate: float, months: int) -> str:
        """Recurring Deposit (RD) maturity for a fixed monthly deposit, quarterly
        compounding. Use for 'monthly bank RD maturity / interest'."""
        return format_tool_response(
            "Recurring Deposit Maturity",
            recurring_deposit(monthly_deposit, annual_rate, months),
        )

    @mcp.tool(name="calculate_fixed_deposit")
    def calculate_fd_tool(
        principal: float, annual_rate: float, years: float, compounding: str = "quarterly"
    ) -> str:
        """Fixed Deposit (FD) maturity and effective yield. compounding:
        annually | half_yearly | quarterly | monthly. Use for bank/NBFC FD maturity."""
        return format_tool_response(
            "Fixed Deposit Maturity", fixed_deposit(principal, annual_rate, years, compounding)
        )

    @mcp.tool(name="calculate_epf")
    def calculate_epf_tool(
        monthly_basic: float, annual_rate: float = 8.25, years: float = 30,
        employee_pct: float = 12.0, employer_pct: float = 3.67, annual_increment: float = 5.0,
    ) -> str:
        """EPF (Employees' Provident Fund) retirement corpus with salary growth.
        Use for 'how big will my EPF/PF be at retirement', employer+employee
        contributions compounding monthly."""
        return format_tool_response(
            "EPF Retirement Corpus",
            epf_corpus(monthly_basic, annual_rate, years, employee_pct, employer_pct, annual_increment),
        )

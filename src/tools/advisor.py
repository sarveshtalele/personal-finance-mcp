"""
Meta-Advisor Orchestrator
(NISM Level 1, Ch 1 Financial Planning Process; Ch 15 Portfolio Construction)

This is the bridge between a user's *story* and the deterministic calculators.
Instead of the user naming a tool, they describe their situation; the model fills
in a profile and calls `create_financial_plan`, which chains the relevant
calculators in the canonical financial-planning order:

    1. Evaluate position  (net worth, cash flow)
    2. Protect            (contingency fund, insurance)
    3. Manage debt        (debt-to-income)
    4. Profile risk       (suitability)
    5. Invest for goals   (retirement & goal SIPs)

and returns a single prioritised action plan.
"""

from .planning import calculate_net_worth, emergency_fund_calculator
from .cashflow import cash_flow_statement, debt_to_income
from .risk_profile import risk_profile_score
from .mutual_funds import sip_required_for_target


def create_financial_plan(
    age: int,
    monthly_income: float,
    monthly_expenses: float,
    monthly_emi: float = 0.0,
    dependents: int = 0,
    existing_emergency_fund: float = 0.0,
    assets: dict[str, float] | None = None,
    liabilities: dict[str, float] | None = None,
    retirement_age: int = 60,
    current_retirement_corpus: float = 0.0,
    expected_return: float = 11.0,
    inflation: float = 6.0,
    life_expectancy: int = 85,
) -> dict:
    """Run the full planning battery and produce a prioritised action plan."""
    assets = assets or {}
    liabilities = liabilities or {}
    plan: dict = {}
    actions: list[str] = []

    # 1. Net worth ----------------------------------------------------------
    if assets or liabilities:
        nw = calculate_net_worth(assets, liabilities)
        plan["net_worth"] = nw["net_worth"]

    # 2. Cash flow ----------------------------------------------------------
    fixed = monthly_expenses
    cf = cash_flow_statement(monthly_income, fixed, 0.0, monthly_emi)
    plan["monthly_surplus"] = cf["monthly_surplus"]
    plan["savings_rate_pct"] = cf["savings_rate"]
    if cf["monthly_surplus"] <= 0:
        actions.append(
            "URGENT: You are running a cash-flow deficit — cut variable spending "
            "before any investing."
        )
    elif cf["savings_rate"] < 20:
        actions.append(
            f"Lift your savings rate from {cf['savings_rate']:.0f}% toward 20%+ "
            "to fund goals faster."
        )

    # 3. Contingency fund ---------------------------------------------------
    ef = emergency_fund_calculator(
        monthly_expenses, monthly_emi, dependents,
        "stable", existing_emergency_fund,
    )
    plan["emergency_fund_target"] = ef["recommended_fund"]
    plan["emergency_fund_gap"] = ef["gap"]
    if ef["gap"] > 0:
        actions.append(
            f"Build an emergency fund of ₹{ef['recommended_fund']:,.0f} "
            f"(shortfall ₹{ef['gap']:,.0f}) before locking money into investments."
        )

    # 4. Debt servicing -----------------------------------------------------
    if monthly_emi > 0:
        dti = debt_to_income(monthly_emi, monthly_income)
        plan["debt_to_income_pct"] = dti["debt_to_income_ratio"]
        if dti["debt_to_income_ratio"] > 40:
            actions.append(
                f"Debt-to-income is {dti['debt_to_income_ratio']:.0f}% (>40%). "
                "Prioritise paying down high-cost debt before new commitments."
            )

    # 5. Risk profile -------------------------------------------------------
    horizon = max(retirement_age - age, 1)
    rp = risk_profile_score(
        age=age, horizon_years=horizon,
        income_stability=4, investment_knowledge=3,
        loss_reaction=3, dependents=dependents,
    )
    plan["risk_profile"] = rp["risk_profile"]
    plan["suggested_equity_pct"] = rp["suggested_equity_pct"]

    # 6. Retirement gap -----------------------------------------------------
    years_to_retire = max(retirement_age - age, 1)
    years_in_retirement = max(life_expectancy - retirement_age, 1)
    real_rate = (1 + expected_return / 100) / (1 + inflation / 100) - 1
    annual_expense_at_retirement = (
        monthly_expenses * 12 * (1 + inflation / 100) ** years_to_retire
    )
    # Corpus needed (real annuity present value at retirement)
    if real_rate != 0:
        corpus_needed = annual_expense_at_retirement * (
            (1 - (1 + real_rate) ** (-years_in_retirement)) / real_rate
        )
    else:
        corpus_needed = annual_expense_at_retirement * years_in_retirement
    fv_current = current_retirement_corpus * (1 + expected_return / 100) ** years_to_retire
    gap = max(corpus_needed - fv_current, 0)
    plan["retirement_corpus_needed"] = round(corpus_needed, 2)
    plan["retirement_corpus_gap"] = round(gap, 2)
    if gap > 0:
        sip = sip_required_for_target(gap, expected_return, years_to_retire)
        plan["retirement_monthly_sip"] = sip["monthly_sip_needed"]
        affordable = sip["monthly_sip_needed"] <= max(cf["monthly_surplus"], 0)
        actions.append(
            f"For retirement, invest ~₹{sip['monthly_sip_needed']:,.0f}/month "
            f"({'within' if affordable else 'ABOVE'} your current surplus) at "
            f"{rp['suggested_equity_pct']}% equity."
        )

    plan["prioritised_actions"] = actions or ["You are on track across the basics — review annually."]
    plan["planning_order"] = "Evaluate → Protect → Reduce debt → Profile risk → Invest for goals"
    return plan


# ruff: noqa: E402
from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="create_financial_plan")
    def create_financial_plan_tool(
        age: int,
        monthly_income: float,
        monthly_expenses: float,
        monthly_emi: float = 0.0,
        dependents: int = 0,
        existing_emergency_fund: float = 0.0,
        retirement_age: int = 60,
        current_retirement_corpus: float = 0.0,
        expected_return: float = 11.0,
        inflation: float = 6.0,
        life_expectancy: int = 85,
    ) -> str:
        """Holistic financial plan from a user's life situation — the best first tool
        when someone describes their finances in plain language ('I'm 30, earn X,
        spend Y, have a home loan, want to retire at 60'). It chains net worth,
        cash flow, emergency fund, debt-to-income, risk profiling and a retirement
        gap into ONE prioritised action plan, in the canonical financial-planning
        order (evaluate → protect → reduce debt → profile risk → invest for goals).
        Call this to bridge a free-form story to concrete numbers, then drill into
        specific calculators (SIP, retirement, loans) for detail."""
        result = create_financial_plan(
            age=age, monthly_income=monthly_income, monthly_expenses=monthly_expenses,
            monthly_emi=monthly_emi, dependents=dependents,
            existing_emergency_fund=existing_emergency_fund,
            retirement_age=retirement_age,
            current_retirement_corpus=current_retirement_corpus,
            expected_return=expected_return, inflation=inflation,
            life_expectancy=life_expectancy,
        )
        return format_tool_response("Your Financial Plan", result)

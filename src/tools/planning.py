from .tvm import inflation_adjusted_amount, required_monthly_savings

"""
Financial Ratios and Position Analysis

Key ratios:
  Savings Ratio = Savings / Gross Income
  Debt-to-Income = Total Monthly Debt Payments / Gross Monthly Income
  Liquidity Ratio = Liquid Assets / Monthly Expenses
  Solvency Ratio = Net Worth / Total Assets
  Debt-to-Asset = Total Liabilities / Total Assets
  Financial Assets Ratio = Financial Assets / Total Assets
"""


def calculate_net_worth(
    assets: dict[str, float], liabilities: dict[str, float]
) -> dict:
    """Calculate net worth = Total Assets - Total Liabilities."""
    total_assets = sum(assets.values())
    total_liabilities = sum(liabilities.values())
    net_worth = total_assets - total_liabilities

    return {
        "total_assets": round(total_assets, 2),
        "total_liabilities": round(total_liabilities, 2),
        "net_worth": round(net_worth, 2),
        "assets_breakdown": {
            k: round(v, 2) for k, v in sorted(assets.items(), key=lambda x: -x[1])
        },
        "liabilities_breakdown": {
            k: round(v, 2) for k, v in sorted(liabilities.items(), key=lambda x: -x[1])
        },
        "debt_to_asset_ratio": round(total_liabilities / total_assets, 4)
        if total_assets > 0
        else 0,
        "solvency_ratio": round(net_worth / total_assets, 4) if total_assets > 0 else 0,
    }


def calculate_financial_ratios(
    monthly_income: float,
    monthly_expenses: float,
    monthly_emis: float,
    monthly_savings: float,
    total_assets: float,
    total_liabilities: float,
    liquid_assets: float,
) -> dict:
    """Calculate all key financial ratios from Core Financial Principles."""
    savings_ratio = monthly_savings / monthly_income if monthly_income > 0 else 0
    dti_ratio = monthly_emis / monthly_income if monthly_income > 0 else 0
    expense_ratio = monthly_expenses / monthly_income if monthly_income > 0 else 0
    liquidity_ratio = liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
    net_worth = total_assets - total_liabilities
    solvency_ratio = net_worth / total_assets if total_assets > 0 else 0
    debt_to_asset = total_liabilities / total_assets if total_assets > 0 else 0

    # Assessments based on standard financial guidelines
    assessments = {}
    assessments["savings_ratio"] = (
        "Healthy (>=20%)"
        if savings_ratio >= 0.20
        else "Adequate (10-20%)"
        if savings_ratio >= 0.10
        else "Low (<10%) - needs improvement"
    )
    assessments["debt_to_income"] = (
        "Healthy (<30%)"
        if dti_ratio < 0.30
        else "Caution (30-40%)"
        if dti_ratio < 0.40
        else "Danger (>40%) - over-leveraged"
    )
    assessments["liquidity"] = (
        "Strong (>6 months)"
        if liquidity_ratio > 6
        else "Adequate (3-6 months)"
        if liquidity_ratio >= 3
        else "Weak (<3 months) - build emergency fund"
    )
    assessments["solvency"] = (
        "Strong (>0.5)"
        if solvency_ratio > 0.5
        else "Adequate (0.2-0.5)"
        if solvency_ratio >= 0.2
        else "Weak (<0.2) - high debt burden"
    )

    return {
        "savings_ratio": round(savings_ratio * 100, 2),
        "debt_to_income_ratio": round(dti_ratio * 100, 2),
        "expense_ratio": round(expense_ratio * 100, 2),
        "liquidity_ratio": round(liquidity_ratio, 2),
        "solvency_ratio": round(solvency_ratio * 100, 2),
        "debt_to_asset_ratio": round(debt_to_asset * 100, 2),
        "net_worth": round(net_worth, 2),
        "assessments": assessments,
    }


def emergency_fund_calculator(
    monthly_expenses: float,
    monthly_emis: float,
    dependents: int = 0,
    job_stability: str = "stable",
    existing_emergency_fund: float = 0,
) -> dict:
    """
    Calculate recommended emergency fund.
    Core principles recommend 3-6 months of expenses.
    Adjusted for dependents and job stability.
    """
    base_monthly = monthly_expenses + monthly_emis

    # Determine months of coverage needed
    if job_stability == "unstable":
        months_needed = 9
    elif job_stability == "moderate":
        months_needed = 6
    else:
        months_needed = 3

    # Add 1 month per dependent beyond 2
    if dependents > 2:
        months_needed += dependents - 2

    recommended = base_monthly * months_needed
    gap = recommended - existing_emergency_fund
    coverage_months = existing_emergency_fund / base_monthly if base_monthly > 0 else 0

    return {
        "monthly_need": round(base_monthly, 2),
        "months_coverage_recommended": months_needed,
        "recommended_fund": round(recommended, 2),
        "existing_fund": round(existing_emergency_fund, 2),
        "gap": round(max(gap, 0), 2),
        "current_coverage_months": round(coverage_months, 1),
        "status": "Adequate" if gap <= 0 else f"Shortfall of ₹{max(gap, 0):,.2f}",
    }


def budget_analysis(
    monthly_income: float,
    expenses: dict[str, float],
    existing_emis: float = 0,
    existing_sips: float = 0,
) -> dict:
    """
    Analyze household budget using 50/30/20 rule and standard financial guidelines.
    50% Needs | 30% Wants | 20% Savings
    """
    total_expenses = sum(expenses.values())
    total_outflow = total_expenses + existing_emis + existing_sips
    surplus = monthly_income - total_outflow
    savings_rate = (
        (existing_sips + max(surplus, 0)) / monthly_income if monthly_income > 0 else 0
    )

    # 50/30/20 benchmarks
    needs_benchmark = monthly_income * 0.50
    wants_benchmark = monthly_income * 0.30
    savings_benchmark = monthly_income * 0.20

    # Categorize expenses (simplified)
    needs_keywords = {
        "rent",
        "food",
        "grocery",
        "groceries",
        "utilities",
        "insurance",
        "medical",
        "health",
        "transport",
        "fuel",
        "electricity",
        "water",
        "gas",
    }
    wants_keywords = {
        "entertainment",
        "dining",
        "shopping",
        "travel",
        "subscription",
        "hobby",
        "gym",
        "movies",
        "eating_out",
    }

    needs_total = sum(v for k, v in expenses.items() if k.lower() in needs_keywords)
    wants_total = sum(v for k, v in expenses.items() if k.lower() in wants_keywords)
    other_total = total_expenses - needs_total - wants_total

    return {
        "monthly_income": round(monthly_income, 2),
        "total_expenses": round(total_expenses, 2),
        "total_emis": round(existing_emis, 2),
        "total_sips": round(existing_sips, 2),
        "total_outflow": round(total_outflow, 2),
        "surplus": round(surplus, 2),
        "savings_rate": round(savings_rate * 100, 2),
        "expense_breakdown": {
            k: round(v, 2) for k, v in sorted(expenses.items(), key=lambda x: -x[1])
        },
        "category_analysis": {
            "needs": round(needs_total, 2),
            "wants": round(wants_total, 2),
            "other": round(other_total, 2),
        },
        "benchmarks_50_30_20": {
            "needs_benchmark": round(needs_benchmark, 2),
            "wants_benchmark": round(wants_benchmark, 2),
            "savings_benchmark": round(savings_benchmark, 2),
            "needs_status": "Within limit"
            if needs_total <= needs_benchmark
            else "Over budget",
            "wants_status": "Within limit"
            if wants_total <= wants_benchmark
            else "Over budget",
            "savings_status": "On track" if savings_rate >= 0.20 else "Below target",
        },
    }


def financial_health_score(
    monthly_income: float,
    monthly_expenses: float,
    total_assets: float,
    total_liabilities: float,
    liquid_assets: float,
    monthly_emis: float,
    monthly_savings: float,
    emergency_fund: float,
    insurance_cover: float,
    age: int,
) -> dict:
    """
    Comprehensive financial health score (0-100).
    Based on Core Financial Principles evaluation criteria.
    """
    score = 0
    breakdown = {}
    recommendations = []

    # 1. Savings Ratio (max 15 points)
    savings_ratio = monthly_savings / monthly_income if monthly_income > 0 else 0
    if savings_ratio >= 0.30:
        s = 15
    elif savings_ratio >= 0.20:
        s = 12
    elif savings_ratio >= 0.10:
        s = 8
    else:
        s = 3
        recommendations.append("Increase savings rate to at least 20% of income")
    breakdown["savings_ratio"] = {
        "score": s,
        "max": 15,
        "value": f"{savings_ratio * 100:.1f}%",
    }
    score += s

    # 2. Debt-to-Income (max 15 points)
    dti = monthly_emis / monthly_income if monthly_income > 0 else 0
    if dti == 0:
        s = 15
    elif dti < 0.20:
        s = 13
    elif dti < 0.30:
        s = 10
    elif dti < 0.40:
        s = 5
    else:
        s = 2
        recommendations.append("Reduce debt obligations - DTI ratio is too high (>40%)")
    breakdown["debt_to_income"] = {"score": s, "max": 15, "value": f"{dti * 100:.1f}%"}
    score += s

    # 3. Emergency Fund (max 15 points)
    ef_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
    if ef_months >= 6:
        s = 15
    elif ef_months >= 3:
        s = 10
    elif ef_months >= 1:
        s = 5
    else:
        s = 1
        recommendations.append(
            "Build emergency fund covering at least 3-6 months of expenses"
        )
    breakdown["emergency_fund"] = {
        "score": s,
        "max": 15,
        "value": f"{ef_months:.1f} months",
    }
    score += s

    # 4. Net Worth Positive (max 15 points)
    net_worth = total_assets - total_liabilities
    nw_ratio = net_worth / total_assets if total_assets > 0 else 0
    if nw_ratio > 0.7:
        s = 15
    elif nw_ratio > 0.5:
        s = 12
    elif nw_ratio > 0.2:
        s = 8
    elif nw_ratio > 0:
        s = 4
    else:
        s = 0
        recommendations.append("Net worth is negative - focus on debt reduction")
    breakdown["net_worth"] = {"score": s, "max": 15, "value": f"₹{net_worth:,.0f}"}
    score += s

    # 5. Insurance Coverage (max 10 points)
    income_multiple = (
        insurance_cover / (monthly_income * 12) if monthly_income > 0 else 0
    )
    if income_multiple >= 10:
        s = 10
    elif income_multiple >= 5:
        s = 7
    elif income_multiple >= 2:
        s = 4
    else:
        s = 1
        recommendations.append(
            "Increase life insurance cover to at least 10x annual income"
        )
    breakdown["insurance"] = {
        "score": s,
        "max": 10,
        "value": f"{income_multiple:.1f}x annual income",
    }
    score += s

    # 6. Liquidity (max 10 points)
    liquidity = liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
    if liquidity > 6:
        s = 10
    elif liquidity > 3:
        s = 7
    elif liquidity > 1:
        s = 4
    else:
        s = 1
    breakdown["liquidity"] = {"score": s, "max": 10, "value": f"{liquidity:.1f} months"}
    score += s

    # 7. Expense Ratio (max 10 points)
    exp_ratio = monthly_expenses / monthly_income if monthly_income > 0 else 1
    if exp_ratio < 0.50:
        s = 10
    elif exp_ratio < 0.60:
        s = 8
    elif exp_ratio < 0.70:
        s = 5
    else:
        s = 2
        recommendations.append(
            "Reduce discretionary expenses to improve savings capacity"
        )
    breakdown["expense_ratio"] = {
        "score": s,
        "max": 10,
        "value": f"{exp_ratio * 100:.1f}%",
    }
    score += s

    # 8. Age-appropriate wealth (max 10 points)
    # Rule of thumb: net worth should be ~(age × annual_income / 10)
    expected_nw = age * monthly_income * 12 / 10
    if expected_nw > 0:
        nw_achievement = net_worth / expected_nw
    else:
        nw_achievement = 0

    if nw_achievement >= 1.0:
        s = 10
    elif nw_achievement >= 0.5:
        s = 7
    elif nw_achievement >= 0.25:
        s = 4
    else:
        s = 1
        recommendations.append(
            "Wealth accumulation is below age-appropriate benchmarks - increase investments"
        )
    breakdown["age_appropriate_wealth"] = {
        "score": s,
        "max": 10,
        "value": f"{nw_achievement * 100:.0f}% of benchmark",
    }
    score += s

    # Rating
    if score >= 80:
        rating = "Excellent"
    elif score >= 60:
        rating = "Good"
    elif score >= 40:
        rating = "Fair"
    elif score >= 20:
        rating = "Needs Improvement"
    else:
        rating = "Critical"

    return {
        "total_score": score,
        "max_score": 100,
        "rating": rating,
        "breakdown": breakdown,
        "recommendations": recommendations,
    }


from mcp.server.fastmcp import FastMCP
from ..utils.formatters import format_tool_response


def register(mcp: FastMCP):

    @mcp.tool(name="calculate_net_worth")
    def calculate_net_worth_tool(
        assets_json: str,
        liabilities_json: str,
    ) -> str:
        """Calculate net worth from assets and liabilities.
        Input JSON maps of name:value pairs.
        Example assets: {"house": 5000000, "stocks": 200000, "fd": 300000}
        Example liabilities: {"home_loan": 3000000, "car_loan": 500000}"""
        import json

        assets = json.loads(assets_json)
        liabilities = json.loads(liabilities_json)
        result = calculate_net_worth(assets, liabilities)
        return format_tool_response("Net Worth Statement", result)

    @mcp.tool(name="analyze_financial_ratios")
    def analyze_financial_ratios_tool(
        monthly_income: float,
        monthly_expenses: float,
        monthly_emis: float,
        monthly_savings: float,
        total_assets: float,
        total_liabilities: float,
        liquid_assets: float,
    ) -> str:
        """Calculate all key financial health ratios: Savings ratio, Debt-to-Income,
        Liquidity ratio, Solvency ratio, Expense ratio. Includes assessments and benchmarks."""
        result = calculate_financial_ratios(
            monthly_income,
            monthly_expenses,
            monthly_emis,
            monthly_savings,
            total_assets,
            total_liabilities,
            liquid_assets,
        )
        return format_tool_response("Financial Ratios Analysis", result)

    @mcp.tool(name="calculate_emergency_fund")
    def calculate_emergency_fund_tool(
        monthly_expenses: float,
        monthly_emis: float = 0,
        dependents: int = 0,
        job_stability: str = "stable",
        existing_emergency_fund: float = 0,
    ) -> str:
        """Calculate recommended emergency fund size (3-6 months of expenses).
        Adjusts for dependents and job stability. job_stability: stable, moderate, unstable."""
        result = emergency_fund_calculator(
            monthly_expenses,
            monthly_emis,
            dependents,
            job_stability,
            existing_emergency_fund,
        )
        return format_tool_response("Emergency Fund Calculator", result)

    @mcp.tool(name="analyze_budget")
    def analyze_budget_tool(
        monthly_income: float,
        expenses_json: str,
        existing_emis: float = 0,
        existing_sips: float = 0,
    ) -> str:
        """Analyze household budget using the 50/30/20 rule.
        50% Needs | 30% Wants | 20% Savings.
        expenses_json: {"rent": 20000, "food": 10000, "entertainment": 5000}"""
        import json

        expenses = json.loads(expenses_json)
        result = budget_analysis(monthly_income, expenses, existing_emis, existing_sips)
        return format_tool_response("Budget Analysis (50/30/20 Rule)", result)

    @mcp.tool(name="plan_financial_goal")
    def plan_financial_goal_tool(
        goal_name: str,
        target_amount_today: float,
        years_to_goal: float,
        inflation_rate: float = 6.0,
        expected_return: float = 12.0,
        current_savings: float = 0,
    ) -> str:
        """Plan for a financial goal (education, house, car, wedding, etc.).
        Adjusts target for inflation, calculates monthly SIP needed."""
        # Inflate target
        inflated = inflation_adjusted_amount(
            target_amount_today, inflation_rate, years_to_goal
        )
        inflation_adjusted_target = inflated["future_amount"]

        # Calculate monthly savings needed
        savings = required_monthly_savings(
            inflation_adjusted_target, expected_return, years_to_goal, current_savings
        )

        output = f"""
══════════════════════════════════════════════════
  Financial Goal Planner: {goal_name}
══════════════════════════════════════════════════

  Goal Details:
    Target (today's value): ₹{target_amount_today:,.2f}
    Inflation Rate: {inflation_rate}% p.a.
    Years to Goal: {years_to_goal}
    Inflation-Adjusted Target: ₹{inflation_adjusted_target:,.2f}

  Investment Plan:
    Expected Return: {expected_return}% p.a.
    Current Savings for Goal: ₹{current_savings:,.2f}
    FV of Current Savings: ₹{savings["future_value_of_current_savings"]:,.2f}
    Monthly SIP Needed: ₹{savings["monthly_savings_needed"]:,.2f}

  Summary:
    Total Investment: ₹{savings["total_invested"]:,.2f}
    Wealth Gained: ₹{savings["wealth_gained"]:,.2f}

  Formula:
    {savings["formula"]}

"""
        return output

    @mcp.tool(name="plan_retirement")
    def plan_retirement_tool(
        current_age: int,
        retirement_age: int,
        life_expectancy: int,
        monthly_expenses: float,
        inflation_rate: float = 6.0,
        pre_retirement_return: float = 12.0,
        post_retirement_return: float = 8.0,
        current_retirement_savings: float = 0,
        monthly_pension: float = 0,
    ) -> str:
        """Comprehensive retirement planning calculator.
        Calculates: corpus needed at retirement, monthly SIP needed,
        accounts for inflation on expenses and pension shortfall."""
        years_to_retire = retirement_age - current_age
        retirement_years = life_expectancy - retirement_age

        # Step 1: Monthly expenses at retirement (inflated)
        inflated = inflation_adjusted_amount(
            monthly_expenses, inflation_rate, years_to_retire
        )
        expenses_at_retirement = inflated["future_amount"]
        net_monthly_need = expenses_at_retirement - monthly_pension

        if net_monthly_need <= 0:
            return "Pension covers all expenses — no additional corpus needed!"

        # Step 2: Corpus needed at retirement (PV of annuity for retirement years)
        # Using real return during retirement
        real_post_ret = (
            (1 + post_retirement_return / 100) / (1 + inflation_rate / 100) - 1
        ) * 100
        if real_post_ret <= 0:
            corpus_needed = net_monthly_need * 12 * retirement_years
        else:
            r = real_post_ret / 100 / 12
            n = retirement_years * 12
            corpus_needed = net_monthly_need * ((1 - (1 + r) ** (-n)) / r)

        # Step 3: Monthly SIP to build corpus
        savings = required_monthly_savings(
            corpus_needed,
            pre_retirement_return,
            years_to_retire,
            current_retirement_savings,
        )

        output = f"""
══════════════════════════════════════════════════
  Retirement Plan
══════════════════════════════════════════════════

  Profile:
    Current Age: {current_age} | Retirement Age: {retirement_age}
    Life Expectancy: {life_expectancy}
    Years to Retirement: {years_to_retire}
    Retirement Duration: {retirement_years} years

  Expense Projection:
    Current Monthly Expenses: ₹{monthly_expenses:,.2f}
    Expenses at Retirement: ₹{expenses_at_retirement:,.2f}
    Monthly Pension: ₹{monthly_pension:,.2f}
    Net Monthly Need: ₹{net_monthly_need:,.2f}

  Corpus Calculation:
    Real Post-Retirement Return: {real_post_ret:.2f}%
    Corpus Needed at Retirement: ₹{corpus_needed:,.2f}

  Investment Plan:
    Current Retirement Savings: ₹{current_retirement_savings:,.2f}
    Pre-Retirement Return: {pre_retirement_return}%
    Monthly SIP Needed: ₹{savings["monthly_savings_needed"]:,.2f}
    Total Investment: ₹{savings["total_invested"]:,.2f}
    Wealth Gained: ₹{savings["wealth_gained"]:,.2f}

"""
        return output

    @mcp.tool(name="plan_education")
    def plan_education_tool(
        child_current_age: int,
        education_start_age: int,
        current_education_cost: float,
        inflation_rate: float = 8.0,
        expected_return: float = 12.0,
        current_savings: float = 0,
    ) -> str:
        """Plan for child's education expense.
        Adjusts cost for education inflation (typically higher than CPI).
        Calculates monthly SIP needed."""
        years_to_goal = education_start_age - child_current_age

        inflated = inflation_adjusted_amount(
            current_education_cost, inflation_rate, years_to_goal
        )
        target = inflated["future_amount"]

        savings = required_monthly_savings(
            target, expected_return, years_to_goal, current_savings
        )

        output = f"""
══════════════════════════════════════════════════
  Education Fund Planner
══════════════════════════════════════════════════

  Child's Current Age: {child_current_age}
  Education Starts At: {education_start_age}
  Years to Goal: {years_to_goal}

  Cost Projection:
    Current Cost: ₹{current_education_cost:,.2f}
    Education Inflation: {inflation_rate}% p.a.
    Projected Cost: ₹{target:,.2f}

  Investment Plan:
    Expected Return: {expected_return}%
    Current Savings: ₹{current_savings:,.2f}
    Monthly SIP Needed: ₹{savings["monthly_savings_needed"]:,.2f}
    Total Investment: ₹{savings["total_invested"]:,.2f}

"""
        return output

    @mcp.tool(name="calculate_insurance_need")
    def calculate_insurance_need_tool(
        annual_income: float,
        years_of_income_to_replace: int,
        outstanding_loans: float = 0,
        future_goals_corpus: float = 0,
        existing_insurance: float = 0,
        existing_investments: float = 0,
    ) -> str:
        """Calculate life insurance need using Human Life Value (HLV) method.
        HLV = PV of future earnings + Outstanding loans + Future goals - Existing cover."""
        # HLV approach
        discount_rate = 0.06
        pv_income = 0
        for yr in range(1, years_of_income_to_replace + 1):
            pv_income += annual_income / (1 + discount_rate) ** yr

        total_need = pv_income + outstanding_loans + future_goals_corpus
        existing_cover = existing_insurance + existing_investments
        gap = total_need - existing_cover

        output = f"""
══════════════════════════════════════════════════
  Insurance Needs Analysis (HLV Method)
══════════════════════════════════════════════════

  Income Replacement:
    Annual Income: ₹{annual_income:,.2f}
    Years to Replace: {years_of_income_to_replace}
    PV of Future Income: ₹{pv_income:,.2f}

  Additional Needs:
    Outstanding Loans: ₹{outstanding_loans:,.2f}
    Future Goals Corpus: ₹{future_goals_corpus:,.2f}

  Total Insurance Need: ₹{total_need:,.2f}

  Existing Cover:
    Insurance: ₹{existing_insurance:,.2f}
    Investments: ₹{existing_investments:,.2f}
    Total Existing: ₹{existing_cover:,.2f}

  Insurance Gap: ₹{max(gap, 0):,.2f}

  Recommendation: {"Adequate cover" if gap <= 0 else f"Buy additional cover of ₹{gap:,.2f}"}

"""
        return output

    @mcp.tool(name="financial_health_check")
    def financial_health_check_tool(
        monthly_income: float,
        monthly_expenses: float,
        total_assets: float,
        total_liabilities: float,
        liquid_assets: float,
        monthly_emis: float,
        monthly_savings: float,
        emergency_fund: float,
        insurance_cover: float,
        age: int,
    ) -> str:
        """Comprehensive financial health score (0-100) with rating and recommendations.
        Evaluates: savings ratio, debt levels, emergency fund, net worth,
        insurance, liquidity, expense ratio, age-appropriate wealth."""
        result = financial_health_score(
            monthly_income,
            monthly_expenses,
            total_assets,
            total_liabilities,
            liquid_assets,
            monthly_emis,
            monthly_savings,
            emergency_fund,
            insurance_cover,
            age,
        )

        output = f"""
══════════════════════════════════════════════════
  Financial Health Check
══════════════════════════════════════════════════

  Overall Score: {result["total_score"]}/{result["max_score"]}
  Rating: {result["rating"]}

  Breakdown:
"""
        for category, details in result["breakdown"].items():
            display = category.replace("_", " ").title()
            output += f"    {display}: {details['score']}/{details['max']} ({details['value']})\n"

        if result["recommendations"]:
            output += "\n  Recommendations:\n"
            for i, rec in enumerate(result["recommendations"], 1):
                output += f"    {i}. {rec}\n"

        return output

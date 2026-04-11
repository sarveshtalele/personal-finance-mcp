from pydantic import BaseModel, Field
from typing import Optional
from .enums import CompoundingFrequency, AnnuityType


class TVMInput(BaseModel):
    present_value: Optional[float] = Field(
        None, description="Present value (lump sum today)"
    )
    future_value: Optional[float] = Field(
        None, description="Future value (target amount)"
    )
    rate: float = Field(
        ..., description="Annual interest rate in percentage (e.g., 12 for 12%)"
    )
    periods: float = Field(..., description="Number of years")
    compounding: CompoundingFrequency = Field(
        CompoundingFrequency.ANNUALLY, description="Compounding frequency"
    )


class AnnuityInput(BaseModel):
    payment: Optional[float] = Field(None, description="Periodic payment amount")
    present_value: Optional[float] = Field(None, description="Present value of annuity")
    future_value: Optional[float] = Field(None, description="Future value of annuity")
    rate: float = Field(..., description="Annual interest rate in percentage")
    periods: float = Field(..., description="Number of years")
    compounding: CompoundingFrequency = Field(CompoundingFrequency.MONTHLY)
    annuity_type: AnnuityType = Field(AnnuityType.ORDINARY)


class LoanInput(BaseModel):
    principal: float = Field(..., description="Loan principal amount")
    annual_rate: float = Field(..., description="Annual interest rate in percentage")
    tenure_years: float = Field(..., description="Loan tenure in years")
    prepayment: Optional[float] = Field(None, description="Monthly prepayment amount")


class GoalInput(BaseModel):
    goal_name: str = Field(..., description="Name of the financial goal")
    target_amount: float = Field(
        ..., description="Target amount needed (today's value)"
    )
    years_to_goal: float = Field(..., description="Years until the goal")
    inflation_rate: float = Field(6.0, description="Expected inflation rate (%)")
    expected_return: float = Field(12.0, description="Expected investment return (%)")
    current_savings: float = Field(0, description="Amount already saved for this goal")


class NetWorthInput(BaseModel):
    assets: dict[str, float] = Field(
        ...,
        description="Assets with name:value pairs (e.g., {'house': 5000000, 'fd': 200000})",
    )
    liabilities: dict[str, float] = Field(
        ...,
        description="Liabilities with name:value pairs (e.g., {'home_loan': 3000000})",
    )


class BudgetInput(BaseModel):
    monthly_income: float = Field(..., description="Total monthly income")
    expenses: dict[str, float] = Field(
        ...,
        description="Monthly expenses by category (e.g., {'rent': 20000, 'food': 10000})",
    )
    existing_emis: float = Field(0, description="Total existing EMI payments")
    existing_sips: float = Field(0, description="Total existing SIP investments")


class BondInput(BaseModel):
    face_value: float = Field(1000, description="Face/par value of bond")
    coupon_rate: float = Field(..., description="Annual coupon rate in percentage")
    ytm: Optional[float] = Field(None, description="Yield to maturity in percentage")
    market_price: Optional[float] = Field(None, description="Current market price")
    years_to_maturity: float = Field(..., description="Years remaining to maturity")
    coupon_frequency: int = Field(
        2, description="Coupon payments per year (1=annual, 2=semi-annual)"
    )


class StockValuationInput(BaseModel):
    current_dividend: Optional[float] = Field(
        None, description="Current annual dividend per share"
    )
    growth_rate: float = Field(..., description="Expected dividend growth rate (%)")
    required_return: float = Field(..., description="Required rate of return (%)")
    earnings_per_share: Optional[float] = Field(
        None, description="EPS for P/E valuation"
    )
    industry_pe: Optional[float] = Field(None, description="Industry average P/E ratio")
    free_cash_flows: Optional[list[float]] = Field(
        None, description="Projected FCFs for DCF"
    )
    terminal_growth: Optional[float] = Field(
        None, description="Terminal growth rate for DCF (%)"
    )


class PortfolioAsset(BaseModel):
    name: str
    weight: float = Field(
        ..., description="Weight in portfolio (as decimal, e.g., 0.6 for 60%)"
    )
    expected_return: float = Field(..., description="Expected annual return (%)")
    std_dev: float = Field(..., description="Standard deviation of returns (%)")


class PortfolioInput(BaseModel):
    assets: list[PortfolioAsset] = Field(..., description="List of portfolio assets")
    correlations: Optional[list[list[float]]] = Field(
        None, description="Correlation matrix (NxN)"
    )
    risk_free_rate: float = Field(6.0, description="Risk-free rate (%)")
    benchmark_return: Optional[float] = Field(None, description="Benchmark return (%)")
    benchmark_std_dev: Optional[float] = Field(
        None, description="Benchmark std deviation (%)"
    )


class SIPInput(BaseModel):
    monthly_investment: Optional[float] = Field(None, description="Monthly SIP amount")
    expected_return: float = Field(12.0, description="Expected annual return (%)")
    years: float = Field(..., description="Investment period in years")
    target_amount: Optional[float] = Field(
        None, description="Target corpus (to find SIP needed)"
    )
    step_up_percentage: float = Field(0, description="Annual step-up in SIP amount (%)")


class RetirementInput(BaseModel):
    current_age: int = Field(..., description="Current age")
    retirement_age: int = Field(60, description="Planned retirement age")
    life_expectancy: int = Field(85, description="Expected life span")
    monthly_expenses: float = Field(..., description="Current monthly expenses")
    inflation_rate: float = Field(6.0, description="Expected inflation rate (%)")
    pre_retirement_return: float = Field(
        12.0, description="Expected return before retirement (%)"
    )
    post_retirement_return: float = Field(
        8.0, description="Expected return after retirement (%)"
    )
    current_retirement_savings: float = Field(
        0, description="Already saved for retirement"
    )
    pension_income: float = Field(0, description="Expected monthly pension income")


class FinancialHealthInput(BaseModel):
    monthly_income: float
    monthly_expenses: float
    total_assets: float
    total_liabilities: float
    liquid_assets: float
    monthly_emis: float
    monthly_savings: float
    emergency_fund: float
    insurance_cover: float
    age: int

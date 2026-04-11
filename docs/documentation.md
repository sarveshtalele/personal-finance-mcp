# Personal Finance MCP Server — Tool Reference

## Overview

The Personal Finance MCP provides 54 robust financial calculators across 7 essential categories. Every tool applies strictly deterministic formulas grounded in core financial and mathematical principles, ensuring transparent and repeatable results without reliance on AI inference for calculations.

---

## 1. Time Value of Money

### `calculate_future_value`
Calculate the Future Value (FV) of a lump sum involving compounding interest.
- **Inputs**: `present_value`, `annual_rate`, `years`, `compounding` (annually/monthly/quarterly/etc.)
- **Formula**: `FV = PV × (1 + r/n)^(n×t)`
- **Example**: `calculate_future_value(100000, 12, 10, "monthly")` → ₹3,30,038.69

### `calculate_present_value`
Calculate what a future sum is worth today (discounting).
- **Inputs**: `future_value`, `annual_rate`, `years`, `compounding`
- **Formula**: `PV = FV / (1 + r/n)^(n×t)`

### `calculate_annuity_fv`
Future Value of regular periodic payments, similar to an SIP.
- **Inputs**: `payment`, `annual_rate`, `years`, `frequency`, `annuity_type` (ordinary/due)
- **Formula**: `FV = PMT × [((1+r)^n - 1) / r]`

### `calculate_annuity_pv`
Present Value of regular periodic payments.
- **Inputs**: `payment`, `annual_rate`, `years`, `frequency`, `annuity_type`
- **Formula**: `PV = PMT × [(1 - (1+r)^-n) / r]`

### `calculate_perpetuity`
Present Value of infinite periodic payments.
- **Inputs**: `payment`, `annual_rate`, `growth_rate` (0 for simple perpetuity)
- **Formula**: Simple: `PV = PMT/r` | Growing: `PV = PMT/(r-g)`

### `calculate_rule_of_72`
A highly regarded heuristic to estimate the years required to double an investment.
- **Input**: `annual_rate`
- **Formula**: `Years ≈ 72 / rate`

### `calculate_effective_rate`
Convert a nominal rate to an Effective Annual Rate (EAR).
- **Inputs**: `nominal_rate`, `compounding`
- **Formula**: `EAR = (1 + r/n)^n - 1`

### `calculate_real_return`
Returns an inflation-adjusted interest rate utilizing the Fisher equation.
- **Inputs**: `nominal_rate`, `inflation_rate`
- **Formula**: `(1 + real) = (1 + nominal) / (1 + inflation)`

### `calculate_inflation_impact`
Predict the future cost of an item strictly owing to inflation.
- **Inputs**: `current_amount`, `inflation_rate`, `years`

### `calculate_savings_needed`
Derive the monthly savings required to reach a specific target corpus given an interest rate.
- **Inputs**: `target_amount`, `annual_rate`, `years`, `current_savings`

---

## 2. Debt Management

### `calculate_emi`
Equated Monthly Installment calculation for any standardized loan type.
- **Inputs**: `principal`, `annual_rate`, `tenure_years`
- **Formula**: `EMI = P × r × (1+r)^n / ((1+r)^n - 1)`
- **Example**: `calculate_emi(5000000, 8.5, 20)` → ₹43,391.16/month

### `loan_amortization`
Generates a month-wise breakdown delineating the principal/interest split.
- **Inputs**: `principal`, `annual_rate`, `tenure_years`

### `compare_loans`
Compare multiple loan options side-by-side to ascertain total cost deviations.
- **Input**: `loans_json` — JSON array of loan objects.

### `calculate_prepayment_savings`
Evaluate the quantitative impact of prepaying—quantifying interest saved and tenure reduction.
- **Inputs**: `principal`, `annual_rate`, `tenure_years`, `monthly_prepayment`, `lump_sum_prepayment`, `lump_sum_month`

### `invest_or_prepay_loan`
Analytical comparison of whether it is mathematically preferable to invest a surplus or prepay a loan.
- **Inputs**: `loan_rate`, `investment_return`, `tax_bracket`, `loan_has_tax_benefit`

### `analyze_debt_consolidation`
Algorithm to evaluate whether consolidating multiple debts into a single structured loan minimizes outlays.
- **Inputs**: `debts_json`, `consolidated_rate`, `consolidated_tenure_years`

---

## 3. Financial Planning

### `calculate_net_worth`
Quantifiable net worth derived from aggregate assets and liabilities.
- **Inputs**: `assets_json`, `liabilities_json` (name:value maps)

### `analyze_financial_ratios`
Comprehensive evaluation of essential personal finance ratios.
- **Inputs**: `monthly_income`, `monthly_expenses`, `monthly_emis`, `monthly_savings`, `total_assets`, `total_liabilities`, `liquid_assets`
- **Outputs**: Savings ratio, Debt-to-Income (DTI), liquidity ratio, solvency ratio.

### `calculate_emergency_fund`
Recommends a buffer magnitude scaled to personal dependents and stability.
- **Inputs**: `monthly_expenses`, `monthly_emis`, `dependents`, `job_stability`, `existing_emergency_fund`

### `analyze_budget`
Analytical execution of the universally standard 50/30/20 budget framework.
- **Inputs**: `monthly_income`, `expenses_json`, `existing_emis`, `existing_sips`

### `plan_financial_goal`
Plan systematically for any financial goal with dynamic inflation adjustment.
- **Inputs**: `goal_name`, `target_amount_today`, `years_to_goal`, `inflation_rate`, `expected_return`, `current_savings`

### `plan_retirement`
Comprehensive retirement corpus derivation modeling post-retirement withdrawals.
- **Inputs**: `current_age`, `retirement_age`, `life_expectancy`, `monthly_expenses`, `inflation_rate`, `pre_retirement_return`, `post_retirement_return`, `current_retirement_savings`, `monthly_pension`

### `plan_education`
Strategic algorithm for child education fund planning.
- **Inputs**: `child_current_age`, `education_start_age`, `current_education_cost`, `inflation_rate`, `expected_return`, `current_savings`

### `calculate_insurance_need`
Objectively models life insurance necessities using the Human Life Value (HLV) method.
- **Inputs**: `annual_income`, `years_of_income_to_replace`, `outstanding_loans`, `future_goals_corpus`, `existing_insurance`, `existing_investments`

### `financial_health_check`
Synthesizes a comprehensive financial wellness score (0-100).
- **Inputs**: Aggregate financial context including `monthly_income`, `total_assets`, `age`, etc.

---

## 4. Bond Analysis

### `calculate_bond_price`
Determines bond price using pure Discounted Cash Flow (DCF).
- **Inputs**: `face_value`, `coupon_rate`, `ytm`, `years_to_maturity`, `coupon_frequency`
- **Formula**: `Price = Σ[C/(1+r)^t] + FV/(1+r)^n`

### `calculate_ytm`
Yield to Maturity calculated robustly via the Newton-Raphson sequence.
- **Inputs**: `face_value`, `coupon_rate`, `market_price`, `years_to_maturity`, `coupon_frequency`

### `calculate_current_yield`
Approximates standard yield: `Current Yield = Annual Coupon / Market Price`.

### `calculate_bond_duration`
Identifies both Macaulay and Modified Duration constants.
- **Outputs**: Duration in periods, percentage price sensitivity per 1% yield change.

### `calculate_bond_convexity`
Measures second-order interest rate sensitivity.

### `calculate_zero_coupon_bond`
Derives zero-coupon bond pricing.
- **Formula**: `Price = FV / (1+r)^n`

---

## 5. Stock Valuation

### `value_stock_ddm`
Executes the Gordon Growth Model for valuation.
- **Formula**: `P = D1 / (r - g)`

### `value_stock_two_stage_ddm`
A two-stage Dividend Discount Model optimal for dynamic growth companies.

### `value_stock_pe`
Computes Price/Earnings relative valuation, enhanced with an optional PEG ratio.
- **Formula**: `Fair Price = EPS × Expected P/E`

### `value_stock_dcf`
Systematic DCF valuation modeling projected Terminal Value.
- **Formula**: `EV = Σ[FCF/(1+WACC)^t] + TV/(1+WACC)^n`

### `calculate_dividend_yield`
Formulates standard yield derived from dividend distribution.

---

## 6. Mutual Funds

### `calculate_sip_returns`
Calculates projected returns of recurring SIP investments featuring step-up logic.
- **Example**: `calculate_sip_returns(10000, 12, 10)` → ₹23.2L from a ₹12L net investment.

### `calculate_sip_needed`
Derives necessary monthly intervals structurally.

### `compare_lumpsum_vs_sip`
Conducts comparative analysis equating periodic SIP vs immediate Lumpsum injection.

### `analyze_expense_ratio_impact`
Reveals compounding detriments of mutual fund expense ratios.

### `calculate_swp`
Systematic Withdrawal Plan — analytically models continuous capital liquidation duration.

### `calculate_cagr`
Derives standard continuous growth.
- **Formula**: `CAGR = (End/Start)^(1/n) - 1`

### `calculate_nav`
Estimates Net Asset Value per Mutual Fund unit.

---

## 7. Portfolio Analysis

### `calculate_portfolio_return`
Generates an objective expected return from weighted individual assets.
- **Formula**: `E(Rp) = Σ w_i × E(R_i)`

### `calculate_portfolio_risk`
Computes portfolio variance accounting for cross-asset diversification variables.
- **Formula**: `σ²p = ΣΣ (w_i × w_j × σ_i × σ_j × ρ_ij)`

### `analyze_two_asset_portfolio`
Provides boundary analysis of a two-asset composite structure.

### `calculate_capm_return`
Formal expectations matching Capital Asset Pricing Theory.
- **Formula**: `E(R) = Rf + β(Rm - Rf)`

### `calculate_sharpe_ratio`
Derives standard Sharpe measurement correlating excess return to broad volatility.
- **Formula**: `(Rp - Rf) / σp`

### `calculate_treynor_ratio`
Identifies ratio of returns normalized strictly to systemic volatility (Beta).
- **Formula**: `(Rp - Rf) / β`

### `calculate_jensens_alpha`
Calculates absolute outperformance diverging from CAPM expected trajectories.
- **Formula**: `α = Rp - [Rf + β(Rm - Rf)]`

### `calculate_information_ratio`
Correlates the consistency of standard active returns scaled to benchmark errors.

### `calculate_sortino_ratio`
Optimizes returns per unit of explicit downside volatility constraint.

### `suggest_asset_allocation`
Algorithmic scaling based strictly on age thresholds and self-identified variance appetite.

### `rebalance_portfolio`
Determines optimal asset injection trajectories to normalize existing portfolio deviations.

---

## Response Format

Every programmatic invocation reliably returns a structured response guaranteeing interpretability:
1. **Title** — Formal calculation identifier
2. **Input summary** — Explicit mapping of validated inputs
3. **Results** — Rigorously calculated values appropriately localized
4. **Formula** — Display of exactly standard metrics computed
5. **Advisory notes** — Pragmatic interpretation directly linked to deterministic outcomes
6. **Reference** — Core logical foundation statement

// Presentation helpers — turn raw calculator dicts into clean, human English.

const CR = 1e7;
const LAKH = 1e5;

// Indian-grouped rupee value, with a compact lakh/crore form for large numbers.
export function inr(n, { compact = false } = {}) {
  if (n == null || isNaN(n)) return "—";
  const neg = n < 0;
  const v = Math.abs(n);
  let out;
  if (compact && v >= CR) out = `₹${(v / CR).toFixed(2)} Cr`;
  else if (compact && v >= LAKH) out = `₹${(v / LAKH).toFixed(2)} L`;
  else out = `₹${v.toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
  return neg ? `-${out}` : out;
}

export function pct(n) {
  if (n == null || isNaN(n)) return "—";
  return `${Number(n).toFixed(2)}%`;
}

export function num(n) {
  if (n == null || isNaN(n)) return "—";
  return Number.isInteger(n) ? n.toLocaleString("en-IN") : Number(n).toLocaleString("en-IN", { maximumFractionDigits: 2 });
}

// snake_case / camelCase -> "Sentence case"
export function titleize(key) {
  const words = key
    .replace(/_/g, " ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/\bpct\b/gi, "")
    .replace(/\bnum\b/gi, "number of")
    .trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

// Friendly overrides for specific keys (better English than auto-titleize).
const LABELS = {
  future_value: "Future value",
  present_value: "Present value",
  maturity_value: "Maturity value",
  epf_corpus: "EPF corpus at retirement",
  total_interest: "Interest earned",
  total_deposited: "You invest",
  total_invested: "You invest",
  total_contributed: "You contribute",
  total_payment: "Total repayment",
  wealth_gained: "Wealth gained",
  compounding_benefit: "Gain from compounding",
  simple_interest: "If it were simple interest",
  growth_multiple: "Growth multiple",
  wealth_ratio: "Wealth multiple",
  monthly_sip: "Monthly SIP",
  monthly_sip_needed: "Monthly SIP needed",
  emi: "Monthly EMI",
  interest_to_principal_ratio: "Interest as % of loan",
  tenure_months: "Tenure",
  effective_yield: "Effective annual yield",
  purchasing_power_loss: "Lost to inflation",
  future_amount: "Cost in the future",
  current_amount: "Cost today",
  inflation_multiplier: "Price multiplier",
  years_to_double_approx: "Years to double (Rule of 72)",
  years_to_double_exact: "Years to double (exact)",
  monthly_surplus: "Monthly surplus",
  savings_rate_pct: "Savings rate",
  emergency_fund_target: "Emergency fund target",
  emergency_fund_gap: "Emergency fund shortfall",
  debt_to_income_pct: "Debt-to-income",
  risk_profile: "Risk profile",
  suggested_equity_pct: "Suggested equity",
  retirement_corpus_needed: "Retirement corpus needed",
  retirement_corpus_gap: "Retirement shortfall",
  retirement_monthly_sip: "Invest monthly for retirement",
  prioritised_actions: "Your action plan",
  annual_rate: "Interest rate",
  annual_return: "Expected return",
  years: "Duration",
  principal: "Loan amount",
  target_amount: "Goal amount",
};

export function label(key) {
  return LABELS[key] || titleize(key);
}

// Decide how to render a value from its key + magnitude.
export function formatValue(key, value) {
  if (typeof value === "string") return value;
  if (typeof value !== "number") return String(value);

  const k = key.toLowerCase();
  if (/(rate|pct|ratio|yield|return|equity|debt_to|savings_rate)/.test(k) && !/ratio_to|multiple/.test(k)) {
    if (k.includes("multiplier") || k.includes("multiple")) return `${value.toFixed(2)}×`;
    return pct(value);
  }
  if (k.includes("multiplier") || k.includes("multiple") || k.includes("ratio")) return `${value.toFixed(2)}×`;
  if (k.includes("tenure_months")) return `${value} months`;
  if (/(years|months|number|count|periods|dependents|age)/.test(k)) return num(value);
  // money by default for large values
  if (Math.abs(value) >= 1000) return inr(value, { compact: Math.abs(value) >= LAKH });
  return num(value);
}

// The headline number for each calculator (id -> result key).
export const PRIMARY = {
  financial_plan: "retirement_monthly_sip",
  future_value: "future_value",
  emi: "emi",
  sip_returns: "future_value",
  sip_needed: "monthly_sip_needed",
  ppf: "maturity_value",
  fixed_deposit: "maturity_value",
  nsc: "maturity_value",
  epf: "epf_corpus",
  inflation_impact: "future_amount",
  rule_of_72: "years_to_double_exact",
};

// Sub-line under the headline (id -> key) for extra context.
export const PRIMARY_SUB = {
  future_value: "total_interest",
  emi: "total_payment",
  sip_returns: "wealth_gained",
  sip_needed: "total_invested",
  ppf: "total_interest",
  fixed_deposit: "total_interest",
  nsc: "total_interest",
  epf: "total_interest",
  inflation_impact: "purchasing_power_loss",
};

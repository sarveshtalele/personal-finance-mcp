// Shared client helpers. In production the API is same-origin (served by the
// Python server). For local dev against a remote API set NEXT_PUBLIC_API_BASE.
export const API = process.env.NEXT_PUBLIC_API_BASE || "";

export async function api(path, opts) {
  const res = await fetch(`${API}${path}`, opts);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const CATEGORY_ICON = {
  "Time Value of Money": "⏳",
  "Debt & Loans": "🏦",
  "Cash Flow & Budgeting": "💸",
  "Financial Planning": "🎯",
  "Fixed Income": "📜",
  "Equity Valuation": "📈",
  "Mutual Funds": "🧺",
  "Portfolio Analytics": "📊",
  Derivatives: "🔀",
  "Small Savings (India)": "🇮🇳",
  "Risk Profiling": "🧭",
  Advisor: "🤖",
  "Live Market Data": "🛰️",
};

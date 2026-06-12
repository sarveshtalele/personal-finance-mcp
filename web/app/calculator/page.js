"use client";
import { useState } from "react";
import { api } from "../lib";

const N = (label, key, def) => ({ label, key, def, type: "number" });
const SEL = (label, key, def, opts) => ({ label, key, def, type: "select", opts });

const CALCS = [
  {
    id: "financial_plan", name: "🤖 Full financial plan",
    desc: "The advisor — one input, a prioritised plan.",
    fields: [
      N("Age", "age", 30), N("Monthly income (₹)", "monthly_income", 100000),
      N("Monthly expenses (₹)", "monthly_expenses", 55000), N("Monthly EMI (₹)", "monthly_emi", 20000),
      N("Dependents", "dependents", 1), N("Emergency fund now (₹)", "existing_emergency_fund", 100000),
      N("Retirement age", "retirement_age", 60), N("Expected return %", "expected_return", 11),
      N("Inflation %", "inflation", 6),
    ],
  },
  {
    id: "future_value", name: "⏳ Future value",
    desc: "Grow a lump sum with compounding.",
    fields: [
      N("Present value (₹)", "present_value", 100000), N("Annual rate %", "annual_rate", 8),
      N("Years", "years", 10),
      SEL("Compounding", "compounding", "annually", ["annually", "semi_annually", "quarterly", "monthly", "daily", "continuous"]),
    ],
  },
  {
    id: "emi", name: "🏦 Loan EMI",
    desc: "Monthly instalment for a loan.",
    fields: [N("Principal (₹)", "principal", 5000000), N("Annual rate %", "annual_rate", 8.5), N("Tenure (years)", "tenure_years", 20)],
  },
  {
    id: "sip_returns", name: "🧺 SIP returns",
    desc: "Where a monthly SIP lands.",
    fields: [N("Monthly investment (₹)", "monthly_investment", 10000), N("Expected return %", "annual_return", 12), N("Years", "years", 15), N("Annual step-up %", "step_up_percentage", 0)],
  },
  {
    id: "sip_needed", name: "🎯 SIP for a goal",
    desc: "Monthly SIP to hit a target corpus.",
    fields: [N("Target amount (₹)", "target_amount", 10000000), N("Expected return %", "annual_return", 12), N("Years", "years", 20)],
  },
  {
    id: "ppf", name: "🇮🇳 PPF maturity",
    desc: "Public Provident Fund growth.",
    fields: [N("Annual deposit (₹)", "annual_deposit", 150000), N("Rate %", "annual_rate", 7.1), N("Years", "years", 15)],
  },
  {
    id: "fixed_deposit", name: "💰 Fixed deposit",
    desc: "Bank/NBFC FD maturity.",
    fields: [N("Principal (₹)", "principal", 100000), N("Rate %", "annual_rate", 7), N("Years", "years", 5),
      SEL("Compounding", "compounding", "quarterly", ["annually", "half_yearly", "quarterly", "monthly"])],
  },
  {
    id: "epf", name: "👔 EPF corpus",
    desc: "Provident-fund corpus at retirement.",
    fields: [N("Monthly basic (₹)", "monthly_basic", 50000), N("Rate %", "annual_rate", 8.25), N("Years", "years", 30), N("Annual increment %", "annual_increment", 5)],
  },
  {
    id: "inflation_impact", name: "📉 Inflation impact",
    desc: "Tomorrow's cost of today's expense.",
    fields: [N("Current amount (₹)", "current_amount", 100000), N("Inflation %", "inflation_rate", 6), N("Years", "years", 20)],
  },
  {
    id: "rule_of_72", name: "✌️ Rule of 72",
    desc: "Years to double your money.",
    fields: [N("Annual rate %", "annual_rate", 9)],
  },
];

function fmt(v) {
  if (typeof v === "number") return Number.isInteger(v) ? v.toLocaleString("en-IN") : v.toLocaleString("en-IN", { maximumFractionDigits: 2 });
  return String(v);
}

export default function Calculator() {
  const [calc, setCalc] = useState(CALCS[0]);
  const [vals, setVals] = useState(() => Object.fromEntries(CALCS[0].fields.map((f) => [f.key, f.def])));
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);

  function pick(c) {
    setCalc(c);
    setVals(Object.fromEntries(c.fields.map((f) => [f.key, f.def])));
    setResult(null); setErr(null);
  }

  async function run() {
    setBusy(true); setErr(null);
    try {
      const params = {};
      for (const f of calc.fields) params[f.key] = f.type === "number" ? Number(vals[f.key]) : vals[f.key];
      const r = await api("/api/calc", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ calculator: calc.id, params }),
      });
      setResult(r.result || r);
    } catch (e) { setErr(e.message); }
    setBusy(false);
  }

  return (
    <div className="container">
      <div className="page-head">
        <h1>Live calculator</h1>
        <p>The same deterministic functions your AI calls — runnable right here, in the browser.</p>
      </div>

      <div className="section" style={{ paddingTop: 28 }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginBottom: 28 }}>
          {CALCS.map((c) => (
            <button key={c.id} onClick={() => pick(c)}
              className={"btn " + (c.id === calc.id ? "btn-primary" : "btn-ghost")}
              style={{ fontSize: 14, padding: "9px 16px" }}>
              {c.name}
            </button>
          ))}
        </div>

        <div className="calc-wrap">
          <div className="card">
            <h3 style={{ marginTop: 0 }}>{calc.name}</h3>
            <p style={{ color: "var(--muted)", marginTop: 0, fontSize: 14 }}>{calc.desc}</p>
            {calc.fields.map((f) => (
              <div className="field" key={f.key}>
                <label>{f.label}</label>
                {f.type === "select" ? (
                  <select value={vals[f.key]} onChange={(e) => setVals({ ...vals, [f.key]: e.target.value })}>
                    {f.opts.map((o) => <option key={o} value={o}>{o.replace(/_/g, " ")}</option>)}
                  </select>
                ) : (
                  <input type="number" value={vals[f.key]}
                    onChange={(e) => setVals({ ...vals, [f.key]: e.target.value })} />
                )}
              </div>
            ))}
            <button className="btn btn-primary" style={{ width: "100%", marginTop: 8 }} onClick={run} disabled={busy}>
              {busy ? "Calculating…" : "Calculate"}
            </button>
          </div>

          <div>
            {err && <div className="note" style={{ marginBottom: 16 }}>Error: {err}</div>}
            {!result && !err && <div className="result-box">Results appear here. Pick a calculator, adjust the inputs and hit Calculate.</div>}
            {result && (
              <div className="card">
                {Object.entries(result).map(([k, v]) => {
                  if (k === "formula") return null;
                  if (Array.isArray(v)) return (
                    <div className="field" key={k}>
                      <label>{k.replace(/_/g, " ")}</label>
                      <ul style={{ margin: 0, paddingLeft: 18, color: "var(--ink)" }}>
                        {v.map((x, i) => <li key={i} style={{ fontSize: 14, marginBottom: 4 }}>{typeof x === "object" ? JSON.stringify(x) : String(x)}</li>)}
                      </ul>
                    </div>
                  );
                  if (typeof v === "object" && v) return null;
                  return (
                    <div className="kv" key={k}>
                      <span className="k">{k.replace(/_/g, " ")}</span>
                      <span className="v">{fmt(v)}</span>
                    </div>
                  );
                })}
                {result.formula && <p style={{ color: "var(--muted)", fontSize: 13, marginTop: 14 }}>ƒ {result.formula}</p>}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

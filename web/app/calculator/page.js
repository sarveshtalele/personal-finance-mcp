"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "../lib";
import { inr, pct, num, label, formatValue, PRIMARY, PRIMARY_SUB } from "../format";

// field: {key, label, type:"slider"|"select", min,max,step,def, unit, opts}
const fF = (key, label, def, min, max, step, unit) => ({ key, label, def, min, max, step, unit, type: "slider" });
const fS = (key, label, def, opts) => ({ key, label, def, opts, type: "select" });

const GROUPS = [
  {
    name: "Plan",
    calcs: [
      { id: "financial_plan", icon: "🤖", name: "Full financial plan", desc: "Describe your finances — get a prioritised plan.",
        fields: [
          fF("age", "Age", 30, 18, 70, 1, "int"),
          fF("monthly_income", "Monthly income", 100000, 10000, 1000000, 5000, "inr"),
          fF("monthly_expenses", "Monthly expenses", 55000, 5000, 800000, 5000, "inr"),
          fF("monthly_emi", "Monthly EMI", 20000, 0, 500000, 2500, "inr"),
          fF("dependents", "Dependents", 1, 0, 8, 1, "int"),
          fF("existing_emergency_fund", "Emergency fund today", 100000, 0, 5000000, 25000, "inr"),
          fF("retirement_age", "Retirement age", 60, 45, 75, 1, "int"),
          fF("expected_return", "Expected return", 11, 4, 16, 0.5, "pct"),
        ] },
    ],
  },
  {
    name: "Grow wealth",
    calcs: [
      { id: "sip_returns", icon: "🧺", name: "SIP returns", desc: "Where a monthly SIP lands.",
        fields: [fF("monthly_investment", "Monthly SIP", 10000, 500, 500000, 500, "inr"), fF("annual_return", "Expected return", 12, 4, 18, 0.5, "pct"), fF("years", "Duration", 15, 1, 40, 1, "yr"), fF("step_up_percentage", "Annual step-up", 0, 0, 20, 1, "pct")] },
      { id: "sip_needed", icon: "🎯", name: "SIP for a goal", desc: "Monthly SIP to hit a target corpus.",
        fields: [fF("target_amount", "Goal amount", 10000000, 100000, 100000000, 100000, "inr"), fF("annual_return", "Expected return", 12, 4, 18, 0.5, "pct"), fF("years", "Years to goal", 20, 1, 40, 1, "yr")] },
      { id: "future_value", icon: "⏳", name: "Future value", desc: "Grow a lump sum with compounding.",
        fields: [fF("present_value", "Amount today", 100000, 1000, 50000000, 10000, "inr"), fF("annual_rate", "Annual rate", 8, 1, 18, 0.5, "pct"), fF("years", "Duration", 10, 1, 40, 1, "yr"), fS("compounding", "Compounding", "annually", ["annually", "semi_annually", "quarterly", "monthly", "daily", "continuous"])] },
    ],
  },
  {
    name: "Save (India)",
    calcs: [
      { id: "ppf", icon: "🇮🇳", name: "PPF", desc: "Public Provident Fund maturity.",
        fields: [fF("annual_deposit", "Yearly deposit", 150000, 500, 150000, 500, "inr"), fF("annual_rate", "Interest rate", 7.1, 6, 9, 0.1, "pct"), fF("years", "Years", 15, 15, 50, 1, "yr")] },
      { id: "epf", icon: "👔", name: "EPF corpus", desc: "Provident-fund corpus at retirement.",
        fields: [fF("monthly_basic", "Monthly basic pay", 50000, 5000, 500000, 5000, "inr"), fF("annual_rate", "Interest rate", 8.25, 7, 9.5, 0.05, "pct"), fF("years", "Years to retire", 30, 1, 45, 1, "yr"), fF("annual_increment", "Annual increment", 5, 0, 15, 1, "pct")] },
      { id: "fixed_deposit", icon: "💰", name: "Fixed deposit", desc: "Bank / NBFC FD maturity.",
        fields: [fF("principal", "Deposit amount", 100000, 1000, 50000000, 10000, "inr"), fF("annual_rate", "Interest rate", 7, 3, 9, 0.1, "pct"), fF("years", "Tenure", 5, 1, 10, 1, "yr"), fS("compounding", "Compounding", "quarterly", ["annually", "half_yearly", "quarterly", "monthly"])] },
      { id: "nsc", icon: "📜", name: "NSC", desc: "National Savings Certificate.",
        fields: [fF("principal", "Investment", 100000, 1000, 10000000, 5000, "inr"), fF("annual_rate", "Interest rate", 7.7, 6, 9, 0.1, "pct"), fF("years", "Tenure", 5, 5, 10, 1, "yr")] },
    ],
  },
  {
    name: "Borrow & protect",
    calcs: [
      { id: "emi", icon: "🏦", name: "Loan EMI", desc: "Monthly instalment for a loan.",
        fields: [fF("principal", "Loan amount", 5000000, 50000, 100000000, 50000, "inr"), fF("annual_rate", "Interest rate", 8.5, 5, 18, 0.1, "pct"), fF("tenure_years", "Tenure", 20, 1, 30, 1, "yr")] },
      { id: "inflation_impact", icon: "📉", name: "Inflation impact", desc: "Tomorrow's cost of today's expense.",
        fields: [fF("current_amount", "Cost today", 100000, 1000, 50000000, 10000, "inr"), fF("inflation_rate", "Inflation", 6, 1, 12, 0.5, "pct"), fF("years", "Years ahead", 20, 1, 40, 1, "yr")] },
      { id: "rule_of_72", icon: "✌️", name: "Rule of 72", desc: "Years to double your money.",
        fields: [fF("annual_rate", "Annual rate", 9, 1, 20, 0.5, "pct")] },
    ],
  },
];

const ALL = GROUPS.flatMap((g) => g.calcs);

function liveFmt(unit, v) {
  if (unit === "inr") return inr(Number(v), { compact: Math.abs(v) >= 100000 });
  if (unit === "pct") return `${v}%`;
  if (unit === "yr") return `${v} yr${v == 1 ? "" : "s"}`;
  return num(Number(v));
}

export default function Calculator() {
  const [calc, setCalc] = useState(ALL[0]);
  const [vals, setVals] = useState(() => Object.fromEntries(ALL[0].fields.map((f) => [f.key, f.def])));
  const [result, setResult] = useState(null);
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);
  const timer = useRef(null);

  const pick = (c) => {
    setCalc(c);
    setVals(Object.fromEntries(c.fields.map((f) => [f.key, f.def])));
    setResult(null); setErr(null);
  };

  const run = useCallback(async (c, v) => {
    setBusy(true); setErr(null);
    try {
      const params = {};
      for (const f of c.fields) params[f.key] = f.type === "slider" ? Number(v[f.key]) : v[f.key];
      const r = await api("/api/calc", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ calculator: c.id, params }) });
      setResult(r.result || r);
    } catch (e) { setErr(e.message); }
    setBusy(false);
  }, []);

  // live, debounced recompute
  useEffect(() => {
    clearTimeout(timer.current);
    timer.current = setTimeout(() => run(calc, vals), 280);
    return () => clearTimeout(timer.current);
  }, [calc, vals, run]);

  const primaryKey = result ? (PRIMARY[calc.id] || Object.keys(result).find((k) => typeof result[k] === "number")) : null;
  const subKey = PRIMARY_SUB[calc.id];
  const actions = result?.prioritised_actions;

  const minis = useMemo(() => {
    if (!result) return [];
    return Object.entries(result).filter(([k, v]) =>
      typeof v === "number" && k !== primaryKey && k !== subKey &&
      !["annual_rate", "annual_return", "rate", "step_up"].includes(k)
    ).slice(0, 6);
  }, [result, primaryKey, subKey]);

  return (
    <div className="container">
      <div className="page-head">
        <div className="kicker">Interactive</div>
        <h1>Calculator</h1>
        <p>The exact functions your AI calls — runnable here. Drag a slider; results update live.</p>
      </div>

      <div className="section" style={{ paddingTop: 32 }}>
        <div className="calc-shell">
          {/* sidebar */}
          <aside className="calc-nav">
            {GROUPS.map((g) => (
              <div key={g.name}>
                <div className="group-label">{g.name}</div>
                {g.calcs.map((c) => (
                  <button key={c.id} className={c.id === calc.id ? "active" : ""} onClick={() => pick(c)}>
                    <span>{c.icon}</span><span>{c.name}</span>
                  </button>
                ))}
              </div>
            ))}
          </aside>

          {/* main */}
          <div className="calc-main">
            {/* inputs */}
            <div className="card">
              <h3 style={{ marginBottom: 4 }}>{calc.icon} {calc.name}</h3>
              <p className="muted" style={{ fontSize: 14, marginBottom: 22 }}>{calc.desc}</p>
              {calc.fields.map((f) => (
                <div className="field" key={f.key}>
                  <div className="row">
                    <label>{f.label}</label>
                    {f.type === "slider" && <span className="val">{liveFmt(f.unit, vals[f.key])}</span>}
                  </div>
                  {f.type === "select" ? (
                    <select aria-label={f.label} value={vals[f.key]} onChange={(e) => setVals({ ...vals, [f.key]: e.target.value })}>
                      {f.opts.map((o) => <option key={o} value={o}>{o.replace(/_/g, " ")}</option>)}
                    </select>
                  ) : (
                    <>
                      <input type="range" aria-label={`${f.label} slider`} min={f.min} max={f.max} step={f.step} value={vals[f.key]}
                        onChange={(e) => setVals({ ...vals, [f.key]: Number(e.target.value) })} />
                      <input type="number" aria-label={f.label} min={f.min} max={f.max} step={f.step} value={vals[f.key]}
                        onChange={(e) => setVals({ ...vals, [f.key]: Number(e.target.value) })} style={{ marginTop: 8 }} />
                    </>
                  )}
                </div>
              ))}
            </div>

            {/* result */}
            <div className="result-panel">
              {err && <div className="note" style={{ background: "#fef2f2", borderColor: "#fecaca", color: "var(--danger)" }}>Couldn't calculate: {err}</div>}
              {!err && result && primaryKey && (
                <>
                  <div className="headline">
                    <div className="cap">{label(primaryKey)}</div>
                    <div className="big">{formatValue(primaryKey, result[primaryKey])}</div>
                    {subKey && result[subKey] != null && (
                      <div className="sub">{label(subKey)}: {formatValue(subKey, result[subKey])}</div>
                    )}
                    {calc.id === "financial_plan" && (
                      <div className="sub">Risk profile: {result.risk_profile} · {result.suggested_equity_pct}% equity</div>
                    )}
                  </div>

                  {minis.length > 0 && (
                    <div className="metrics">
                      {minis.map(([k, v]) => (
                        <div className="metric-mini" key={k}><div className="k">{label(k)}</div><div className="v">{formatValue(k, v)}</div></div>
                      ))}
                    </div>
                  )}

                  {Array.isArray(actions) && (
                    <div className="card" style={{ marginTop: 14, padding: "10px 20px" }}>
                      <ul className="actions-list">
                        {actions.map((a, i) => <li key={i}><span className="mark">→</span><span>{a}</span></li>)}
                      </ul>
                    </div>
                  )}

                  {result.formula && <div className="formula">ƒ {result.formula}</div>}
                </>
              )}
              {!err && !result && <div className="headline"><div className="cap">Result</div><div className="big" style={{ opacity: .4 }}>—</div><div className="sub">Adjust the inputs to see your numbers.</div></div>}
            </div>
          </div>
        </div>
        <p className="muted" style={{ fontSize: 12.5, marginTop: 28, textAlign: "center" }}>
          Educational tool. Figures are illustrative and not investment advice.
        </p>
      </div>
    </div>
  );
}

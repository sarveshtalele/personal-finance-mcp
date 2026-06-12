import Link from "next/link";
import Reveal from "./Reveal";

const FEATURES = [
  { icon: "🤖", title: "Understands your story", body: "Describe your situation in plain words. The advisor maps it to the right calculators and chains them — you never name a tool." },
  { icon: "🧮", title: "76 deterministic tools", body: "Time value of money, loans, SIPs, bonds, derivatives, portfolio analytics and Indian small-savings. Exact maths — same inputs, same answer, every time." },
  { icon: "🇮🇳", title: "Grounded in NISM theory", body: "Every formula traces to the NISM Investment Adviser (Level 1) curriculum: PPF, SSY, NSC, EMI, CAPM, bond duration and more." },
  { icon: "🛰️", title: "Live market data", body: "Real mutual-fund NAVs (AMFI), FX rates (ECB) and equity quotes (Yahoo) — fetched live, no API keys, nothing to configure." },
  { icon: "🔌", title: "Works everywhere", body: "One connector URL plugs into Claude Desktop, Claude Code, Cursor, or any MCP-compatible client. Add it in under a minute." },
  { icon: "🔒", title: "Stateless & private", body: "Pure calculations behind hardened, rate-limited APIs. Nothing about you is stored — every call is independent and reproducible." },
];

const FLOW = [
  { n: 1, t: "Tell it your situation", d: "“I'm 30, earn ₹1L a month, spend ₹55k, pay a ₹20k home-loan EMI, and want to retire at 60.”" },
  { n: 2, t: "It picks and chains tools", d: "create_financial_plan runs net-worth, cash-flow, emergency-fund, debt-to-income, risk profiling and a retirement gap." },
  { n: 3, t: "You get a clear plan", d: "A prioritised action plan with exact figures and the formula behind each — then drill into any calculator for detail." },
];

const USECASES = [
  { ic: "🎯", t: "Goal & retirement planning", d: "Size the SIP for a goal, project a retirement corpus, factor in inflation." },
  { ic: "🏦", t: "Loans & debt", d: "EMI, amortisation, prepay-vs-invest, loan comparison, debt-to-income." },
  { ic: "📈", t: "Investing & valuation", d: "SIP/lumpsum, stock DCF/DDM, bond pricing, duration, mutual-fund NAV." },
  { ic: "📊", t: "Portfolio analytics", d: "Sharpe, Sortino, Treynor, alpha, CAPM, allocation and rebalancing." },
];

export default function Home() {
  return (
    <>
      <section className="hero">
        <div className="hero-mesh" />
        <div className="container">
          <span className="eyebrow"><span className="dot" /> Model Context Protocol · 76 tools · live</span>
          <h1 className="display">Financial planning,<br /><span className="gradient-text">answered by maths.</span></h1>
          <p className="lead">
            A deterministic financial toolkit your AI can actually use. Plan retirement, size a SIP,
            price a bond or hedge a portfolio — from a single plain-language question.
          </p>
          <div className="btn-row">
            <Link href="/connect/" className="btn btn-primary">Connect to Claude →</Link>
            <Link href="/calculator/" className="btn btn-ghost">Open the calculator</Link>
          </div>
          <div className="trust">No API keys · Free · Open source · Works in Claude Desktop, Claude Code & IDEs</div>

          <Reveal className="preview">
            <div className="preview-card">
              <div className="preview-bar"><i /><i /><i /></div>
              <div className="preview-body">
                <div className="chat-q">I'm 30, earn ₹1L/month, spend ₹55k, have a ₹20k EMI. Can I retire at 60?</div>
                <div className="chat-a">
                  → calls <span className="tool">create_financial_plan</span> → chains{" "}
                  <span className="tool">cash_flow</span> · <span className="tool">emergency_fund</span> ·{" "}
                  <span className="tool">debt_to_income</span> · <span className="tool">retirement_gap</span>
                  <br /><br />
                  <strong style={{ color: "var(--ink)" }}>Monthly surplus ₹25,000 · Save ₹18,400/mo for retirement · Build a ₹3.3L emergency fund first.</strong>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="band section tight">
        <div className="container">
          <div className="stats">
            {[["76", "Financial tools"], ["13", "Categories"], ["3", "Live data feeds"], ["0", "API keys"]].map(([n, l], i) => (
              <Reveal key={l} delay={i * 70}><div className="stat"><div className="stat-num">{n}</div><div className="stat-label">{l}</div></div></Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="section-head">
            <div className="kicker">Why it's different</div>
            <h2>Calculators that think with you</h2>
            <p>The gap between “what should I do?” and a precise, sourced answer — closed.</p>
          </div>
          <div className="grid grid-3">
            {FEATURES.map((f, i) => (
              <Reveal key={f.title} delay={(i % 3) * 80}>
                <div className="card hover"><div className="card-icon">{f.icon}</div><h3>{f.title}</h3><p>{f.body}</p></div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="band section">
        <div className="container">
          <div className="section-head">
            <div className="kicker">How it works</div>
            <h2>From a sentence to a plan</h2>
            <p>You speak naturally. The server bridges intent to the exact calculation.</p>
          </div>
          <div className="grid grid-3">
            {FLOW.map((s, i) => (
              <Reveal key={s.n} delay={i * 90}>
                <div className="card"><div className="step-badge">{s.n}</div><h3>{s.t}</h3><p>{s.d}</p></div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="grid grid-2" style={{ alignItems: "center", gap: 48 }}>
            <Reveal>
              <div>
                <div className="kicker" style={{ color: "var(--teal)", fontWeight: 650, fontSize: 13, textTransform: "uppercase", letterSpacing: ".08em" }}>Use cases</div>
                <h2 style={{ fontSize: "clamp(28px,4vw,40px)", margin: "12px 0 16px" }}>Everything a personal-finance conversation needs</h2>
                <p className="muted" style={{ fontSize: 17 }}>Thirteen categories of tools, from a first budget to portfolio risk-adjusted returns — all callable by your AI or right here in the browser.</p>
                <div className="btn-row" style={{ marginTop: 24, justifyContent: "flex-start" }}>
                  <Link href="/tools/" className="btn btn-primary">Browse all 76 tools</Link>
                </div>
              </div>
            </Reveal>
            <Reveal delay={120}>
              <div className="card">
                {USECASES.map((u) => (
                  <div className="usecase" key={u.t}><span className="ic">{u.ic}</span><div><b>{u.t}</b><span>{u.d}</span></div></div>
                ))}
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container narrow">
          <Reveal>
            <div className="card" style={{ textAlign: "center", padding: 48, background: "linear-gradient(160deg, var(--teal-900), var(--teal-700))", color: "#fff", border: "none" }}>
              <h2 style={{ fontSize: "clamp(28px,4vw,40px)" }}>Add it as a connector in 60 seconds</h2>
              <p style={{ color: "var(--green-soft)", fontSize: 17, maxWidth: 480, margin: "12px auto 24px" }}>
                Point any MCP client at one streamable-HTTP endpoint — all 76 tools appear instantly.
              </p>
              <div className="btn-row">
                <Link href="/connect/" className="btn" style={{ background: "#fff", color: "var(--teal-700)" }}>Setup guide</Link>
                <Link href="/calculator/" className="btn btn-ghost" style={{ background: "transparent", color: "#fff", borderColor: "rgba(255,255,255,.4)" }}>Try it first</Link>
              </div>
            </div>
          </Reveal>
        </div>
      </section>
    </>
  );
}

import Link from "next/link";

const FEATURES = [
  { icon: "🤖", title: "Understands your story", body: "Describe your situation in plain words. The advisor maps it to the right calculators — you never name a tool." },
  { icon: "🧮", title: "76 deterministic tools", body: "Time value of money, loans, SIPs, bonds, derivatives, portfolio analytics and Indian small-savings — exact maths, no guessing." },
  { icon: "🇮🇳", title: "Built on NISM theory", body: "Every formula traces to the NISM Investment Adviser (Level 1) curriculum — PPF, SSY, NSC, EMI, CAPM, duration and more." },
  { icon: "🛰️", title: "Live market data", body: "Real mutual-fund NAVs (AMFI), FX rates (ECB) and equity quotes — fetched live, no API key needed." },
  { icon: "🔌", title: "Works everywhere", body: "One connector URL plugs into Claude Desktop, Claude Code, your IDE, or any MCP-compatible client." },
  { icon: "🔒", title: "Stateless & private", body: "Pure calculations. Nothing about you is stored — every call is independent and reproducible." },
];

const FLOW = [
  { n: 1, t: "Tell it your situation", d: "“I'm 30, earn ₹1L/month, spend ₹55k, have a home-loan EMI of ₹20k and want to retire at 60.”" },
  { n: 2, t: "It picks the tools", d: "create_financial_plan chains net-worth, cash-flow, emergency-fund, debt-to-income, risk profiling and a retirement gap." },
  { n: 3, t: "You get numbers + a plan", d: "A prioritised action plan with exact figures and the formula behind each one — then drill into any calculator." },
];

export default function Home() {
  return (
    <div className="container">
      <section className="hero">
        <span className="eyebrow">Model Context Protocol · 76 tools</span>
        <h1>
          Personal finance,<br />
          <span className="gradient-text">solved by maths.</span>
        </h1>
        <p className="lead">
          A deterministic financial-planning toolkit your AI can actually use. Plan retirement,
          size a SIP, price a bond or hedge a portfolio — from a plain-language question.
        </p>
        <div className="btn-row">
          <Link href="/connect/" className="btn btn-primary">Connect to Claude</Link>
          <Link href="/calculator/" className="btn btn-ghost">Try a calculator</Link>
        </div>
      </section>

      <section className="stats">
        <div className="stat"><div className="stat-num">76</div><div className="stat-label">Financial tools</div></div>
        <div className="stat"><div className="stat-num">13</div><div className="stat-label">Categories</div></div>
        <div className="stat"><div className="stat-num">3</div><div className="stat-label">Live data feeds</div></div>
        <div className="stat"><div className="stat-num">0</div><div className="stat-label">API keys needed</div></div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>Calculators that think with you</h2>
          <p>The gap between &ldquo;what should I do?&rdquo; and a precise answer — closed.</p>
        </div>
        <div className="grid grid-3">
          {FEATURES.map((f) => (
            <div className="card" key={f.title}>
              <div className="card-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2>From a sentence to a plan</h2>
          <p>You speak naturally. The server bridges intent to the exact calculation.</p>
        </div>
        <div className="grid grid-3">
          {FLOW.map((s) => (
            <div className="card" key={s.n}>
              <div className="card-icon">{s.n}</div>
              <h3>{s.t}</h3>
              <p>{s.d}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section" style={{ textAlign: "center" }}>
        <div className="card" style={{ maxWidth: 720, margin: "0 auto", padding: 40 }}>
          <h2 style={{ marginTop: 0 }}>Add it as a connector in 60 seconds</h2>
          <p style={{ color: "var(--muted)", fontSize: 17 }}>
            Point any MCP client at the streamable-HTTP endpoint and all 76 tools appear instantly.
          </p>
          <div className="btn-row" style={{ marginTop: 8 }}>
            <Link href="/connect/" className="btn btn-primary">Setup guide</Link>
            <Link href="/tools/" className="btn btn-ghost">Browse all tools</Link>
          </div>
        </div>
      </section>
    </div>
  );
}

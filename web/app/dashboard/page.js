"use client";
import { useEffect, useState } from "react";
import { api } from "../lib";

const INDICES = [
  { sym: "^NSEI", label: "Nifty 50" },
  { sym: "^BSESN", label: "BSE Sensex" },
  { sym: "^DJI", label: "Dow Jones" },
];

export default function Dashboard() {
  const [fx, setFx] = useState(null);
  const [quotes, setQuotes] = useState({});
  const [navQ, setNavQ] = useState("");
  const [navResults, setNavResults] = useState(null);
  const [nav, setNav] = useState(null);

  useEffect(() => {
    api("/api/fx?base=USD&symbols=INR,EUR,GBP,JPY").then(setFx).catch(() => {});
    INDICES.forEach(({ sym }) =>
      api(`/api/quote?symbol=${encodeURIComponent(sym)}`)
        .then((d) => setQuotes((q) => ({ ...q, [sym]: d })))
        .catch(() => {})
    );
  }, []);

  async function searchNav(e) {
    e.preventDefault();
    if (!navQ.trim()) return;
    setNavResults(null); setNav(null);
    try { setNavResults(await api(`/api/nav?q=${encodeURIComponent(navQ)}`)); }
    catch { setNavResults({ error: "search failed" }); }
  }
  async function loadNav(code) {
    try { setNav(await api(`/api/nav?code=${code}`)); } catch { setNav({ error: "fetch failed" }); }
  }

  return (
    <div className="container">
      <div className="page-head">
        <h1>Market dashboard</h1>
        <p>Live, keyless data — the same feeds the MCP tools use. Mutual-fund NAVs from AMFI, FX from the ECB, index quotes from stooq.</p>
      </div>

      <div className="section" style={{ paddingTop: 28 }}>
        <h3>Indices</h3>
        <div className="grid grid-3" style={{ marginBottom: 36 }}>
          {INDICES.map(({ sym, label }) => {
            const d = quotes[sym];
            const up = d?.change_pct >= 0;
            return (
              <div className="metric" key={sym}>
                <div className="label">{label}</div>
                <div className="value">{d?.price ? Number(d.price).toLocaleString("en-IN", { maximumFractionDigits: 2 }) : "—"}</div>
                <div className="sub" style={{ color: d?.change_pct != null ? (up ? "var(--teal)" : "#dc2626") : "var(--muted)" }}>
                  {d?.change_pct != null ? `${up ? "▲" : "▼"} ${Math.abs(d.change_pct)}% · ${d.currency || ""}` : (d?.error || "loading…")}
                </div>
              </div>
            );
          })}
        </div>

        <h3>Currencies · 1 USD</h3>
        <div className="grid grid-3" style={{ marginBottom: 36 }}>
          {fx?.rates ? Object.entries(fx.rates).map(([k, v]) => (
            <div className="metric" key={k}>
              <div className="label">USD → {k}</div>
              <div className="value">{Number(v).toFixed(2)}</div>
              <div className="sub">ECB ref · {fx.date}</div>
            </div>
          )) : <div className="metric"><div className="label">FX</div><div className="value">—</div><div className="sub">loading…</div></div>}
        </div>

        <h3>Mutual-fund NAV lookup</h3>
        <form onSubmit={searchNav}>
          <input className="search" placeholder="Search a fund — e.g. “Parag Parikh Flexi Cap”, “HDFC Index”"
            value={navQ} onChange={(e) => setNavQ(e.target.value)} />
        </form>

        {navResults?.schemes && (
          <div className="tool-list" style={{ marginBottom: 24 }}>
            {navResults.schemes.map((s) => (
              <button key={s.scheme_code} className="tool-item" style={{ textAlign: "left", cursor: "pointer", border: "1px solid var(--line)" }}
                onClick={() => loadNav(s.scheme_code)}>
                <code>{s.scheme_code}</code>
                <p>{s.scheme_name}</p>
              </button>
            ))}
          </div>
        )}
        {navResults?.error && <div className="note">No results / search failed.</div>}

        {nav && !nav.error && (
          <div className="card" style={{ maxWidth: 520 }}>
            <h3 style={{ marginTop: 0 }}>{nav.scheme_name}</h3>
            <div className="kv"><span className="k">NAV</span><span className="v">₹{nav.nav}</span></div>
            <div className="kv"><span className="k">Date</span><span className="v">{nav.date}</span></div>
            <div className="kv"><span className="k">Fund house</span><span className="v">{nav.fund_house}</span></div>
            <div className="kv"><span className="k">Category</span><span className="v">{nav.category}</span></div>
          </div>
        )}
      </div>
    </div>
  );
}

"use client";
import { useEffect, useState } from "react";
import { api } from "../lib";
import { num } from "../format";

const INDICES = [
  { sym: "^NSEI", label: "Nifty 50" },
  { sym: "^BSESN", label: "BSE Sensex" },
  { sym: "^DJI", label: "Dow Jones" },
];

function Metric({ label, value, sub, subClass, loading }) {
  return (
    <div className="metric-card">
      <div className="label">{label}</div>
      {loading ? <div className="skel" style={{ height: 34, width: "60%", margin: "6px 0" }} />
        : <div className="value">{value}</div>}
      {loading ? <div className="skel" style={{ height: 14, width: "40%" }} />
        : <div className={"sub " + (subClass || "muted")}>{sub}</div>}
    </div>
  );
}

export default function Dashboard() {
  const [fx, setFx] = useState(null);
  const [quotes, setQuotes] = useState({});
  const [navQ, setNavQ] = useState("");
  const [navResults, setNavResults] = useState(null);
  const [nav, setNav] = useState(null);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    api("/api/fx?base=USD&symbols=INR,EUR,GBP").then(setFx).catch(() => setFx({ error: true }));
    INDICES.forEach(({ sym }) =>
      api(`/api/quote?symbol=${encodeURIComponent(sym)}`)
        .then((d) => setQuotes((q) => ({ ...q, [sym]: d }))).catch(() => setQuotes((q) => ({ ...q, [sym]: { error: true } })))
    );
  }, []);

  async function searchNav(e) {
    e.preventDefault();
    if (!navQ.trim()) return;
    setSearching(true); setNavResults(null); setNav(null);
    try { setNavResults(await api(`/api/nav?q=${encodeURIComponent(navQ)}`)); }
    catch { setNavResults({ error: "search failed" }); }
    setSearching(false);
  }
  async function loadNav(code) { try { setNav(await api(`/api/nav?code=${code}`)); } catch { setNav({ error: "fetch failed" }); } }

  return (
    <div className="container">
      <div className="page-head">
        <div className="kicker">Live market data</div>
        <h1>Dashboard</h1>
        <p>Real, keyless feeds — the same ones the MCP tools use. Indices &amp; FX update on load; look up any mutual-fund NAV below.</p>
      </div>

      <div className="section" style={{ paddingTop: 32 }}>
        <h3 style={{ marginBottom: 16 }}>Indices</h3>
        <div className="grid grid-3" style={{ marginBottom: 40 }}>
          {INDICES.map(({ sym, label }) => {
            const d = quotes[sym];
            const up = d?.change_pct >= 0;
            return (
              <Metric key={sym} loading={!d} label={label}
                value={d?.price != null ? num(d.price) : "—"}
                sub={d?.error ? "unavailable" : d?.change_pct != null ? `${up ? "▲" : "▼"} ${Math.abs(d.change_pct)}%  ·  ${d.currency || ""}` : ""}
                subClass={d?.change_pct != null ? (up ? "up" : "down") : "muted"} />
            );
          })}
        </div>

        <h3 style={{ marginBottom: 16 }}>Currencies · per 1 USD</h3>
        <div className="grid grid-3" style={{ marginBottom: 40 }}>
          {fx?.rates ? Object.entries(fx.rates).map(([k, v]) => (
            <Metric key={k} label={`USD → ${k}`} value={Number(v).toFixed(2)} sub={`ECB reference · ${fx.date}`} subClass="muted" />
          )) : [0, 1, 2].map((i) => <Metric key={i} loading={!fx?.error} label="USD → …" value="—" sub={fx?.error ? "unavailable" : ""} />)}
        </div>

        <h3 style={{ marginBottom: 12 }}>Mutual-fund NAV lookup</h3>
        <form onSubmit={searchNav} className="toolbar" style={{ marginBottom: 20 }}>
          <input className="search" placeholder="Search a fund — e.g. “Parag Parikh Flexi Cap”, “HDFC Index”"
            value={navQ} onChange={(e) => setNavQ(e.target.value)} />
          <button className="btn btn-primary btn-sm" type="submit" disabled={searching}>{searching ? "Searching…" : "Search"}</button>
        </form>

        {navResults?.schemes?.length > 0 && (
          <div className="tool-list" style={{ marginBottom: 24 }}>
            {navResults.schemes.map((s) => (
              <button key={s.scheme_code} className="tool-item" style={{ textAlign: "left", cursor: "pointer" }} onClick={() => loadNav(s.scheme_code)}>
                <code>#{s.scheme_code}</code><p>{s.scheme_name}</p>
              </button>
            ))}
          </div>
        )}
        {navResults && !navResults.schemes?.length && <div className="note">No funds matched that search.</div>}

        {nav && !nav.error && (
          <div className="card" style={{ maxWidth: 540 }}>
            <h3 style={{ marginBottom: 14 }}>{nav.scheme_name}</h3>
            <div className="metrics" style={{ gridTemplateColumns: "1fr 1fr" }}>
              <div className="metric-mini"><div className="k">Latest NAV</div><div className="v">₹{nav.nav}</div></div>
              <div className="metric-mini"><div className="k">As of</div><div className="v">{nav.date}</div></div>
              <div className="metric-mini"><div className="k">Fund house</div><div className="v" style={{ fontSize: 14 }}>{nav.fund_house}</div></div>
              <div className="metric-mini"><div className="k">Category</div><div className="v" style={{ fontSize: 14 }}>{nav.category}</div></div>
            </div>
          </div>
        )}
        <p className="muted" style={{ fontSize: 12.5, marginTop: 32, textAlign: "center" }}>
          Market data is delayed/best-effort from public sources. For information only, not investment advice.
        </p>
      </div>
    </div>
  );
}

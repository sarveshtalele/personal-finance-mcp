"use client";
import { useEffect, useMemo, useState } from "react";
import { api, CATEGORY_ICON } from "../lib";

export default function ToolsPage() {
  const [data, setData] = useState(null);
  const [q, setQ] = useState("");
  const [active, setActive] = useState("All");
  const [err, setErr] = useState(null);

  useEffect(() => { api("/api/tools").then(setData).catch((e) => setErr(e.message)); }, []);

  const categories = useMemo(() => (data ? ["All", ...Object.keys(data.categories)] : ["All"]), [data]);

  const grouped = useMemo(() => {
    if (!data) return {};
    const f = q.trim().toLowerCase();
    const out = {};
    for (const t of data.tools) {
      if (active !== "All" && t.category !== active) continue;
      if (f && !`${t.name} ${t.description}`.toLowerCase().includes(f)) continue;
      (out[t.category] = out[t.category] || []).push(t);
    }
    return out;
  }, [data, q, active]);

  return (
    <div className="container">
      <div className="page-head">
        <div className="kicker">Catalog</div>
        <h1>{data ? `${data.count} financial tools` : "Tools"}</h1>
        <p>Every tool is a deterministic calculator grounded in the NISM IA Level 1 syllabus. Filter by category or search by what it does.</p>
      </div>

      <div className="section" style={{ paddingTop: 28 }}>
        <div className="toolbar">
          <input className="search" placeholder="Search — “retirement”, “loan”, “PPF”, “option”, “Sharpe”…" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <div className="toolbar">
          {categories.map((c) => (
            <button key={c} className={"chip" + (active === c ? " active" : "")} onClick={() => setActive(c)}>
              {c === "All" ? "All" : `${CATEGORY_ICON[c] || "•"} ${c}`}
              {c !== "All" && data ? ` ${data.categories[c]}` : ""}
            </button>
          ))}
        </div>

        {err && <div className="note" style={{ marginTop: 20 }}>Couldn't load the live catalog ({err}). The server may be waking up — refresh in a moment.</div>}
        {!data && !err && (
          <div className="grid grid-2" style={{ marginTop: 24 }}>
            {[...Array(6)].map((_, i) => <div key={i} className="skel" style={{ height: 70 }} />)}
          </div>
        )}

        <div style={{ marginTop: 24 }}>
          {Object.entries(grouped).map(([cat, tools]) => (
            <div className="cat-block" key={cat}>
              <div className="cat-title">
                <span style={{ fontSize: 22 }}>{CATEGORY_ICON[cat] || "•"}</span>
                <h3>{cat}</h3><span className="pill">{tools.length}</span>
              </div>
              <div className="tool-list">
                {tools.map((t) => (
                  <div className="tool-item" key={t.name}><code>{t.name}</code><p>{t.description}</p></div>
                ))}
              </div>
            </div>
          ))}
          {data && Object.keys(grouped).length === 0 && <div className="note">No tools match “{q}”.</div>}
        </div>
      </div>
    </div>
  );
}

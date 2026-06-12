"use client";
import { useEffect, useMemo, useState } from "react";
import { api, CATEGORY_ICON } from "../lib";

export default function ToolsPage() {
  const [data, setData] = useState(null);
  const [q, setQ] = useState("");
  const [err, setErr] = useState(null);

  useEffect(() => {
    api("/api/tools").then(setData).catch((e) => setErr(e.message));
  }, []);

  const grouped = useMemo(() => {
    if (!data) return {};
    const f = q.trim().toLowerCase();
    const out = {};
    for (const t of data.tools) {
      if (f && !(`${t.name} ${t.description}`.toLowerCase().includes(f))) continue;
      (out[t.category] = out[t.category] || []).push(t);
    }
    return out;
  }, [data, q]);

  return (
    <div className="container">
      <div className="page-head">
        <h1>{data ? `${data.count} financial tools` : "Tool catalog"}</h1>
        <p>Every tool is a deterministic calculator grounded in the NISM IA Level&nbsp;1 syllabus. Search by name or what it does.</p>
      </div>

      <div className="section" style={{ paddingTop: 32 }}>
        <input
          className="search"
          placeholder="Search tools — e.g. “retirement”, “loan”, “PPF”, “option”…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />

        {err && <div className="note">Could not load the live catalog ({err}). The server may be starting up.</div>}
        {!data && !err && <p style={{ color: "var(--muted)" }}>Loading…</p>}

        {Object.entries(grouped).map(([cat, tools]) => (
          <div className="cat-block" key={cat}>
            <div className="cat-title">
              <span style={{ fontSize: 22 }}>{CATEGORY_ICON[cat] || "•"}</span>
              <h3>{cat}</h3>
              <span className="pill">{tools.length}</span>
            </div>
            <div className="tool-list">
              {tools.map((t) => (
                <div className="tool-item" key={t.name}>
                  <code>{t.name}</code>
                  <p>{t.description}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

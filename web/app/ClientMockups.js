"use client";
import { useState } from "react";

const TABS = ["Claude Desktop", "Claude Code", "VS Code"];

function DesktopMock() {
  return (
    <div className="mockup">
      <div className="win-bar">
        <span className="dots"><i className="r" /><i className="y" /><i className="g" /></span>
        <span className="ttl">Claude</span>
      </div>
      <div className="win-body">
        <div className="dm-q">How much SIP for ₹2 crore in 18 years at 12%?</div>
        <div className="dm-a">
          Using <span className="tool">calculate_sip_needed</span> →
          <ul>
            <li><span className="mk">→</span>Monthly SIP: <strong>₹26,640</strong></li>
            <li><span className="mk">→</span>You invest ₹57.5L · wealth gained ₹1.42 Cr</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

function CodeMock() {
  return (
    <div className="mockup">
      <div className="win-bar">
        <span className="dots"><i className="r" /><i className="y" /><i className="g" /></span>
        <span className="ttl">claude — personal-finance</span>
      </div>
      <div className="term">
        <div><span className="p">›</span> <span className="hl">Compare PPF vs a 7% FD for ₹1.5L/year over 15 years</span></div>
        <div className="d">⏺ calling calculate_ppf, calculate_fixed_deposit …</div>
        <div><span className="c">PPF</span>  maturity ₹40,68,209  ·  interest ₹18,18,209</div>
        <div><span className="c">FD</span>   maturity ₹39,21,560  ·  interest ₹16,71,560</div>
        <div className="hl">→ PPF wins by ₹1.46L and is tax-free.</div>
      </div>
    </div>
  );
}

function VsMock() {
  return (
    <div className="mockup">
      <div className="vs">
        <div className="vs-act"><span>📄</span><span>🔍</span><span>⎇</span><span>💬</span></div>
        <div className="vs-side">
          <p className="h">Explorer</p>
          <div className="file">portfolio.py</div>
          <div className="file on">analysis.ipynb</div>
          <div className="file">README.md</div>
        </div>
        <div className="vs-main">
          <span className="vs-tab">💬 MCP: personal-finance</span>
          <div className="vs-chat">
            <div><span className="u">you ›</span> Is my 70/30 equity-debt split too risky at 45?</div>
            <div style={{ marginTop: 8 }}><span className="tool">assess_risk_profile</span> → Moderate · suggests 50% equity</div>
            <div><span className="tool">rebalance_portfolio</span> → sell ₹4.0L equity, buy debt</div>
            <div className="hl" style={{ marginTop: 8 }}>→ Trim equity to ~50–55% to match your horizon.</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function ClientMockups() {
  const [tab, setTab] = useState(0);
  return (
    <div>
      <div style={{ textAlign: "center" }}>
        <div className="tabs">
          {TABS.map((t, i) => (
            <button key={t} className={tab === i ? "active" : ""} onClick={() => setTab(i)}>{t}</button>
          ))}
        </div>
      </div>
      {tab === 0 && <DesktopMock />}
      {tab === 1 && <CodeMock />}
      {tab === 2 && <VsMock />}
    </div>
  );
}

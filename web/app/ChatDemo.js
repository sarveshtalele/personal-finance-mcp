"use client";
import { useEffect, useRef, useState } from "react";

const QUERY = "I'm 30, earn ₹1L/month, spend ₹55k, have a ₹20k EMI. Can I retire at 60?";
const TOOLS = ["cash_flow", "emergency_fund", "debt_to_income", "retirement_gap"];
const ANSWER = [
  ["Monthly surplus", "₹25,000"],
  ["Retirement SIP", "₹18,400 / month"],
  ["Do first", "Build a ₹3.3L emergency fund"],
];
const REPORT = [
  ["Monthly surplus", "₹25,000"],
  ["Savings rate", "25%"],
  ["Emergency fund target", "₹3,30,000"],
  ["Debt-to-income", "20% — healthy"],
  ["Retirement corpus needed", "₹6.1 Cr"],
  ["Invest monthly", "₹18,400"],
];

export default function ChatDemo() {
  const [typed, setTyped] = useState("");
  const [phase, setPhase] = useState(0); // 0 typing,1 thinking,2 tools,3 answer,4 report-ready
  const [report, setReport] = useState(false);
  const timers = useRef([]);

  const clear = () => { timers.current.forEach(clearTimeout); timers.current = []; };
  const at = (ms, fn) => timers.current.push(setTimeout(fn, ms));

  const play = () => {
    clear(); setTyped(""); setPhase(0); setReport(false);
    let i = 0;
    const step = () => {
      i++; setTyped(QUERY.slice(0, i));
      if (i < QUERY.length) at(28, step);
      else { at(450, () => setPhase(1)); at(1500, () => setPhase(2)); at(3200, () => setPhase(3)); at(4400, () => setPhase(4)); }
    };
    at(500, step);
  };

  useEffect(() => { play(); return clear; }, []);

  return (
    <div className="preview-card">
      <div className="win-bar">
        <span className="dots"><i className="r" /><i className="y" /><i className="g" /></span>
        <span className="ttl">Claude · Personal Finance MCP</span>
        {phase >= 4 && <button className="replay" onClick={play}>↻ Replay</button>}
      </div>
      <div className="preview-body">
        <div className="chat">
          <div className="bubble user">{typed}{phase === 0 && <span className="cursor" />}</div>

          {phase >= 1 && (
            <div className="bubble ai">
              <div className="toolrun">
                {phase === 1 ? (
                  <span className="thinking"><i /><i /><i /></span>
                ) : (
                  <>
                    <span>calls <span className="call">create_financial_plan</span> →</span>
                    {TOOLS.map((t, i) => (
                      <span className="tchip" key={t} style={{ animationDelay: `${i * 140}ms` }}>{t}</span>
                    ))}
                  </>
                )}
              </div>

              {phase >= 3 && ANSWER.map(([k, v], i) => (
                <div className="aline" key={k} style={{ animationDelay: `${i * 160}ms` }}>
                  <span className="mk">→</span><span>{k}: <b>{v}</b></span>
                </div>
              ))}

              {phase >= 4 && !report && (
                <button className="btn btn-primary btn-sm genbtn" onClick={() => setReport(true)}>📄 Generate full report</button>
              )}

              {report && (
                <div className="report">
                  <div className="report-head"><span>Your financial plan</span><span>30 → 60</span></div>
                  <div className="report-body">
                    {REPORT.map(([k, v]) => (
                      <div className="report-row" key={k}><span className="k">{k}</span><span className="v">{v}</span></div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

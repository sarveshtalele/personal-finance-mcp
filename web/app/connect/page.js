"use client";
import { useEffect, useState } from "react";

function Code({ children }) {
  const [copied, setCopied] = useState(false);
  const copy = () => { navigator.clipboard?.writeText(children); setCopied(true); setTimeout(() => setCopied(false), 1400); };
  return (
    <div className="codeblock">
      <button className="copy" onClick={copy}>{copied ? "copied ✓" : "copy"}</button>
      <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{children}</pre>
    </div>
  );
}

export default function Connect() {
  const [origin, setOrigin] = useState("https://your-space.hf.space");
  useEffect(() => { if (typeof window !== "undefined") setOrigin(window.location.origin); }, []);
  const url = `${origin}/mcp`;

  return (
    <div className="container">
      <div className="page-head">
        <h1>Connect in 60 seconds</h1>
        <p>One streamable-HTTP endpoint. Add it anywhere that speaks MCP — all 76 tools show up instantly.</p>
      </div>

      <div className="section" style={{ paddingTop: 24, maxWidth: 820 }}>
        <div className="note" style={{ marginBottom: 28 }}>
          Your connector URL: <strong>{url}</strong>
        </div>

        <div className="step">
          <div className="step-num">1</div>
          <div style={{ flex: 1 }}>
            <h4>Claude Desktop — custom connector (easiest)</h4>
            <p>Settings → <strong>Connectors</strong> → <strong>Add custom connector</strong> → paste the URL:</p>
            <Code>{url}</Code>
          </div>
        </div>

        <div className="step">
          <div className="step-num">2</div>
          <div style={{ flex: 1 }}>
            <h4>Claude Code (CLI)</h4>
            <p>One command adds it as an HTTP server:</p>
            <Code>{`claude mcp add --transport http personal-finance ${url}`}</Code>
          </div>
        </div>

        <div className="step">
          <div className="step-num">3</div>
          <div style={{ flex: 1 }}>
            <h4>Cursor / VS Code / any IDE</h4>
            <p>Add to your <code>mcp.json</code> (or the IDE&rsquo;s MCP settings):</p>
            <Code>{`{
  "mcpServers": {
    "personal-finance": {
      "url": "${url}",
      "transport": "http"
    }
  }
}`}</Code>
          </div>
        </div>

        <div className="step">
          <div className="step-num">4</div>
          <div style={{ flex: 1 }}>
            <h4>Claude Desktop via config file (stdio bridge)</h4>
            <p>If you prefer the config file, bridge the remote server with <code>mcp-remote</code>. Edit <code>claude_desktop_config.json</code>:</p>
            <Code>{`{
  "mcpServers": {
    "personal-finance": {
      "command": "npx",
      "args": ["mcp-remote", "${url}"]
    }
  }
}`}</Code>
          </div>
        </div>

        <div className="step">
          <div className="step-num">5</div>
          <div style={{ flex: 1 }}>
            <h4>Run it locally (stdio, fully offline)</h4>
            <p>Clone the repo and point Claude Desktop at the local process:</p>
            <Code>{`pip install -e .
# claude_desktop_config.json
{
  "mcpServers": {
    "personal-finance": {
      "command": "python",
      "args": ["-m", "src"]
    }
  }
}`}</Code>
          </div>
        </div>

        <h3 style={{ marginTop: 40 }}>Try these prompts</h3>
        <div className="grid grid-2">
          {[
            "I'm 32, earn ₹1.2L/month, spend ₹70k, have a ₹25k home-loan EMI. Build me a financial plan.",
            "How much SIP do I need to reach ₹2 crore in 18 years at 12%?",
            "Price a 1-year ATM call on a ₹100 stock with 20% volatility.",
            "Compare PPF vs a 7% FD for ₹1.5L/year over 15 years.",
          ].map((p) => (
            <div className="card" key={p}><p style={{ margin: 0 }}>&ldquo;{p}&rdquo;</p></div>
          ))}
        </div>
      </div>
    </div>
  );
}

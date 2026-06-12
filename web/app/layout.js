import "./globals.css";
import Link from "next/link";
import Nav from "./Nav";

export const metadata = {
  metadataBase: new URL("https://sarveshtalele-personal-finance-mcp.hf.space"),
  title: "FinPlan MCP — 76 financial planning tools for your AI",
  description:
    "A deterministic personal-finance toolkit (NISM IA Level 1) exposed over the Model Context Protocol. Plan, calculate and analyse from plain-language questions — in Claude Desktop, your IDE, or right here.",
  openGraph: {
    title: "FinPlan MCP — financial planning tools for your AI",
    description: "76 deterministic financial calculators, a meta-advisor, and live market data — as one MCP connector + website.",
    type: "website",
  },
};

export default function RootLayout({ children }) {
  const year = new Date().getFullYear();
  return (
    <html lang="en">
      <body>
        <Nav />
        <main>{children}</main>
        <footer className="footer">
          <div className="container footer-grid">
            <div>
              <Link href="/" className="brand"><span className="brand-mark">₹</span><span>FinPlan&nbsp;MCP</span></Link>
              <p>Deterministic financial planning, grounded in the NISM Investment Adviser (Level 1) curriculum. Educational use only — not investment advice.</p>
            </div>
            <div className="col">
              <h5>Product</h5>
              <Link href="/tools/">Tools</Link>
              <Link href="/calculator/">Calculator</Link>
              <Link href="/dashboard/">Dashboard</Link>
              <Link href="/connect/">Connect</Link>
            </div>
            <div className="col">
              <h5>Resources</h5>
              <a href="https://github.com/sarveshtalele/personal-finance-mcp" target="_blank" rel="noreferrer noopener">GitHub</a>
              <a href="https://modelcontextprotocol.io" target="_blank" rel="noreferrer noopener">About MCP</a>
              <a href="/api/health">API status</a>
            </div>
          </div>
          <div className="container" style={{ marginTop: 28, color: "var(--muted-2)", fontSize: 13 }}>
            © {year} FinPlan MCP · MIT License
          </div>
        </footer>
      </body>
    </html>
  );
}

import "./globals.css";
import Nav from "./Nav";

export const metadata = {
  title: "Personal Finance MCP — 76 financial tools for Claude",
  description:
    "A deterministic personal-finance toolkit (NISM IA Level 1) exposed as MCP tools. Plan, calculate and analyse — in Claude Desktop, your IDE, or right here.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Nav />
        <main>{children}</main>
        <footer className="footer">
          <div className="container footer-inner">
            <span>© {new Date().getFullYear()} Personal Finance MCP · MIT License</span>
            <span>Built on the NISM Investment Adviser (Level 1) curriculum · Educational use only</span>
          </div>
        </footer>
      </body>
    </html>
  );
}

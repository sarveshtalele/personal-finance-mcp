"use client";
import Link from "next/link";

export default function Nav() {
  return (
    <nav className="nav">
      <div className="container nav-inner">
        <Link href="/" className="brand">
          <span className="brand-mark">₹</span>
          <span>Finance&nbsp;MCP</span>
        </Link>
        <div className="nav-links">
          <Link href="/tools/">Tools</Link>
          <Link href="/calculator/">Calculator</Link>
          <Link href="/dashboard/">Dashboard</Link>
          <Link href="/connect/" className="nav-cta">Connect</Link>
        </div>
      </div>
    </nav>
  );
}

"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/tools/", label: "Tools" },
  { href: "/calculator/", label: "Calculator" },
  { href: "/dashboard/", label: "Dashboard" },
];

export default function Nav() {
  const path = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => { setOpen(false); }, [path]);

  const isActive = (h) => path === h || path === h.replace(/\/$/, "");

  return (
    <nav className={"nav" + (scrolled ? " scrolled" : "")}>
      <div className="container nav-inner">
        <Link href="/" className="brand">
          <span className="brand-mark">₹</span>
          <span>FinPlan&nbsp;MCP</span>
        </Link>
        <div className="nav-links">
          {LINKS.map((l) => (
            <Link key={l.href} href={l.href} className={isActive(l.href) ? "active" : ""}
              aria-current={isActive(l.href) ? "page" : undefined}>{l.label}</Link>
          ))}
          <Link href="/connect/" className="nav-cta">Connect</Link>
        </div>
        <button className="nav-burger" aria-label="Menu" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
          {open ? "✕" : "☰"}
        </button>
      </div>
      <div className={"mobile-menu" + (open ? " open" : "")}>
        {LINKS.map((l) => <Link key={l.href} href={l.href}>{l.label}</Link>)}
        <Link href="/connect/">Connect</Link>
      </div>
    </nav>
  );
}

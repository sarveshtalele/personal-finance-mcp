import Link from "next/link";

export const metadata = { title: "Page not found — FinPlan MCP" };

export default function NotFound() {
  return (
    <div className="container" style={{ textAlign: "center", padding: "120px 24px 80px" }}>
      <div className="eyebrow"><span className="dot" /> 404</div>
      <h1 className="display" style={{ fontSize: "clamp(38px,7vw,72px)" }}>
        This page <span className="gradient-text">doesn&rsquo;t add up.</span>
      </h1>
      <p className="lead">The page you&rsquo;re looking for isn&rsquo;t here. The numbers still are.</p>
      <div className="btn-row">
        <Link href="/" className="btn btn-primary">Back home</Link>
        <Link href="/calculator/" className="btn btn-ghost">Open the calculator</Link>
      </div>
    </div>
  );
}

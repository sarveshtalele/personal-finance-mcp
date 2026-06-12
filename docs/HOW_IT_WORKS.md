# How It Works — Concepts, Architecture & Hosting

A complete walkthrough of what this project is, the ideas behind it, how the
pieces fit together, how to host it (including on your own portfolio site), and
an honest assessment of how far it is from an enterprise/production-grade system.

---

## 1. What this project is

One codebase that ships **three products at once**:

1. **An MCP server** — 76 deterministic personal-finance calculators an LLM can call.
2. **A website** — a Next.js UI (tool catalog, live calculator, market dashboard, setup guide).
3. **A hosted connector** — a single public HTTPS URL that any MCP client can attach to.

The trick is that all three are served by **one process** on **one port**.

---

## 2. Core concepts

### 2.1 Model Context Protocol (MCP)

MCP is an open protocol that lets an AI model (the *client*, e.g. Claude) discover
and call external **tools** exposed by a *server*. The model reads each tool's
name + description, decides which to call, sends JSON arguments, and gets a result
back. Think of it as "function calling, standardised across apps."

This project is an MCP **server**. It does not contain an LLM — it exposes tools.
The LLM lives in the client (Claude Desktop, Claude Code, your IDE).

### 2.2 Deterministic calculators

Every tool is a **pure function**: same inputs → same output, no randomness, no
model inference for the numbers. `calculate_emi(5000000, 8.5, 20)` always returns
₹43,391.16. This is the opposite of letting an LLM "estimate" maths — it's exact
and auditable, and each result includes the formula used.

### 2.3 Story → tools (semantic routing)

Users don't name tools. They say *"I'm 30, earn ₹1L/month, want to retire at 60."*
Two things make the right tools fire:

- **Rich tool descriptions** — each `@mcp.tool` docstring says *when* to use it
  ("Use when a user asks how long to double their money"). The client model matches
  intent to description.
- **A meta-advisor** — `create_financial_plan` is an orchestrator tool that itself
  chains many calculators (net worth → cash flow → emergency fund → debt-to-income
  → risk profile → retirement gap) and returns one prioritised plan. It's the bridge
  from a free-form story to concrete numbers.

### 2.4 Transports

MCP can travel over different channels. This server supports all the common ones:

| Transport | Where it's used | URL/command |
|-----------|-----------------|-------------|
| **stdio** | Local: Claude Desktop / Code spawn the process | `python -m src` |
| **SSE** | Legacy remote (Server-Sent Events) | `run_production.py` |
| **streamable-HTTP** | Modern remote connector (one HTTP endpoint) | `/mcp` |

The hosted connector uses **streamable-HTTP** — a single endpoint that handles the
request/response and server-streamed messages over plain HTTPS.

---

## 3. Architecture

```
┌───────────────────────────────────────────────────────────────────────┐
│                          CLIENTS                                        │
│  Claude Desktop · Claude Code · Cursor/VS Code        Web browser       │
└───────────┬───────────────────────────────────────────────┬───────────┘
            │ MCP (streamable-HTTP / stdio)                  │ HTTPS
            ▼                                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│              UNIFIED SERVER  (src/web/server.py, one port)              │
│                                                                         │
│   /mcp  ──────────────►  FastMCP streamable-HTTP app                    │
│   /api/* ─────────────►  JSON endpoints (tools, calc, live data)        │
│   /     ──────────────►  StaticFiles → exported Next.js site (web/out)  │
│                                                                         │
│   SecurityMiddleware (headers/CSP, rate limit, body cap) wraps all      │
└───────────┬───────────────────────────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────────────────────────────────────┐
│   FastMCP server  (src/server.py)  — registers 13 tool modules         │
│                                                                         │
│   tvm · debt · planning · bonds · stocks · mutual_funds · portfolio     │
│   derivatives · india_savings · cashflow · risk_profile · advisor       │
│   marketdata (live)                                                     │
│                                                                         │
│   Each module:  pure functions  +  @mcp.tool wrappers (register(mcp))   │
└───────────┬───────────────────────────────────────────────────────────┘
            │ marketdata only
            ▼
   Public keyless APIs:  AMFI/mfapi (NAVs) · Frankfurter (FX) · Yahoo (quotes)
```

**Layering principle:** the deterministic pure functions are separate from the thin
MCP wrappers. That one decision lets the *same* function back the MCP tool, the web
`/api/calc` endpoint, and the unit tests — no duplicated maths.

### Repo layout

```
src/
├── server.py            FastMCP server, registers every tool module
├── __main__.py          `python -m src`  → stdio transport
├── tools/               pure math fns + register(mcp) wrappers (13 modules)
├── models/              Pydantic schemas + enums
├── utils/               output formatters
└── web/
    ├── server.py        unified Starlette app (/mcp + /api + static + security)
    └── __main__.py      `python -m src.web` → uvicorn (port 7860)

web/                     Next.js front-end (static export → web/out)
└── app/                 home, tools, calculator, dashboard, connect + components
```

---

## 4. End-to-end flows

### A. An AI calls a tool

```
Claude  ──initialize──►  /mcp
Claude  ──tools/list──►  /mcp           (reads 76 names + descriptions)
User: "EMI on a 50L loan at 8.5% for 20y?"
Claude  ──tools/call calculate_emi {principal:5000000, annual_rate:8.5, tenure_years:20}──►  /mcp
        FastMCP → debt.calculate_emi() pure fn → formatted text
Claude  ◄──result: "Monthly EMI ₹43,391.16 …"──
```

### B. The website calculator

```
Browser  ──POST /api/calc {calculator:"emi", params:{…}}──►  unified server
         SecurityMiddleware: rate-limit + body-cap
         run_calc(): _sanitize_params() (finite, magnitude + loop caps)
         → debt.calculate_emi() → JSON
Browser  ◄── {result:{emi:43391.16, …}} ──  → formatted with format.js (₹, %, ×)
```

### C. Live dashboard

```
Browser ──GET /api/quote?symbol=^NSEI──► server → marketdata.get_quote()
        → Yahoo Finance → {price, change_pct, currency} → rendered card
```

---

## 5. Security model

- **Stateless** — no DB, no sessions; every call independent and reproducible.
- **Transparent ASGI SecurityMiddleware** — adds CSP (with `frame-ancestors` for the
  HF embed), `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`,
  HSTS, COOP to every response. Implemented at the ASGI layer so it never buffers
  the streaming `/mcp` (SSE) responses.
- **Rate limiting** — per-IP sliding window on `/api/*`, with periodic pruning so the
  counter map can't grow without bound.
- **Input validation** — `/api/calc` requires finite numbers, caps magnitude, and
  bounds loop-driving parameters (years/months/age) to stop DoS via unbounded
  iteration. Live-data params are regex-validated.
- **CORS** — limited to GET/POST/OPTIONS, no credentials.
- **No secrets in the app** — live data is public and keyless; the only secret is the
  Hugging Face token, held as a GitHub Actions secret.

---

## 6. Deployment & hosting

### The pipeline

```
git push main ──► GitHub Actions
                  ├── CI: ruff + pytest (3.10 & 3.12) + build + tool-count check
                  ├── CodeQL: static analysis (python + JS/TS)
                  └── hf-sync: upload repo to the HF Space (generates Space README
                              frontmatter) → HF builds the Docker image → RUNNING
```

The multi-stage `Dockerfile` builds the Next.js site in a Node stage, copies the
static export into a Python stage, installs `.[web]`, and runs `python -m src.web`.

### Hosting it yourself (and on a portfolio site)

> **Can a static portfolio site host the MCP connector? No — and here's why.**

An MCP remote connector is a **running server process** that speaks HTTP. A static
host (GitHub Pages, Netlify/Vercel *static*, an S3 bucket) only serves files — there
is no process to answer `/mcp`. That's exactly the gap Hugging Face fills: a **Docker
Space runs the container**, keeps the process alive, and exposes a public HTTPS port
with TLS. The "server" is the part static hosting can't provide.

So you have two clean options:

1. **Reuse the existing connector from anywhere.** Your portfolio can be fully
   static and still *link to* or *embed* the tool. The connector URL
   `https://sarveshtalele-personal-finance-mcp.hf.space/mcp` already works in any MCP
   client — you don't need to re-host it. Embed the UI with an iframe:
   ```html
   <iframe src="https://sarveshtalele-personal-finance-mcp.hf.space/"
           style="width:100%;height:720px;border:0;border-radius:16px"></iframe>
   ```

2. **Self-host the server elsewhere** if you want it on your own domain. Any host that
   runs a long-lived container/process works — Render, Railway, Fly.io, a VPS, Google
   Cloud Run, AWS App Runner, Azure Container Apps. Steps:
   ```bash
   docker build -t personal-finance-mcp .
   # run on the host, expose port 7860 behind its TLS/proxy
   ```
   Your connector becomes `https://finance.yourdomain.com/mcp`. Point a CNAME/custom
   domain at the host. (Vercel/Netlify *Functions* can serve the JSON API but are a
   poor fit for the long-lived streaming `/mcp` session — prefer a container host.)

**Bottom line:** the MCP part needs a server, not a static site. Hugging Face (or any
container host) provides that server; your portfolio links to or embeds it, or you
move the same container to your own domain.

---

## 7. Is this enterprise-grade? Honest assessment

**Today it is a well-engineered, production-*ready hobby/portfolio* service** — clean
architecture, deterministic core, security headers, rate limiting, input validation,
CI + CodeQL + Dependabot, automated deploy, 129 tests. That is genuinely above
average for a side project.

It is **not yet enterprise-grade**, because "enterprise" implies guarantees this
single-container, single-region, unauthenticated service doesn't make yet. The gaps,
and how to close them for production:

### Reliability & scale
- **Single instance / single region.** Move to ≥2 replicas behind a load balancer;
  the app is already stateless, so horizontal scaling is easy. Add health/readiness
  probes (the Docker `HEALTHCHECK` is a start) and autoscaling.
- **In-memory rate limiter** doesn't share state across replicas. Back it with Redis
  (or an API gateway's rate limiting) so limits hold cluster-wide.
- **No caching** of live-data calls. Add a short-TTL cache (Redis/in-proc) + upstream
  timeouts/circuit-breakers so a slow third-party API can't degrade the service.

### Security & compliance
- **No authentication on `/mcp` or `/api`.** Fine for a public read-only calculator;
  for enterprise add OAuth2/API keys (MCP supports auth), per-key quotas, and audit
  logging. Put a WAF / API gateway in front.
- **Secrets** currently a single GitHub Actions token. Use a secret manager (Vault,
  AWS/GCP Secret Manager), short-lived tokens, and rotation (rotate the demo tokens).
- **Supply chain.** Pin dependencies (hashes/lockfile in CI), pin GitHub Actions to
  commit SHAs, sign images (cosign) and generate an SBOM, run container scanning.
- **CSP** uses `'unsafe-inline'` for scripts (required by static Next). For stricter
  CSP, serve with per-request nonces from a non-static renderer.

### Observability
- Add **structured logging**, **metrics** (Prometheus/OpenTelemetry), **tracing**, and
  dashboards/alerts (latency, error rate, rate-limit hits, upstream failures). Define
  **SLOs** and error budgets.

### Delivery & operations
- **Infrastructure as Code** (Terraform) and a real environment promotion path
  (dev → staging → prod) instead of push-to-main → prod.
- **Release management** — semantic versioning is in place; add changelogs, canary or
  blue-green deploys, and rollback automation.
- **Testing depth** — add load tests, contract tests for the MCP surface, coverage
  gates, and fuzzing for the calculators.
- **Data/SLA** — a status page, backups (none needed while stateless), and a defined
  incident process.

### Quick "level-up" order (highest ROI first)
1. Redis-backed rate limiting + response caching + upstream timeouts.
2. Auth on the API (keys/OAuth) + per-key quotas + audit log.
3. Observability (logs/metrics/traces + alerts) and health/readiness probes.
4. ≥2 replicas behind an LB + autoscaling; IaC for the whole stack.
5. Supply-chain hardening (pinned deps/actions, image signing, SBOM, scanning).

Close those and it moves from "solid portfolio project" to "enterprise production
service."

---

## 8. Quick reference

| Thing | Value |
|-------|-------|
| Connector URL | `https://sarveshtalele-personal-finance-mcp.hf.space/mcp` |
| Website | `https://sarveshtalele-personal-finance-mcp.hf.space/` |
| Local stdio | `python -m src` |
| Local full stack | `python -m src.web` (port 7860) |
| Tools | 76 across 13 categories |
| Transports | stdio · SSE · streamable-HTTP |

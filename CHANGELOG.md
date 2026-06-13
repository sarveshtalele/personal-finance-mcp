# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/), and the
project follows [Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-06-13 — Public launch 🚀

First public release of Personal Finance MCP: a deterministic personal-finance
toolkit exposed over the Model Context Protocol, with a website and a hosted
connector.

### Highlights
- **76 deterministic tools** across 13 categories: time value of money, debt &
  loans, cash-flow & budgeting, Indian small-savings (PPF/SSY/NSC/KVP/SCSS/RD/FD/
  EPF), goal & retirement planning, stock & bond valuation, derivatives, mutual
  funds, portfolio analytics, and risk profiling.
- **Meta-advisor** (`create_financial_plan`): routes a plain-language story to the
  right calculators and returns one prioritised plan.
- **Live market data** (keyless): mutual-fund NAVs (AMFI), FX (ECB), equity quotes (Yahoo).
- **Unified server**: MCP over streamable-HTTP at `/mcp`, a JSON API at `/api/*`,
  and a Next.js website (live calculator + market dashboard) on one port.
- **One connector URL** works in Claude Desktop, Claude Code, Cursor, Windsurf,
  Zed, Continue, and Cline.
- Deployed as a Hugging Face Docker Space, auto-synced from GitHub.

### Governance & correctness
- Single source of truth for asset allocation — `assess_risk_profile` and
  `suggest_asset_allocation` can never disagree.
- Server instructions forbid fabricated figures; tools return the formula used.

### Security
- Stateless service; per-IP rate limiting with memory pruning; request-body cap;
  bounded calculator inputs (DoS protection); CSP + HSTS + security headers;
  validated live-data parameters; CORS limited to GET/POST.

### Quality & delivery
- 137 tests; CI on Python 3.10 + 3.12 with ruff + build; CodeQL + Dependabot;
  branch protection on `main`; automated GitHub → Hugging Face deploy.
- Accessibility: focus-visible rings, skip link, ARIA labels, reduced-motion support.

> Note: development builds 1.0.2 / 1.1.0 were published to PyPI before this public
> 1.0.0 launch; `pip` may resolve a higher development build until the line is
> reconciled.

[1.0.0]: https://github.com/sarveshtalele/personal-finance-mcp/releases/tag/v1.0.0

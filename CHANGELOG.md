# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/), and the
project follows [Semantic Versioning](https://semver.org/).

## [1.1.1] — 2026-06-13

### Fixed
- **Allocation consistency (governance).** `assess_risk_profile` and
  `suggest_asset_allocation` now share a single allocation engine, so the same
  person can never receive two different equity/debt/gold splits.
- `suggest_asset_allocation` accepts `monthly_investment` and returns exact
  per-bucket monthly amounts, plus a presentation note.

### Added
- **GOVERNANCE** block in the MCP server instructions: use only tool numbers,
  present them verbatim, never fabricate funds/returns/tax/projections, surface
  conflicts instead of silently choosing.
- Favicon, Open Graph image, branded 404 page, root changelog, `.env.example`.
- Accessibility labels on calculator controls; on-page "not advice" disclaimers.

### Security / SDLC
- Rate-limiter memory pruning; HSTS + COOP headers; sanitized API errors.
- CI fixed and expanded (Python 3.10 + 3.12, build step); CodeQL + Dependabot.
- Branch protection on `main`.

## [1.1.0] — 2026-06-12

### Added
- Grew from 54 to **76 deterministic tools**: derivatives, Indian small-savings
  (PPF/SSY/NSC/KVP/SCSS/RD/FD/EPF), cash-flow & budgeting, risk profiling, and a
  `create_financial_plan` meta-advisor that routes a plain-language story to tools.
- **Live market data** tools (AMFI NAVs, ECB FX, Yahoo quotes) — keyless.
- **Unified server** serving the MCP connector (`/mcp`, streamable-HTTP), a JSON
  API (`/api/*`), and a **Next.js website** (calculator + market dashboard) on one port.
- Docker image + Hugging Face Space deployment, auto-synced from GitHub.
- Security hardening: input validation/bounds, rate limiting, security headers, CSP.

## [1.0.2] — earlier

- Initial public release: 54 deterministic personal-finance calculators over MCP
  (stdio), published to PyPI.

[1.1.1]: https://github.com/sarveshtalele/personal-finance-mcp/releases/tag/v1.1.1
[1.1.0]: https://github.com/sarveshtalele/personal-finance-mcp/releases/tag/v1.1.0

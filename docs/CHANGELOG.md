# Development Log

## 2026-04-11 — Registry Release Preparation

### Built
- **Anthropic Registry configuration** (`server.json`) — added standard mcp schema payload matching `pypi` repository expectations.
- **`dist/` Build** — successfully built wheel and source distributions via `uv build` for prospective PyPI upload.

### Documentation
- **`docs/anthropic.md`** — comprehensive, Python-specific instructions mirroring the TypeScript MCP-Registry Quickstart.
- **`docs/documentation.md`** — formalized mathematical equations and standalone architecture descriptions.
- **`README.md`** — refined documentation and tool references.

### Refined
- Applied `ruff format` and `ruff check --fix` over the entire `src/` hierarchy.
- Resolved multiple hidden implicit `F821` linting errors maintaining 100% test passage stability across 102 individual constraints.

---


## 2026-04-11 — v1.1.0 — Completion & Polish

### Added
- **Integration test suite** (`test_integration.py`) — 18 new tests
  - Server registration verification for all 54 tools across 7 categories
  - Output format validation (reference labels, currency formatting, formulas)
  - End-to-end scenario tests: retirement planning, debt analysis, SIP/goal, portfolio
- **`__main__.py`** — enables `python -m src` server startup
- **`Dockerfile`** — production container with healthcheck
- **`run_production.py`** — SSE server launcher with CLI args and env var support
- **`.gitignore`** — standard Python project ignores
- **`LICENSE`** — MIT license
- **Comprehensive `README.md`** — badges, full 54-tool catalog, example output, architecture, deployment table

### Fixed
- `config/claude_desktop.json` — updated with actual machine path
- `README.md` — replaced minimal stub with professional documentation

### Validated
- All 100+ tests passing (86 unit + 18 integration)
- 54 tools registered and verified
- Server starts correctly via `python -m src`, `python -m src.server`, and `personal-finance-mcp` CLI

---

## 2026-04-11 — v1.0.0 — Initial Release

### Built
- Complete MCP server with **54 financial tools** across 7 categories
- All calculations based on standard, deterministic financial formulas
- Stateless design — no database, no session storage

### Architecture
- **Layered design**: Tools → Calculators → Models
- Calculators are pure functions (no side effects, deterministic)
- Tools wrap calculators with MCP interface and formatting
- Pydantic models for input validation

### Tool Categories Implemented
| Category | Tools | Topic |
|----------|-------|-------|
| Time Value of Money | 10 | Compounding, annuities, perpetuities |
| Debt Management | 6 | EMI, amortization, prepayment |
| Financial Planning | 9 | Net worth, ratios, retirement |
| Bond Analysis | 6 | Pricing, YTM, duration |
| Stock Valuation | 5 | DDM, DCF, P/E |
| Mutual Funds | 7 | SIP, SWP, CAGR, NAV |
| Portfolio Analytics | 11 | MPT, CAPM, risk-adjusted return |

### Key Formulas Implemented
- TVM: FV, PV, Annuity (ordinary/due), Perpetuity (simple/growing), EAR, Fisher equation
- Debt: EMI, Amortization schedule, Prepayment impact, Invest vs Prepay analysis
- Ratios: Savings, DTI, Liquidity, Solvency, 50/30/20 budget rule
- Bonds: DCF pricing, YTM (Newton-Raphson), Duration (Macaulay/Modified), Convexity
- Stocks: Gordon Growth DDM, Two-stage DDM, P/E with PEG, DCF/WACC
- MF: SIP (with step-up), SWP, Lumpsum vs SIP, CAGR, NAV, Expense ratio impact
- Portfolio: MPT (return/risk), CAPM, Sharpe, Treynor, Jensen's Alpha, Information Ratio, Sortino
- Planning: Retirement, Education, Insurance (HLV), Emergency fund, Financial health score

### Testing
- **86 unit tests** — all passing
- Tests verify against hand-calculated reference values
- Coverage across all 7 calculator modules

### Tech Stack
- Python 3.12, MCP SDK (FastMCP), Pydantic 2.x
- Transport: stdio (Claude Desktop) + SSE (remote)
- No external API dependencies — fully offline capable

### Files Created
```
19 source files (src/)
7 test files (tests/)
6 documentation files (docs/)
4 project files (Plan.md, Architecture.md, log.md, README.md)
2 config files (pyproject.toml, claude_desktop.json)
```

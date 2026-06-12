---
title: Personal Finance MCP
emoji: 💰
colorFrom: green
colorTo: teal
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# 💰 Personal Finance MCP Server

mcp-name: io.github.sarveshtalele/personal-finance

> **Deterministic personal finance calculator** powered by [Model Context Protocol](https://modelcontextprotocol.io/) — based on the **Core Financial Principles**.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![MCP SDK](https://img.shields.io/badge/MCP-1.0+-blueviolet)](https://modelcontextprotocol.io/)
[![PyPI](https://img.shields.io/pypi/v/personal-finance-mcp?color=blue)](https://pypi.org/project/personal-finance-mcp/)
[![Tests](https://img.shields.io/badge/tests-100%25_passing-brightgreen)](tests/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## ✨ What It Does

Connect this server to **Claude Desktop**, **Claude Code**, or any MCP client to get **76 financial tools** with:

- 🔢 **Deterministic outputs** — same inputs → same results, always
- 📖 **Theory-grounded** — every formula traced to the NISM Investment Adviser (Level 1) curriculum
- 📐 **Full formula display** — shows the exact calculation, not just the answer
- 🇮🇳 **Indian finance context** — ₹ formatting, PPF/SSY/NSC/EPF, SIP, EMI
- 🤖 **Story → tools** — describe your situation; `create_financial_plan` routes you to the right calculators
- 🛰️ **Live market data** — mutual-fund NAVs (AMFI), FX (ECB), index quotes — no API keys
- 🌐 **Website + connector** — a Next.js site (calculators + live dashboard) and an MCP endpoint, deployable to Hugging Face

### Website & Hugging Face deployment

The unified server (`python -m src.web`) serves everything on one port:

| Path | What |
|------|------|
| `/` | The Next.js website (tool catalog, live calculator, market dashboard, setup guide) |
| `/mcp` | The MCP server over **streamable-HTTP** — use this URL as a connector |
| `/api/*` | JSON endpoints powering the site (tool catalog, calculators, live data) |

Deploy as a **Docker Space** on Hugging Face (`sdk: docker`, `app_port: 7860`). Your connector URL becomes `https://<user>-<space>.hf.space/mcp`. See [docs/deployment.md](docs/deployment.md).

---

## 📦 Quick Start

### 1. Connect to Claude Desktop (Zero-Install Method)

Because this tool is globally published to PyPI, you don't even need to download the code to use it. Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "personal-finance": {
      "command": "uvx",
      "args": [
        "personal-finance-mcp"
      ]
    }
  }
}
```

> **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
> **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

Restart Claude Desktop, and you will see the integration automatically.

### 2. Manual Global Installation

If you'd like to use it natively from your terminal without `uv`, just install it via standard `pip`:

```bash
pip install personal-finance-mcp

# Starts the server!
personal-finance-mcp
```

---

## 🛠 Tool Categories (54 Tools)

### 📊 Time Value of Money — 10 tools
| Tool | Description |
|------|-------------|
| `calculate_future_value` | FV with any compounding frequency |
| `calculate_present_value` | Discount future cash flows to today |
| `calculate_annuity_fv` | Future value of regular payments (SIP) |
| `calculate_annuity_pv` | Present value of regular payments |
| `calculate_perpetuity` | Value of infinite periodic payments |
| `calculate_rule_of_72` | Quick doubling time estimate |
| `calculate_effective_rate` | Nominal → Effective Annual Rate |
| `calculate_real_return` | Inflation-adjusted return (Fisher) |
| `calculate_inflation_impact` | Future cost after inflation |
| `calculate_savings_needed` | Monthly savings for a target corpus |

### 💳 Debt Management — 6 tools
| Tool | Description |
|------|-------------|
| `calculate_emi` | EMI for any loan |
| `loan_amortization` | Month-wise principal/interest split |
| `compare_loans` | Side-by-side loan comparison |
| `calculate_prepayment_savings` | Interest saved by prepaying |
| `invest_or_prepay_loan` | Should you invest or prepay? |
| `analyze_debt_consolidation` | Should you consolidate debts? |

### 📋 Financial Planning — 9 tools
| Tool | Description |
|------|-------------|
| `calculate_net_worth` | Assets - Liabilities statement |
| `analyze_financial_ratios` | Savings, DTI, liquidity, solvency |
| `calculate_emergency_fund` | Recommended buffer size |
| `analyze_budget` | 50/30/20 rule analysis |
| `plan_financial_goal` | Goal setting with inflation adjustment |
| `plan_retirement` | Retirement corpus & SIP calculator |
| `plan_education` | Child education fund planner |
| `calculate_insurance_need` | Human Life Value method |
| `financial_health_check` | 0-100 health score with rating |

### 📈 Bond Analysis — 6 tools
| Tool | Description |
|------|-------------|
| `calculate_bond_price` | DCF bond pricing |
| `calculate_ytm` | Yield to Maturity (Newton-Raphson) |
| `calculate_current_yield` | Annual coupon / market price |
| `calculate_bond_duration` | Macaulay & Modified Duration |
| `calculate_bond_convexity` | Second-order interest rate risk |
| `calculate_zero_coupon_bond` | Zero-coupon bond pricing |

### 📊 Stock Valuation — 5 tools
| Tool | Description |
|------|-------------|
| `value_stock_ddm` | Gordon Growth Model |
| `value_stock_two_stage_ddm` | Two-stage DDM |
| `value_stock_pe` | P/E relative valuation + PEG |
| `value_stock_dcf` | Discounted Cash Flow |
| `calculate_dividend_yield` | Dividend yield % |

### 🏦 Mutual Funds — 7 tools
| Tool | Description |
|------|-------------|
| `calculate_sip_returns` | SIP calculator with step-up |
| `calculate_sip_needed` | Monthly SIP for a target corpus |
| `compare_lumpsum_vs_sip` | Lump sum vs SIP comparison |
| `analyze_expense_ratio_impact` | How expense ratio erodes returns |
| `calculate_swp` | Systematic Withdrawal Plan duration |
| `calculate_cagr` | Compound Annual Growth Rate |
| `calculate_nav` | Net Asset Value calculation |

### 📊 Portfolio Analytics — 11 tools
| Tool | Description |
|------|-------------|
| `calculate_portfolio_return` | Weighted expected return |
| `calculate_portfolio_risk` | Portfolio variance & std deviation |
| `analyze_two_asset_portfolio` | Two-asset analysis + min variance |
| `calculate_capm_return` | CAPM expected return |
| `calculate_sharpe_ratio` | Risk-adjusted return (total risk) |
| `calculate_treynor_ratio` | Risk-adjusted return (systematic) |
| `calculate_jensens_alpha` | Manager skill measurement |
| `calculate_information_ratio` | Consistency vs benchmark |
| `calculate_sortino_ratio` | Downside-risk-adjusted return |
| `suggest_asset_allocation` | Age & risk-based allocation |
| `rebalance_portfolio` | Trades needed for target allocation |

---

## 💬 Example Usage in Claude

```
"Calculate EMI for a 50 lakh home loan at 8.5% for 20 years"
```

Output:
```
══════════════════════════════════════════════════
  EMI Calculation
══════════════════════════════════════════════════
  Emi: ₹43,391.16
  Total Payment: ₹1,04,13,878.40
  Total Interest: ₹54,13,878.40
  Interest To Principal Ratio: 1.0828
  Principal: ₹50,00,000.00
  Annual Rate: 8.5%
  Tenure Months: 240

  Formula: EMI = 50,00,000.00 × 0.007083 × (1+0.007083)^240 / ((1+0.007083)^240 - 1)

  
```

---

## 🏗 Architecture

```
Tools Layer  ───────→  Models Layer
     │                      │
  MCP interface        Pydantic validation
  + core math               + enums
```

- **Tools**: FastMCP wrappers + deterministic mathematical functions.
- **Models**: Pydantic schemas for strict input validation.

See [docs/Architecture.md](docs/Architecture.md) for full details.

---

## 📁 Project Structure

```
personal-finance-mcp/
├── src/
│   ├── server.py              # MCP server entry point
│   ├── __main__.py            # python -m src entry point
│   ├── tools/                 # Pure math & MCP wrappers
│   │   ├── tvm.py             # Time Value of Money
│   │   ├── debt.py            # EMI, amortization
│   │   ├── planning.py        # Financial ratios, health score
│   │   ├── bonds.py           # Bond pricing, YTM, duration
│   │   ├── stocks.py          # DDM, DCF, P/E valuation
│   │   ├── mutual_funds.py    # SIP, SWP, CAGR, NAV
│   │   └── portfolio.py       # MPT, CAPM, Sharpe, alpha
│   ├── models/                # Pydantic validation schemas
│   │   ├── schemas.py         # Type definitions & constraints
│   │   └── enums.py           # Validation Enums
│   └── utils/                 # Formatters & helpers
├── tests/                     # 100+ unit & integration tests
├── docs/                      # documentation & architecture
├── Dockerfile                 # Container deployment
├── run_production.py          # SSE server launcher
├── pyproject.toml             # Package configuration
└── LICENSE                    # MIT License
```

---

## 🚀 Deployment Options

| Method | Transport | Use Case |
|--------|-----------|----------|
| Claude Desktop | stdio | Personal use — simplest |
| Claude Code | stdio | Development / coding |
| SSE Server | HTTP | Remote clients, team use |
| Docker | HTTP | Production deployment |

See [docs/deployment.md](docs/deployment.md) for full instructions.

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [docs/documentation.md](docs/documentation.md) | Full tool reference with formulas |
| [docs/setup.md](docs/setup.md) | Installation & connection guide |
| [docs/testing.md](docs/testing.md) | Test structure & running tests |
| [docs/deployment.md](docs/deployment.md) | Local, SSE, Docker deployment |
| [docs/Architecture.md](docs/Architecture.md) | System design & data flow |

---

## 🔑 Key Design Decisions

1. **Stateless** — No database, no sessions. Every tool call is self-contained.
2. **Deterministic** — Pure math, no randomness, no AI inference for numbers.
3. **Layered** — Tools → Calculators → Models, each with single responsibility.
4. **Offline-first** — Zero external API calls. Works without internet.
5. **Theory-grounded** — Every formula is mathematically deterministic.



## Setup Guide

### Prerequisites

- **Python 3.10+** (3.12 recommended)
- **uv** (recommended) or pip
- **Claude Desktop** or any MCP-compatible client

### Installation

#### Global Installation

Because this tool is globally published to PyPI, you don't even need to download the code to use it if you are using modern tools.

##### Option 1: Zero-Install (using uvx)
If you have `uv` installed, it can dynamically fetch and run the package:
```bash
uvx personal-finance-mcp
```

##### Option 2: Global Pipeline (using pip)
To natively install the executable into your python ecosystem:
```bash
pip install personal-finance-mcp
```

### Connect to Claude Desktop

1. Open Claude Desktop settings → Developer → Edit Config
2. Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "personal-finance": {
      "command": "uvx",
      "args": [
        "personal-finance-mcp"
      ]
    }
  }
}
```

*Note: If you don't use `uv`, you can replace `"uvx"` with `"python"` and `"args": ["-m", "personal_finance_mcp"]`.*

3. Restart Claude Desktop
4. You should see the hammer icon with 54 tools available

### Connect to Claude Code

Claude Code auto-discovers MCP servers. Add to your project's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "personal-finance": {
      "command": "uvx",
      "args": [
        "personal-finance-mcp"
      ]
    }
  }
}
```

### Run as Standalone Server (SSE)

For remote MCP clients:

```bash
# If installed normally:
python -c "from src.server import mcp; mcp.run(transport='sse')"
```

Server starts at `http://127.0.0.1:8000/sse`.

### Verify Installation

```bash
# Run tests
pytest tests/ -v

# Quick smoke test
python -c "from src.server import mcp; print(f'{len(mcp._tool_manager._tools)} tools loaded')"
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp[cli]` | >=1.0.0 | MCP Python SDK |
| `pydantic` | >=2.0.0 | Input validation |
| `pytest` | >=7.0 (dev) | Testing |

### Troubleshooting

#### "ModuleNotFoundError: No module named 'src'"
If you're running locally from source, ensure you installed with the `-e` (editable) flag: `uv pip install -e ".[dev]"`

#### Claude Desktop doesn't show tools
- Check the path in config is absolute and correct
- Restart Claude Desktop completely
- Check `~/Library/Logs/Claude/mcp*.log` on macOS for errors

#### Import errors
```bash
# Verify the package is installed correctly
python -c "from src.calculators.tvm import future_value; print(future_value(100000, 12, 10, 12))"
```
---

## 📄 License

[MIT](LICENSE) — free to use, modify, and distribute.

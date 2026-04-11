# Personal Finance MCP Server - Project Plan

## Overview
A stateless Model Context Protocol (MCP) server built in Python that provides deterministic personal finance calculations based on the Complete Financial Planning MVP curriculum. Connectable from Claude Desktop, any MCP client, or programmatically.

## Goals
1. Implement all financial calculations from MVP IAA Level 1 workbook as MCP tools
2. Provide deterministic, auditable outputs (no AI hallucination for numbers)
3. Offer financial planning advice grounded in textbook theory
4. Stateless design (no database), with optional Claude memory integration
5. Production-ready with full documentation, testing, and deployment guides

## Modules (Mapped to MVP Book Chapters)

### Module 1: Personal Financial Planning
| Tool | Source Chapter | Description |
|------|---------------|-------------|
| `time_value_of_money` | Ch 2 | FV, PV, annuity, perpetuity, compounding |
| `financial_position` | Ch 3 | Net worth, budget, savings plan, financial ratios |
| `goal_planner` | Ch 1,3 | Goal setting, prioritization, corpus calculation |
| `debt_analyzer` | Ch 4 | EMI, amortization, debt ratios, loan comparison |
| `budget_planner` | Ch 3 | Cash flow management, budget creation |
| `emergency_fund` | Ch 3 | Emergency fund calculator |

### Module 2: Investment Analysis
| Tool | Source Chapter | Description |
|------|---------------|-------------|
| `stock_valuation` | Ch 8 | DCF, DDM, P/E, relative valuation |
| `bond_calculator` | Ch 9 | Bond pricing, YTM, duration, convexity |
| `mutual_fund_analyzer` | Ch 11 | NAV, SIP returns, expense ratio impact |

### Module 3: Portfolio Management
| Tool | Source Chapter | Description |
|------|---------------|-------------|
| `portfolio_analyzer` | Ch 14,15 | Expected return, risk, correlation, optimization |
| `portfolio_performance` | Ch 16 | Sharpe, Treynor, Jensen's alpha, CAGR, XIRR |
| `asset_allocation` | Ch 15 | Strategic/tactical allocation, rebalancing |

### Module 4: Comprehensive Planning
| Tool | Source Chapter | Description |
|------|---------------|-------------|
| `retirement_planner` | Ch 1,2 | Retirement corpus, withdrawal strategy |
| `education_planner` | Ch 1,2 | Education fund planning |
| `insurance_needs` | Ch 1 | HLV method, insurance gap analysis |
| `tax_efficiency` | Ch 17 | Tax-efficient investment suggestions |
| `financial_health_check` | All | Comprehensive financial health score |

## Phases

### Phase 1: Core Engine (Current)
- Time Value of Money calculator
- Financial ratios & position analysis
- Debt/loan calculator
- Goal planner
- MCP server setup with stdio transport

### Phase 2: Investment Tools
- Stock valuation models
- Bond pricing & yield calculator
- Mutual fund analyzer

### Phase 3: Portfolio Tools
- Portfolio risk/return analysis
- Performance measurement
- Asset allocation advisor

### Phase 4: Comprehensive Planning
- Retirement planner
- Education planner
- Financial health check
- Insurance needs analysis

## Technical Stack
- **Language**: Python 3.10+
- **MCP SDK**: `mcp[cli]` (official Python SDK)
- **Transport**: stdio (Claude Desktop compatible), SSE (remote)
- **Math**: Python `math`, `decimal` for precision
- **Testing**: `pytest`
- **Packaging**: `pyproject.toml` with `uv` or `pip`

## Timeline
- Phase 1: Core engine + MCP server scaffold
- Phase 2: Investment calculation tools
- Phase 3: Portfolio management tools
- Phase 4: Comprehensive planners + documentation + deployment

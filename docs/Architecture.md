# Architecture - Personal Finance MCP Server

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    MCP Clients                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐    │
│  │  Claude  │  │  Claude  │  │  Custom MCP Client   │    │
│  │  Desktop │  │   Code   │  │  (Python/TS/etc)     │    │
│  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘    │
│       │             │                   │                │
└───────┼─────────────┼───────────────────┼────────────────┘
        │ stdio       │ stdio             │ SSE/stdio
        ▼             ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│                 MCP Server Layer                         │
│  ┌────────────────────────────────────────────────────┐  │
│  │              server.py (FastMCP)                   │  │
│  │  - Tool registration & routing                     │  │
│  │  - Input validation (Pydantic models)              │  │
│  │  - Response formatting                             │  │
│  └──────────────────┬─────────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼────────────────────────────────┐   │
│  │              Tools Layer (tools/)                 │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │   │
│  │  │ TVM      │ │ Debt     │ │ Goal Planner     │   │   │
│  │  │ Tools    │ │ Tools    │ │ Tools            │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │   │
│  │  ┌────┴─────┐ ┌────┴─────┐ ┌────────┴─────────┐   │   │
│  │  │ Bond     │ │ Stock    │ │ Portfolio        │   │   │
│  │  │ Tools    │ │ Tools    │ │ Tools            │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │   │
│  │  ┌────┴─────┐ ┌────┴─────┐ ┌────────┴─────────┐   │   │
│  │  │ MF       │ │ Budget   │ │ Retirement       │   │   │
│  │  │ Tools    │ │ Tools    │ │ Tools            │   │   │
│  │  └──────────┘ └──────────┘ └──────────────────┘   │   │
│  └──────────────────┬────────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼────────────────────────────────┐   │
│  │          Calculators Layer ()                     │.  │
│  │  Pure functions, no side effects, deterministic   │   │
│  │  ┌─────────────┐  ┌──────────────┐                │   │
│  │  │ tvm.py      │  │ debt.py      │                │   │
│  │  │ FV/PV/PMT   │  │ EMI/Amort    │                │   │
│  │  └─────────────┘  └──────────────┘                │   │
│  │  ┌─────────────┐  ┌──────────────┐                │   │
│  │  │ bonds.py    │  │ portfolio.py │                │   │
│  │  │ Price/YTM   │  │ Risk/Return  │                │   │
│  │  └─────────────┘  └──────────────┘                │   │
│  │  ┌─────────────┐  ┌──────────────┐                │   │
│  │  │ stocks.py   │  │ ratios.py    │                │   │
│  │  │ DCF/DDM     │  │ Fin. Ratios  │                │   │
│  │  └─────────────┘  └──────────────┘                │   │
│  └──────────────────┬────────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼────────────────────────────────┐   │
│  │              Models Layer (models/)               │   │
│  │  Pydantic models for input validation & output    │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ inputs.py  - Request schemas                 │ │   │
│  │  │ outputs.py - Response schemas                │ │   │
│  │  │ enums.py   - Frequency, CompoundType, etc.   │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  └───────────────────────────────────────────────────┘   │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Utils Layer (utils/)                 │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ formatters.py - Currency/percentage format   │ │   │
│  │  │ validators.py - Business rule validation     │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  └───────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. Stateless
- No database, no session storage
- Every tool call is self-contained with all required inputs
- Claude memory can optionally store user context between sessions

### 2. Deterministic
- All calculations use exact formulas from MVP textbook
- No randomness, no AI inference for numerical outputs
- Same inputs always produce same outputs
- Uses Python `float` with controlled rounding (2 decimal places for currency)

### 3. Layered Architecture
```
Tools → Calculators → Models
  │          │           │
  │          │           └── Data validation & structure
  │          └── Pure math functions
  └── MCP interface, formatting, context
```

### 4. Single Responsibility
- **Calculators**: Pure math. No formatting, no MCP awareness.
- **Tools**: MCP tool definitions. Calls calculators, formats output.
- **Models**: Pydantic schemas. Validation only.

## Data Flow

```
Client Request (JSON)
       │
       ▼
  MCP Server (FastMCP)
       │
       ▼
  Tool Function
       │ validates via Pydantic
       ▼
  Calculator Function(s)
       │ pure math
       ▼
  Result Dict
       │ formatted to string
       ▼
  MCP Response (text)
```

## Tool Categories & Count

| Category | Tools | Calculator Module |
|----------|-------|-------------------|
| Time Value of Money | 6 | `tvm.py` |
| Debt & Loans | 4 | `debt.py` |
| Financial Position | 4 | `ratios.py` |
| Goal Planning | 3 | `tvm.py` + `ratios.py` |
| Bond Analysis | 4 | `bonds.py` |
| Stock Valuation | 3 | `stocks.py` |
| Mutual Funds | 3 | `mutual_funds.py` |
| Portfolio Analysis | 4 | `portfolio.py` |
| Comprehensive Plans | 4 | Multiple |
| **Total** | **~35** | |

## File Structure
```
personal-finance-mcp/
├── pyproject.toml          # Package config, dependencies
├── README.md
├── Plan.md
├── Architecture.md
├── log.md
├── docs/
│   ├── documentation.md
│   ├── setup.md
│   ├── testing.md
│   └── deployment.md
├── config/
│   └── claude_desktop.json  # Example Claude Desktop config
├── src/
│   ├── __init__.py
│   ├── server.py            # MCP server entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py         # Enumerations
│   │   └── schemas.py       # Pydantic models
│   ├── 
│   │   ├── __init__.py
│   │   ├── tvm.py           # Time Value of Money
│   │   ├── debt.py          # Debt & Loan calculations
│   │   ├── ratios.py        # Financial ratios
│   │   ├── bonds.py         # Bond pricing & yields
│   │   ├── stocks.py        # Stock valuation
│   │   ├── mutual_funds.py  # MF calculations
│   │   └── portfolio.py     # Portfolio analytics
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── tvm_tools.py
│   │   ├── debt_tools.py
│   │   ├── planning_tools.py
│   │   ├── bond_tools.py
│   │   ├── stock_tools.py
│   │   ├── mf_tools.py
│   │   ├── portfolio_tools.py
│   │   └── comprehensive_tools.py
│   └── utils/
│       ├── __init__.py
│       └── formatters.py
└── tests/
    ├── __init__.py
    ├── test_tvm.py
    ├── test_debt.py
    ├── test_ratios.py
    ├── test_bonds.py
    ├── test_stocks.py
    ├── test_mutual_funds.py
    ├── test_portfolio.py
    └── test_integration.py
```

## MCP Protocol Details

### Transport
- **Primary**: stdio (for Claude Desktop / Claude Code)
- **Secondary**: SSE over HTTP (for remote clients)

### Tool Schema
Each tool is defined with:
- `name`: snake_case identifier
- `description`: What it calculates + which MVP chapter it's from
- `inputSchema`: JSON Schema (generated from Pydantic)
- Returns: Formatted text with calculations, formulas used, and advisory notes

### Example Tool Response Format
```
═══ Future Value Calculation ═══

Inputs:
  Present Value: ₹1,00,000
  Rate: 12.00% p.a.
  Period: 10 years
  Compounding: Monthly

Result:
  Future Value: ₹3,30,038.69

Formula Used:
  FV = PV × (1 + r/n)^(n×t)
  FV = 1,00,000 × (1 + 0.12/12)^(12×10)

Advisory Note:
  At 12% annual return with monthly compounding,
  your investment grows 3.30x over 10 years.
  The power of compounding adds ₹1,10,038.69
  beyond simple interest (₹1,20,000).

Reference: MVP IAA Level 1, Chapter 2 - Time Value of Money
```

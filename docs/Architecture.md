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
│  │              Tools Layer (src/tools/)             │   │
│  │  (Contains BOTH pure math logic & MCP wrappers)   │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │   │
│  │  │ tvm.py   │ │ debt.py  │ │ planning.py      │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │   │
│  │  ┌────┴─────┐ ┌────┴─────┐ ┌────────┴─────────┐   │   │
│  │  │ bonds.py │ │ stocks.py│ │ portfolio.py     │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │   │
│  │               ┌────┴─────┐                    │   │
│  │               │ mutual_  │                    │   │
│  │               │ funds.py │                    │   │
│  │               └──────────┘                    │   │
│  └──────────────────┬────────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────▼────────────────────────────────┐   │
│  │              Models Layer (src/models/)           │   │
│  │  Pydantic models for input validation & output    │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ schemas.py - Request/Response schemas        │ │   │
│  │  │ enums.py   - Validation Enumerators          │ │   │
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
Tools ─────────────→ Models
  │                     │
  │                     └── Data validation & structure
  └── MCP interface, formatting, & pure mathematical calculations
```

### 4. Single Responsibility
- **Tools**: Houses both the core mathematical logic and the MCP tool definition that formats outputs.
- **Models**: Pydantic schemas. Validation only.

## Data Flow

```
Client Request (JSON)
       │
       ▼
  MCP Server (FastMCP)
       │
       ▼
  Tool Function (src/tools/)
       │ 1. Validates inputs via Pydantic Schemas
       │ 2. Computes pure deterministic mathematics
       │ 3. Formats results to structured string
       ▼
  MCP Response (text)
```

## Tool Categories & Count

| Category | Tools | Target Module |
|----------|-------|-------------------|
| Time Value of Money | 10 | `tvm.py` |
| Debt & Loans | 6 | `debt.py` |
| Financial Planning | 9 | `planning.py` |
| Bond Analysis | 6 | `bonds.py` |
| Stock Valuation | 5 | `stocks.py` |
| Mutual Funds | 7 | `mutual_funds.py` |
| Portfolio Analysis | 11 | `portfolio.py` |
| **Total** | **54** | All combined within `src/tools/` |

## File Structure
```
personal-finance-mcp/
├── pyproject.toml          # Package config, dependencies
├── README.md
├── docs/
│   ├── Architecture.md      # System design
│   ├── CHANGELOG.md         # Development log
│   ├── documentation.md
│   ├── setup.md
│   ├── testing.md
│   └── deployment.md
├── src/
│   ├── __init__.py
│   ├── server.py            # FastMCP server entry point
│   ├── __main__.py          # python -m module execution
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py         # Enumerations
│   │   └── schemas.py       # Pydantic validation schemas
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── tvm.py           # Time Value of Money (Logic + MCP)
│   │   ├── debt.py          # Debt & Loan calculations
│   │   ├── planning.py      # Financial tools & Health checks
│   │   ├── bonds.py         # Bond pricing & yields
│   │   ├── stocks.py        # Stock valuation
│   │   ├── mutual_funds.py  # MF calculations
│   │   └── portfolio.py     # Portfolio analytics
│   └── utils/
│       ├── __init__.py
│       └── formatters.py    # Monetary display mapping
└── tests/
    ├── __init__.py
    ├── test_tvm.py
    ├── test_debt.py
    ├── test_planning.py
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

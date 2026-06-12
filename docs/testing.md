# Testing Guide

## Test Structure

```
tests/
├── test_tvm.py           # 16 tests — Time Value of Money
├── test_debt.py          # 11 tests — Debt & Loan calculations
├── test_ratios.py        #  9 tests — Financial ratios & health score
├── test_bonds.py         # 10 tests — Bond pricing & yields
├── test_stocks.py        #  8 tests — Stock valuation models
├── test_mutual_funds.py  # 11 tests — MF/SIP calculations
├── test_portfolio.py     # 19 tests — Portfolio analytics
├── test_integration.py   # 18 tests — Server registration, output format, E2E scenarios
└── (total: 102 tests)
```

## Running Tests

```bash
# Activate environment
source .venv/bin/activate

# Run all tests
pytest tests/ -v

# Run a specific module
pytest tests/test_tvm.py -v

# Run a specific test class
pytest tests/test_portfolio.py::TestSharpeRatio -v

# Run with coverage (install pytest-cov first)
pytest tests/ --cov=src --cov-report=term-missing
```

## Test Categories

### Unit Tests (Calculator Layer)
Each calculator module has its own test file. Tests verify:
- **Correctness**: Output matches hand-calculated reference values
- **Edge cases**: Zero rates, negative values, boundary conditions
- **Error handling**: Invalid inputs (growth > return, zero denominators)
- **Consistency**: Inverse operations produce original values

### Examples of Verified Calculations

| Test | Input | Expected | Method |
|------|-------|----------|--------|
| FV annual | PV=1L, r=10%, t=5y | ₹1,61,051 | Compound interest |
| FV monthly | PV=1L, r=12%, t=10y | ₹3,30,038.69 | Compound interest |
| EMI | P=50L, r=8.5%, t=20y | ₹43,391.16 | Amortized loan |
| Bond price | FV=1000, c=8%, YTM=10%, t=5y | ₹922.78 | DCF pricing |
| CAPM | Rf=6%, β=1.2, Rm=15% | 16.8% | CAPM |
| Sharpe | Rp=15%, Rf=6%, σ=8% | 1.125 | Sharpe ratio |
| DDM | D0=5, g=8%, r=15% | ₹77.14 | Gordon growth |

## Adding New Tests

Follow the pattern:

```python
from src.calculators.module_name import function_name

class TestFunctionName:
    def test_basic_case(self):
        result = function_name(inputs...)
        assert result["key"] == expected_value

    def test_edge_case(self):
        result = function_name(edge_inputs...)
        assert "error" in result or result["key"] satisfies condition
```

## Integration Testing

Test MCP tool layer (tools call calculators and format output):

```python
# Quick integration test
python -c "
from src.server import mcp
import asyncio

async def test():
    tools = mcp._tool_manager._tools
    # Verify all tools are registered
    assert len(tools) == 54
    print('All 54 tools registered successfully')

asyncio.run(test())
"
```

## Testing with Claude Desktop

1. Connect the server to Claude Desktop (see setup.md)
2. Test with natural language prompts:
   - "Calculate EMI for a 50 lakh home loan at 8.5% for 20 years"
   - "What's my financial health score?" (provide details)
   - "Plan my retirement — I'm 30, earn 1.5L/month"
   - "Compare two bonds: 8% coupon vs 10% coupon, both 5 year"

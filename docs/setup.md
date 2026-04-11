# Setup Guide

## Prerequisites

- **Python 3.10+** (3.12 recommended)
- **uv** (recommended) or pip
- **Claude Desktop** or any MCP-compatible client

## Installation

### Option 1: Using uv (Recommended)

```bash
# Clone the project
cd personal-finance-mcp

# Create virtual environment and install
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

uv pip install -e ".[dev]"
```

### Option 2: Using pip

```bash
cd personal-finance-mcp
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Connect to Claude Desktop

1. Open Claude Desktop settings → Developer → Edit Config
2. Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "personal-finance": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/ABSOLUTE/PATH/TO/personal-finance-mcp",
        "personal-finance-mcp"
      ]
    }
  }
}
```

Replace `/ABSOLUTE/PATH/TO/personal-finance-mcp` with the actual path on your machine.

3. Restart Claude Desktop
4. You should see the hammer icon with 54 tools available

## Connect to Claude Code

Claude Code auto-discovers MCP servers. Add to your project's `.claude/settings.json`:

```json
{
  "mcpServers": {
    "personal-finance": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/ABSOLUTE/PATH/TO/personal-finance-mcp",
        "personal-finance-mcp"
      ]
    }
  }
}
```

## Run as Standalone Server (SSE)

For remote MCP clients:

```bash
source .venv/bin/activate
python -c "from src.server import mcp; mcp.run(transport='sse')"
```

Server starts at `http://127.0.0.1:8000/sse`.

## Verify Installation

```bash
# Run tests
pytest tests/ -v

# Quick smoke test
python -c "from src.server import mcp; print(f'{len(mcp._tool_manager._tools)} tools loaded')"
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp[cli]` | >=1.0.0 | MCP Python SDK |
| `pydantic` | >=2.0.0 | Input validation |
| `pytest` | >=7.0 (dev) | Testing |

## Troubleshooting

### "No module named 'src'"
Ensure you installed with `-e` (editable) flag: `uv pip install -e ".[dev]"`

### Claude Desktop doesn't show tools
- Check the path in config is absolute and correct
- Restart Claude Desktop completely
- Check `~/Library/Logs/Claude/mcp*.log` on macOS for errors

### Import errors
```bash
# Verify the package is installed correctly
python -c "from src.calculators.tvm import future_value; print(future_value(100000, 12, 10, 12))"
```

# Setup Guide

## Prerequisites

- **Python 3.10+** (3.12 recommended)
- **uv** (recommended) or pip
- **Claude Desktop** or any MCP-compatible client

## Installation

## Global Installation

Because this tool is globally published to PyPI, you don't even need to download the code to use it if you are using modern tools.

### Option 1: Zero-Install (using uvx)
If you have `uv` installed, it can dynamically fetch and run the package:
```bash
uvx personal-finance-mcp
```

### Option 2: Global Pipeline (using pip)
To natively install the executable into your python ecosystem:
```bash
pip install personal-finance-mcp
```

## Connect to Claude Desktop

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

## Connect to Claude Code

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

## Run as Standalone Server (SSE)

For remote MCP clients:

```bash
# If installed normally:
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

### "ModuleNotFoundError: No module named 'src'"
If you're running locally from source, ensure you installed with the `-e` (editable) flag: `uv pip install -e ".[dev]"`

### Claude Desktop doesn't show tools
- Check the path in config is absolute and correct
- Restart Claude Desktop completely
- Check `~/Library/Logs/Claude/mcp*.log` on macOS for errors

### Import errors
```bash
# Verify the package is installed correctly
python -c "from src.calculators.tvm import future_value; print(future_value(100000, 12, 10, 12))"
```

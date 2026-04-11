# Quickstart: Publish to the Anthropic MCP Registry

The MCP Registry is currently in preview. This tutorial provides a meticulous, step-by-step guide to publishing the **Personal Finance MCP** to the official MCP Registry. Since the MCP Registry only hosts metadata and not code artifacts, we must first publish the Python package to PyPI.

## Prerequisites
- **Python/uv** setup on your local machine.
- **PyPI Account**: Essential as your artifacts will be served via PyPI.
- **GitHub Account**: Required for seamless namespace authentication on the MCP Registry.

---

## Step 1: Prepare the Package for PyPI

Before registering with Anthropic, your project must be publicly accessible as a Python package.

1. Ensure your `pyproject.toml` is completely filled out with your package name (e.g., `personal-finance-mcp`).
2. Build the distribution files:
   ```bash
   uv build
   ```
3. Publish to PyPI (you will need to authenticate):
   ```bash
   uv publish
   ```
> [!NOTE]
> Ensure the package is successfully visible at `https://pypi.org/project/personal-finance-mcp/` or your chosen package name before proceeding to the MCP Registry.

---

## Step 2: Install `mcp-publisher`

Anthropic requires the official `mcp-publisher` CLI tool to upload metadata to the Registry.

**macOS (Homebrew):**
```bash
brew install mcp-publisher
```

**Linux / macOS (Binary Download):**
```bash
curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/
```

Verify your installation:
```bash
mcp-publisher --help
```

---

## Step 3: Generate `server.json`

The MCP Registry requires a `server.json` configuration file at the root of your project to validate schema routing and execution transport.

Run the initialization tool:
```bash
mcp-publisher init
```

This generates a `server.json` file. Since we are using standard GitHub authentication without custom DNS domains, you **must format the server name with your GitHub prefix**.

Edit `server.json` carefully to resemble this configuration:
```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
  "name": "io.github.sarveshtalele/personal-finance",
  "description": "54 robust financial calculators based on deterministic mathematical principles.",
  "repository": {
    "url": "https://github.com/sarveshtalele/personal-finance-mcp",
    "source": "github"
  },
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "pypi",
      "identifier": "personal-finance-mcp",
      "version": "1.0.0",
      "transport": {
        "type": "stdio"
      }
    }
  ]
}
```

> [!IMPORTANT]
> - `registryType` must be set to `"pypi"` for Python packages.
> - `identifier` must be your exact PyPI package name.
> - **Security Note**: This MCP operates completely offline. You do not need to specify any `environmentVariables` blocks acting as API keys.

---

## Step 4: Authenticate with the MCP Registry

We will authenticate the CLI against your existing GitHub identity.

Initiate the flow:
```bash
mcp-publisher login github
```

Follow the terminal instructions carefully:
1. Go to: `https://github.com/login/device`
2. Enter the generated one-time code.
3. Authorize the application.

Your terminal should return:
```
✓ Successfully logged in
```

---

## Step 5: Publish Server Metadata

Finally, upload your validated `server.json` into the public Anthropic MCP network.

```bash
mcp-publisher publish
```

You should see:
```text
Publishing to https://registry.modelcontextprotocol.io...
✓ Successfully published
✓ Server io.github.sarveshtalele/personal-finance version 1.0.0
```

### Verification
You can verify your server exists within the global registry index by querying the API:
```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.sarveshtalele/personal-finance"
```

---

## Troubleshooting

| Error Message | Action |
| ------------- | ------ |
| `"Registry validation failed for package"` | Verify your PyPI package name (`identifier`) is public and matches your `server.json`. |
| `"Invalid or expired Registry JWT token"` | Run `mcp-publisher logout` then `mcp-publisher login github` to re-issue credentials. |
| `"You do not have permission to publish this server"` | Your `name` field does not perfectly map to your GitHub authenticated namespace. It must begin exactly with `io.github.sarveshtalele/`. |

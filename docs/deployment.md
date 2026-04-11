# Deployment Guide

## Deployment Options

### 1. Local (Claude Desktop / Claude Code)

**Simplest option** — run on your machine, connect via stdio.

```bash
```bash
# If using uv
uvx personal-finance-mcp

# If using pip
pip install personal-finance-mcp
```

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

### 2. SSE Server (Remote Access)

Run as an HTTP server for remote MCP clients.

```bash
# Start server
python -c "from src.server import mcp; mcp.run(transport='sse')"
# Server runs at http://127.0.0.1:8000/sse
```

For production, use behind a reverse proxy:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name finance-mcp.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3. Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["python", "-c", "from src.server import mcp; mcp.run(transport='sse')"]
```

```bash
docker build -t personal-finance-mcp .
docker run -p 8000:8000 personal-finance-mcp
```

### 4. Streamable HTTP (Production)

For production deployments with better connection handling:

```python
# run_production.py
from src.server import mcp

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000,
    )
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_HOST` | `127.0.0.1` | Server bind host |
| `MCP_PORT` | `8000` | Server port |
| `LOG_LEVEL` | `INFO` | Logging level |

## Health Check

```bash
# Verify server is running
curl http://localhost:8000/sse
```

## Security Considerations

- **No authentication by default** — add auth for production SSE deployments
- **No PII stored** — server is stateless, no data persisted
- **All calculations are deterministic** — no external API calls
- **Input validation** via Pydantic — prevents injection attacks

## Monitoring

The server logs all tool calls to stderr. Monitor with:

```bash
# View logs in real-time
python -c "from src.server import mcp; mcp.run(transport='sse')" 2>&1 | tee server.log
```

## Scaling

This server is CPU-bound (pure math calculations), not I/O bound:
- Single instance handles ~1000 calculations/second
- For high load, run multiple instances behind a load balancer
- No shared state — horizontally scalable

## Updating

If you installed globally via `pip`:
```bash
pip install --upgrade personal-finance-mcp
```
*(If you are using `uvx`, updates are pulled dynamically!).*

### 5. Hugging Face Spaces & Public Connectors

You can easily host this MCP server for free on **Hugging Face Spaces**. This allows anyone to connect to your financial calculators remotely without needing to download or install the code locally.

**Step 1: Deploying to Hugging Face**
1. Create a new **Space** on Hugging Face.
2. Select **Docker** as the Space SDK and choose the **Blank** template.
3. Upload the files from this repository directly to the Space.
4. Since Hugging Face expects web servers to listen on port `7860`, update the `Dockerfile` CMD to bind appropriately:
   ```dockerfile
   EXPOSE 7860
   CMD ["python", "-c", "from src.server import mcp; mcp.run(transport='sse', host='0.0.0.0', port=7860)"]
   ```

**Step 2: Connecting Claude Desktop to your Remote Server**
Because Claude Desktop exclusively communicates via stdio (command-line pipes) today, you need an SSE proxy to connect to a cloud URL. You can use standard public NPM proxies to bridge the connection. 

Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "finance-cloud": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/client-sse",
        "https://yourhfusername-spacename.hf.space/sse"
      ]
    }
  }
}
```
*Note: Any third-party MCP client that natively supports the HTTP/SSE transport protocol can simply point directly to the URL `https://yourhfusername-spacename.hf.space/sse` to consume the tools automatically!*

### 6. Official Connectors & Registries (Like Figma, GitHub)

You may notice that Claude Desktop has built-in UI toggles for "Official Connectors" like Figma, Google Drive, or GitHub. 

Currently, Anthropic natively builds and maintains those toggles directly inside the Claude application. Third-party developers cannot arbitrarily add a toggle switch to the Claude Desktop UI. However, you can achieve "official" status within the developer ecosystem using these three methods:

**Method A: Submit to the Official MCP GitHub Registry**
Anthropic maintains the official open-source directory of MCP servers. 
1. Push your repository to GitHub.
2. Submit a Pull Request to the [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) repository.
3. If approved, your financial server will be listed officially for the global community.

**Method B: Publish via Smithery (The MCP Package Manager)**
[Smithery.ai](https://smithery.ai/) is the most popular registry for MCP servers. 
1. Sign up on Smithery.ai and link your GitHub repository.
2. Add a `smithery.yaml` file to your root directory.
3. Once published, anyone in the world can install your connector natively into their Claude Desktop config via a single command:
   ```bash
   npx @smithery/cli install personal-finance-mcp --client claude
   ```

**Method C: Custom Built-ins (Enterprise)**
If you are representing a large organization processing proprietary financial datasets and want a dedicated toggle switch inside Claude Desktop natively (like Figma), you must reach out to the Anthropic Partnerships team directly for an enterprise API integration.

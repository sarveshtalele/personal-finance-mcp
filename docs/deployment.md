# Deployment

The repository ships a **unified server** that serves the website, the JSON API,
and the MCP connector on a single port — packaged as one Docker image.

```
/        -> Next.js website (built into web/out)
/mcp     -> MCP server over streamable-HTTP  (the connector URL)
/api/*   -> JSON endpoints (tool catalog, calculators, live market data)
```

## Run locally

```bash
# 1. Build the website (once, or whenever the UI changes)
cd web && npm install && npm run build && cd ..

# 2. Install + run the unified server
pip install -e .
python -m src.web            # http://localhost:7860
```

Open `http://localhost:7860`, and add `http://localhost:7860/mcp` as an HTTP MCP
server in Claude Code:

```bash
claude mcp add --transport http personal-finance http://localhost:7860/mcp
```

> Prefer pure stdio (offline, no web)? `python -m src` still runs the classic
> stdio MCP server with all 76 tools.

## Run with Docker

```bash
docker build -t personal-finance-mcp .
docker run -p 7860:7860 personal-finance-mcp
```

The multi-stage `Dockerfile` builds the Next.js site in a Node stage, then copies
the static export into the Python runtime stage.

## Deploy to Hugging Face Spaces (Docker)

The root `README.md` already contains the required Space frontmatter
(`sdk: docker`, `app_port: 7860`).

1. **Create a write token** at <https://huggingface.co/settings/tokens> (role: *Write*).
2. **Create a Space** (SDK = *Docker*, blank) at
   `https://huggingface.co/new-space`, e.g. `your-username/personal-finance-mcp`.
3. **Push this repo to the Space** (the Space is just a git remote):

   ```bash
   pip install -U "huggingface_hub[cli]"
   huggingface-cli login                       # paste the write token

   git remote add space https://huggingface.co/spaces/<user>/personal-finance-mcp
   git push space main
   ```

   Or create + push in one step (token inline):

   ```bash
   huggingface-cli repo create personal-finance-mcp --type space --space_sdk docker
   git push https://<user>:<HF_TOKEN>@huggingface.co/spaces/<user>/personal-finance-mcp main
   ```

4. Hugging Face builds the image and starts the container. Once it shows
   **Running**, your URLs are:

   | URL | Use |
   |-----|-----|
   | `https://<user>-personal-finance-mcp.hf.space/` | Website |
   | `https://<user>-personal-finance-mcp.hf.space/mcp` | **Connector URL** |

5. **Use the connector** anywhere:
   - Claude Desktop → Settings → Connectors → Add custom connector → paste the `/mcp` URL.
   - Claude Code → `claude mcp add --transport http personal-finance <url>/mcp`.
   - Cursor / VS Code → add `{ "url": "<url>/mcp", "transport": "http" }` to `mcp.json`.

### Notes

- The server runs **stateless** (`stateless_http=True`) and disables DNS-rebinding
  host checks so it works behind the Hugging Face proxy. See `src/server.py`.
- Live-data tools call public, keyless APIs (AMFI / Frankfurter / stooq); no
  secrets are required. Outbound network is allowed on Spaces by default.
- Nothing is persisted — every calculation is independent and reproducible.

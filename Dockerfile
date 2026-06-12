# syntax=docker/dockerfile:1
# Multi-stage build: compile the Next.js site, then run the unified Python server
# (MCP over streamable-HTTP at /mcp + JSON API at /api + the static website at /).

# ---------- Stage 1: build the website ----------
FROM node:26-slim AS web
WORKDIR /web
COPY web/package.json web/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY web/ ./
RUN npm run build          # produces /web/out (output: "export")

# ---------- Stage 2: python runtime ----------
FROM python:3.12-slim
LABEL maintainer="sarveshkishortalele"
LABEL description="Personal Finance MCP — 76 tools, website + connector"

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir -e ".[web]"

# Bring in the exported website so the server can serve it at "/"
COPY --from=web /web/out web/out

ENV PORT=7860
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"7860\")}/api/health')" || exit 1

CMD ["python", "-m", "src.web"]

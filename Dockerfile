FROM python:3.12-slim

LABEL maintainer="sarveshkishortalele"
LABEL description="Complete Financial Planning MVP MCP Server"

WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ src/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose SSE port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "from src.server import mcp; print('OK')" || exit 1

# Run SSE server for remote clients
CMD ["python", "-c", "from src.server import mcp; mcp.run(transport='sse', host='0.0.0.0', port=8000)"]

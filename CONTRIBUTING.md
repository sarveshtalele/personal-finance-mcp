# Contributing

Thanks for your interest in improving Personal Finance MCP! Contributions of all sizes are welcome.

## Getting started

```bash
git clone https://github.com/sarveshtalele/personal-finance-mcp.git
cd personal-finance-mcp
pip install -e ".[dev]"
pytest -q
```

To work on the website:

```bash
cd web && npm install && npm run dev      # http://localhost:3000 (UI only)
# or build + serve the full stack:
npm run build && cd .. && python -m src.web
```

## Adding a calculator (tool)

Tools live in `src/tools/`. Each module keeps **pure functions** separate from the thin MCP
wrappers, so the same function powers the MCP server, the web API, and the tests.

1. Write a pure function that takes numbers and returns a `dict` (include a `"formula"` key).
2. Register it inside the module's `register(mcp)` with an `@mcp.tool` wrapper. Write a clear,
   intent-rich docstring — the description is how the model decides when to call your tool
   (e.g. "Use when a user asks how long to double their money").
3. If it's a new module, import and `register()` it in `src/server.py`.
4. Add a test in `tests/`.
5. (Optional) Expose it in the web calculator via `CALCULATORS` in `src/web/server.py`.

## Guidelines

- **Deterministic only** — no randomness or model inference for the numbers.
- Match the surrounding style; run `ruff check .` and `pytest -q` before opening a PR.
- Keep formulas traceable to a recognised source (the NISM IA Level 1 curriculum is the baseline).
- Cite the formula in the result `dict` and/or a comment.

## Pull requests

- Branch from `main`, keep PRs focused, and describe the change and its rationale.
- Ensure CI is green (lint + tests). New tools should include tests.

By contributing you agree your work is licensed under the project's [MIT License](LICENSE).

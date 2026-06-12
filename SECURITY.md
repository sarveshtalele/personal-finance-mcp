# Security Policy

## Reporting a vulnerability

Please report security issues **privately** — do not open a public issue.

- Use GitHub's [private vulnerability reporting](https://github.com/sarveshtalele/personal-finance-mcp/security/advisories/new), or
- Email the maintainer via the address on the GitHub profile.

Include steps to reproduce and the impact. We aim to acknowledge within a few days.

## Scope & design notes

- The server is **stateless** and stores no user data.
- The JSON API is rate-limited, bounds all numeric inputs (to prevent DoS via loop-driving
  parameters), caps request bodies, and sends security headers (CSP, `X-Content-Type-Options`,
  `Referrer-Policy`, `Permissions-Policy`).
- Live-market-data tools call only fixed, public, keyless endpoints (AMFI, Frankfurter, Yahoo);
  inputs are validated. No secrets are stored in the application.
- The only secret in the deployment pipeline is the Hugging Face token, held as the GitHub
  Actions secret `HF_TOKEN`.

## Disclaimer

This project is for educational use and is **not investment advice**.

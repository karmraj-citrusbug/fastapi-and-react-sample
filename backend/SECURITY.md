## Security Policy

This repository is designed to demonstrate best practices without exposing sensitive data.

### Reporting a Vulnerability
If you discover a security issue, please open a private report or contact the maintainer directly. Do not open a public issue with exploit details.

### Best Practices Implemented
- Secrets are loaded from environment variables with `.env.<environment>` files
- No hard-coded credentials
- Centralized error handling and logging without leaking sensitive data
- Pinned dependencies in `requirements.txt`
- Pre-commit hooks for linting and static analysis

### Hardening Recommendations
- Rotate tokens regularly and use least-privilege API keys
- Run with `DEBUG=false` in non-local environments
- Use HTTPS everywhere and secure cookies for frontends



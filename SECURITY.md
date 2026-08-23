# 🔒 Security Policy

## Supported Versions
SmartCart AI-RAG actively maintains and patches security issues on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## Reporting a Vulnerability
We take security and secret protection seriously. If you discover a vulnerability or security issue:

1. Please **do NOT** create a public GitHub issue.
2. Email the maintainer directly at: `tatapudiprasad6300284084@gmail.com` with:
   - Description of the issue.
   - Steps to reproduce.
   - Potential impact.
3. We will acknowledge receipt within 48 hours and work on a fix promptly.

---

## Secrets & API Key Guidelines
- **Never commit `.env` files** containing real `OPENROUTER_API_KEY`, database credentials, or secret tokens.
- All secret variables must be supplied via local environment variables or deployment secret vaults.
- `.gitignore` is pre-configured to strictly ignore all `.env` files across the project.

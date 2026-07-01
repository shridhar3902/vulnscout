# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 2.x     | ✅ Active  |
| 1.x     | ⚠️ Critical fixes only |
| < 1.0   | ❌ Unsupported |

---

## Reporting a Vulnerability

**Please do NOT open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in VulnScout itself (not in a scan target), please report it privately:

1. **Email**: `security@shridhar.dev`  
   *(Replace with your actual contact — if no security email, use GitHub's private security advisory feature below)*
2. **GitHub Private Advisory**: [Report a vulnerability](../../security/advisories/new)

### What to include

- VulnScout version (`python3 vulnscout.py --version`)
- A description of the vulnerability and its potential impact
- Steps to reproduce
- Any proof-of-concept code (sanitized — no real targets)

### Response Timeline

| Step | Timeline |
|------|---------|
| Acknowledgement | Within 48 hours |
| Initial assessment | Within 5 business days |
| Fix / mitigation | Within 30 days for critical issues |
| Public disclosure | Coordinated with reporter |

We follow **coordinated disclosure** — we will credit you in the release notes unless you prefer to remain anonymous.

---

## Scope

This policy covers security issues **in the VulnScout codebase itself**, such as:

- Remote code execution via malicious scan target responses
- Insecure handling of user-supplied input
- Credential or secret leakage
- Dependency vulnerabilities (if directly exploitable)

This policy does **not** cover:

- Vulnerabilities in scan targets (that's what VulnScout is designed to find!)
- Issues already fixed in the latest release
- Theoretical attacks with no realistic exploitation path

---

## Authorized Use Reminder

VulnScout is an authorized-use-only tool. Misuse of VulnScout against unauthorized targets is **not** a security vulnerability in VulnScout — it is a legal and ethical violation by the operator. Read [DISCLAIMER.md](DISCLAIMER.md).

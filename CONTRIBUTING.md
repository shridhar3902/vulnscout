# Contributing to VulnScout

First off — thank you for taking the time to contribute! VulnScout is an open-source community project and every contribution counts.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Responsible Disclosure](#responsible-disclosure)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Writing a New Module](#writing-a-new-module)
- [Coding Standards](#coding-standards)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

---

## Responsible Disclosure

**Do not open a public GitHub issue for security vulnerabilities in VulnScout itself.** See [SECURITY.md](SECURITY.md) for the responsible disclosure process.

---

## How to Contribute

| Type | Where to start |
|------|----------------|
| Bug report | [Open an issue](../../issues/new?template=bug_report.yml) |
| Feature idea | [Open an issue](../../issues/new?template=feature_request.yml) or start a [Discussion](../../discussions) |
| Code fix / module | Fork → branch → PR (see below) |
| Documentation | Edit Markdown files, open a PR |
| Translations | Open a discussion first |

---

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/vulnscout.git
cd vulnscout

# 2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies + dev tools
pip install -r requirements.txt
pip install flake8

# 4. Run a test scan (safe public target)
python3 vulnscout.py -d example.com --headers --ssl --yes
```

---

## Project Structure

```
vulnscout/
├── vulnscout.py           # Entry point, CLI, orchestration
├── modules/
│   ├── animation.py       # Spinner, ProgressBar, TypeWriter, colour helpers
│   ├── banner.py          # Animated ASCII art banner
│   ├── scope_gate.py      # Mandatory authorization prompt
│   ├── report.py          # HTML + JSON report writer
│   ├── subdomains.py      # Passive subdomain enumeration
│   ├── headers_check.py   # Security header audit
│   ├── exposed_files.py   # Exposed file probe
│   ├── tech_fingerprint.py# Technology fingerprinting
│   ├── port_scan.py       # Port scanner
│   ├── reflected_params.py# Reflected parameter / XSS surface
│   ├── ssl_check.py       # TLS certificate inspection
│   ├── cors_check.py      # CORS misconfiguration probe
│   ├── waf_detect.py      # WAF/CDN fingerprinting
│   ├── whois_lookup.py    # WHOIS intelligence
│   ├── robots_parser.py   # robots.txt / sitemap parser
│   └── vuln_hints.py      # CVE surface matcher
├── reports/               # Generated scan reports (git-ignored)
├── requirements.txt
├── install.sh
├── README.md
├── CONTRIBUTING.md        ← you are here
├── CHANGELOG.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── DISCLAIMER.md
└── .github/
    ├── workflows/ci.yml
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── FUNDING.yml
```

---

## Writing a New Module

Every module is a Python file in `modules/` with a single `run(target: str) -> dict` function.

### Template

```python
"""
my_module.py — Short description.
"""
import requests
from modules.animation import Spinner


def run(target: str) -> dict:
    out = {
        "status":   "ok",
        "findings": [],
        # ... your data fields
    }

    spinner = Spinner(f"Running my check on {target}")
    spinner.start()

    try:
        # ... do your work
        spinner.stop("Done", success=True)
    except Exception as e:
        out["status"] = "error"
        out["error"]  = str(e)
        spinner.stop(f"Error: {e}", success=False)

    return out
```

### Rules

1. **Always use a `Spinner`** for any I/O-bound operation.
2. **Return findings** as `[{"severity": "critical|high|medium|low|info", "msg": "..."}]`.
3. **Never auto-exploit.** Surface findings only — let humans decide.
4. **Document data sources** — where does the information come from?
5. **Add your module** to `vulnscout.py` (import + `--flag` + `section_header` + `results["modules"][key]`).
6. **Add a renderer** in `modules/report.py` under `_RENDERERS` and `_RENDER_ORDER`.
7. **Update `README.md`** module table.
8. **Update `CHANGELOG.md`** under `[Unreleased]`.

---

## Coding Standards

- **PEP 8** — max line length 110 characters
- **Type hints** on all function signatures
- **Docstrings** on all modules and public functions
- **No bare `except:`** — catch specific exceptions
- **No `print()` in modules** — use `Spinner`, `ProgressBar`, or the animation helpers

---

## Commit Message Convention

```
<type>(<scope>): <short summary>

Types: feat | fix | docs | style | refactor | perf | test | chore
Scope: module name, cli, report, ci, docs, etc.

Examples:
feat(ssl): add OCSP stapling check
fix(cors): handle connection timeout gracefully
docs(readme): add Windows install instructions
```

---

## Pull Request Process

1. **Create a feature branch** from `main`:  
   `git checkout -b feat/my-module`
2. **Make your changes**, following the standards above.
3. **Test locally** against `example.com --yes`.
4. **Run linting**: `flake8 vulnscout.py modules/ --max-line-length=110`
5. **Open your PR** using the PR template.
6. A maintainer will review within 7 days.

**The scope-confirmation gate must stay intact.** Any PR that bypasses or weakens `scope_gate.py` will not be merged.

---

Thank you for making VulnScout better! ⭐

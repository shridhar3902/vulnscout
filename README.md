<div align="center">

```
 __   __     _       ____                 _   
 \ \ / /   _| |_ __ |  _ \  ___ _ __ ___| |_ 
  \ V / | | | | '_ \| | | |/ _ \ '__/ __| __|
   | || |_| | | | | | |_| |  __/ |  \__ \ |_ 
   |_| \__,_|_|_| |_|____/ \___|_|  |___/\__|
```

# VulnScout

**Authorized Web Recon & Vulnerability Surface Mapper**

*Terminal-first · Zero noise · Bug-bounty ready · 12 modules · Animated reports*

---

[![Version](https://img.shields.io/github/v/release/shridhar3902/vulnscout?color=00d2ff&label=version&style=flat-square)](https://github.com/shridhar3902/vulnscout/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-00d2ff?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/shridhar3902/vulnscout?color=7b2fff&style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/shridhar3902/vulnscout?color=ffcc00&style=flat-square)](https://github.com/shridhar3902/vulnscout/stargazers)
[![Issues](https://img.shields.io/github/issues/shridhar3902/vulnscout?color=ff6b35&style=flat-square)](https://github.com/shridhar3902/vulnscout/issues)
[![CI](https://img.shields.io/github/actions/workflow/status/shridhar3902/vulnscout/ci.yml?label=CI&style=flat-square&logo=github-actions&logoColor=white)](https://github.com/shridhar3902/vulnscout/actions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)
[![Maintained](https://img.shields.io/badge/maintained-yes-22c55e?style=flat-square)](https://github.com/shridhar3902/vulnscout/graphs/commit-activity)

[Features](#-features) · [Installation](#-installation) · [Quick Start](#-quick-start) · [All Flags](#-command-line-reference) · [Modules](#-modules-in-depth) · [Report](#-html-report) · [Bug Bounty](#-bug-bounty-workflow) · [FAQ](#-faq) · [Contributing](#-contributing) · [Legal](#-legal--ethics)

</div>

---

> **⚠️ Authorized Use Only** — VulnScout requires you to type `I CONFIRM` before scanning any target. It is designed for assets you own, in-scope bug bounty programs, and lab environments. Using it against unauthorized targets is illegal. Read [DISCLAIMER.md](DISCLAIMER.md).

---

## 🌟 What is VulnScout?

VulnScout is a **modular, terminal-animated web reconnaissance and vulnerability surface mapping tool** built for security professionals, bug bounty hunters, and CTF players. It maps the attack surface of a target you're authorized to test — then generates a stunning, fully animated HTML report you can share with your team or attach to a bug report.

It is **not** a point-and-shoot exploitation framework. It finds surface — you do the thinking.

### Why VulnScout over other tools?

| Feature | VulnScout | Nmap alone | Nikto | Manual curl |
|---------|:---------:|:----------:|:-----:|:-----------:|
| Animated terminal UI | ✅ | ❌ | ❌ | ❌ |
| Cinematic HTML report | ✅ | ❌ | Basic | ❌ |
| CORS misconfiguration probe | ✅ | ❌ | Partial | Manual |
| WAF/CDN fingerprinting | ✅ | ❌ | Partial | Manual |
| CVE hints for detected stack | ✅ | ❌ | Partial | ❌ |
| TLS cert deep inspection | ✅ | Basic | Basic | Manual |
| WHOIS intelligence | ✅ | ❌ | ❌ | Manual |
| Scope gate (ethical guard) | ✅ | ❌ | ❌ | ❌ |
| Zero paid API keys needed | ✅ | ✅ | ✅ | ✅ |
| Cross-platform | ✅ | ✅ | Linux | ✅ |

---

## ✨ Features

### Terminal Experience
- **Glitch-reveal animated banner** — Matrix-style scramble effect on startup
- **Live spinners** per module with braille-frame animation and color cycling
- **Color-coded severity output** — 🔴 Critical · 🟠 High · 🟡 Medium · 🔵 Low · ⚪ Info
- **Section dividers** between each module run
- **Final summary table** — all modules, status, finding count, top severity in one view
- **Risk score display** (0–100) with gradient bar at scan end
- **Windows-safe** — gracefully falls back to ASCII on CP1252 terminals (no `UnicodeEncodeError`)

### Scanning Power — 12 Modules
| Module | Flag | Category |
|--------|------|----------|
| WHOIS Intelligence | `--whois` | Passive Intel |
| Passive Subdomain Enumeration | `--subdomains` | Passive Intel |
| robots.txt & Sitemap Surface | `--robots` | Passive Intel |
| Technology Fingerprinting | `--tech` | Fingerprinting |
| WAF / CDN Detection | `--waf` | Fingerprinting |
| TLS/SSL Certificate Inspection | `--ssl` | Security Audit |
| HTTP Security Headers Audit | `--headers` | Security Audit |
| CORS Misconfiguration Probe | `--cors` | Security Audit |
| Exposed Sensitive Files | `--exposed` | Security Audit |
| Port Scan (27 ports) | `--ports` | Network |
| Reflected Parameter Discovery | `--reflect` | XSS Surface |
| CVE / Vulnerability Hints | `--vulns` | Intelligence |

### HTML Report
- Canvas particle-network animated background
- SVG animated risk gauge (0–100) with needle & count-up
- Severity badge counters that animate up on page load
- Glassmorphism accordion cards (auto-expand on findings)
- Port heatmap chips colour-coded by risk level
- CVE advisory links inline per finding
- Print mode (animations freeze, white background)

---

## 📦 Installation

### Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| pip | Any recent version |
| OS | Kali Linux, Ubuntu, Debian, macOS, Windows 10+ |

### Option 1 — Kali Linux / Debian / Ubuntu (Recommended)

```bash
git clone https://github.com/shridhar3902/vulnscout.git
cd vulnscout
chmod +x install.sh
./install.sh
```

The installer checks your Python version, installs all dependencies, and creates the `reports/` directory automatically.

### Option 2 — Manual (any OS with Python 3.10+)

```bash
# Clone the repository
git clone https://github.com/shridhar3902/vulnscout.git
cd vulnscout

# Install dependencies
pip3 install -r requirements.txt

# Verify installation
python3 vulnscout.py --version
```

### Option 3 — Windows (PowerShell)

```powershell
# Clone
git clone https://github.com/shridhar3902/vulnscout.git
cd vulnscout

# Install dependencies
pip install -r requirements.txt

# Run
python vulnscout.py --help
```

> **Windows Tip:** Run in Windows Terminal for best colour support. The tool automatically detects CP1252 terminals and falls back to ASCII-safe characters.

### Option 4 — Virtual Environment (clean install)

```bash
git clone https://github.com/shridhar3902/vulnscout.git
cd vulnscout

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python3 vulnscout.py --version
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | ≥ 2.31.0 | HTTP requests for all active modules |
| `python-whois` | ≥ 0.9.4 | WHOIS domain intelligence |
| `colorama` | ≥ 0.4.6 | Windows ANSI terminal colour support |

All dependencies are in [requirements.txt](requirements.txt). No API keys. No accounts. No paid tiers.

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/shridhar3902/vulnscout.git
cd vulnscout
pip3 install -r requirements.txt

# 2. Run a full scan
python3 vulnscout.py -d example.com --all

# 3. Type "I CONFIRM" at the scope prompt

# 4. Open the report
# Reports are saved to reports/vulnscout_example.com_<timestamp>.html
```

---

## 📖 Command-Line Reference

```
usage: vulnscout [-h] -d DOMAIN [-o OUTPUT] [--version] [--yes]
                 [--all] [--subdomains] [--headers] [--exposed]
                 [--tech] [--ports] [--reflect] [--ssl] [--cors]
                 [--waf] [--whois] [--robots] [--vulns]
```

### Core Arguments

| Flag | Description |
|------|-------------|
| `-d`, `--domain DOMAIN` | **Required.** Target domain (e.g. `example.com`). `http://` and `https://` prefixes are stripped automatically. |
| `-o`, `--output NAME` | Base name for output files (no extension). Default: `vulnscout_<domain>_<timestamp>` |
| `--version` | Show version number and exit |
| `--yes` | Skip the interactive `I CONFIRM` scope prompt. **Only use in CI/scripted runs where authorization has already been verified out-of-band.** |
| `-h`, `--help` | Show help message and exit |

### Module Flags

| Flag | Module | Description |
|------|--------|-------------|
| `--all` | All modules | Runs all 12 modules in sequence. Equivalent to passing every other flag. |
| `--whois` | WHOIS Intel | Queries WHOIS for registrar, creation/expiry dates, nameservers, status flags, and checks for transfer lock. |
| `--subdomains` | Subdomain Enum | Passive certificate-transparency log enumeration via crt.sh. No DNS brute-force — completely passive. |
| `--robots` | robots.txt | Fetches `robots.txt` and `sitemap.xml`, extracts all `Disallow` paths, and flags those matching sensitive patterns (admin, API, staging, backups, etc.). |
| `--tech` | Tech Stack | Fingerprints the server, framework, and JS libraries from HTTP headers and page source. Detects WordPress, Drupal, Joomla, Laravel, Django, React, Next.js, jQuery, Bootstrap, Nginx, Apache, Cloudflare. |
| `--waf` | WAF / CDN | Detects Cloudflare, Akamai, Fastly, Imperva Incapsula, F5 BIG-IP, Barracuda, Sucuri, ModSecurity, and generic WAFs via header signatures, cookie names, body error pages, and blocking behaviour. |
| `--ssl` | TLS/SSL | Inspects the TLS certificate: validity, days until expiry, issuer, Subject Alternative Names, protocol version (TLS 1.2 / 1.3 / weak), cipher suite, and self-signed detection. |
| `--headers` | Sec Headers | Audits 6 critical security headers: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`. |
| `--cors` | CORS Probe | Sends 4 distinct Origin probes: (1) arbitrary origin reflection, (2) wildcard ACAO, (3) null origin, (4) credentials + reflected origin. Reports exact ACAO/ACAC response headers as evidence. |
| `--exposed` | Exposed Files | Probes 15+ commonly-exposed paths: `.git/HEAD`, `.env`, `.env.local`, `wp-config.php.bak`, `backup.zip`, `backup.sql`, `.DS_Store`, `id_rsa`, `.aws/credentials`, `phpinfo.php`, `docker-compose.yml`, and more. |
| `--ports` | Port Scan | Concurrent TCP connect scan across 27 common service ports. Includes FTP, SSH, Telnet, SMTP, DNS, HTTP/S, SMB, RDP, MySQL, PostgreSQL, Redis, Elasticsearch, MongoDB, and more. |
| `--reflect` | XSS Surface | Tests 12 common GET parameter names (`q`, `search`, `id`, `page`, `ref`, `redirect`, `url`, `name`, `query`, `keyword`, `lang`, `category`) for unescaped value reflection using a benign canary string. No payloads injected. |
| `--vulns` | CVE Hints | Cross-references the technology stack detected by `--tech` against a curated CVE table. Covers critical CVEs for WordPress, Drupal, Joomla, Laravel, Django, Next.js, jQuery, Nginx, Apache, Cloudflare. |

---

## 🗂️ Modules In Depth

### `--whois` — WHOIS Domain Intelligence

Queries public WHOIS records for the target domain (strips `www.` automatically).

**What it reports:**
- Registrar name and WHOIS server
- Domain creation, expiry, and last-updated dates
- Days until expiry (with warnings at < 30 and < 90 days)
- Nameservers list
- Registrant organisation (if not privacy-redacted)
- Domain status flags (e.g. `clientTransferProhibited`, `clientUpdateProhibited`)

**Findings flagged:**
- 🔴 Domain registration EXPIRED
- 🟠 Expiry within 30 days
- 🟡 Expiry within 90 days
- 🔵 Transfer lock not set (domain hijack risk)

---

### `--subdomains` — Passive Subdomain Enumeration

Queries [crt.sh](https://crt.sh) certificate transparency logs to discover subdomains without sending a single packet to the target.

**What it reports:**
- Complete list of unique subdomains (sorted)
- Total count

**Data source:** crt.sh (Comodo CT log aggregator)  
**Mode:** Completely passive — zero connection to the target

---

### `--robots` — robots.txt & Sitemap Surface Mapper

**What it fetches:**
- `https://target/robots.txt` — parses User-Agent blocks, `Disallow`, `Allow`, and `Sitemap` directives
- `https://target/sitemap.xml` (and any sitemaps listed in robots.txt)

**Sensitive path patterns flagged:**
`admin`, `login`, `dashboard`, `api/`, `internal`, `staging`, `dev`, `test`, `backup`, `config`, `.git`, `.env`, `secret`, `private`, `hidden`, `wp-admin`, `phpmyadmin`, `cpanel`, `plesk`

---

### `--tech` — Technology Fingerprinting

Inspects HTTP response headers and page body for technology signatures.

**Headers inspected:** `Server`, `X-Powered-By`

**Signatures detected:**
| Technology | Detection Method |
|-----------|-----------------|
| WordPress | `wp-content`, `wp-includes` in body |
| Drupal | `sites/all/themes`, `Drupal.settings` |
| Joomla | `/media/jui/`, `Joomla!` |
| Laravel | `laravel_session` cookie |
| Django | `csrfmiddlewaretoken` in body |
| React | `__REACT_DEVTOOLS`, `data-reactroot` |
| Next.js | `__NEXT_DATA__` in body |
| jQuery | `jquery.min.js` in body |
| Bootstrap | `bootstrap.min.css` in body |
| Nginx | `nginx` in `Server` header |
| Apache | `Apache` in `Server` header |
| Cloudflare | `cloudflare` anywhere |

---

### `--waf` — WAF / CDN Fingerprinting

Uses three detection layers:

1. **Header signatures** — `Server`, `Via`, `X-Powered-By`, `CF-RAY`, `X-Sucuri-ID`, `X-CDN`, `X-Cache`, `X-Served-By`
2. **Cookie name signatures** — `__cfduid`, `incap_ses`, `visid_incap`, `BIGipServer`, `barra_counter_session`
3. **Body error-page signatures** — triggered by sending a benign SQLi probe (`?id=1'+OR+'1'%3D'1`) and inspecting the response

**Detects:** Cloudflare · Akamai · Amazon CloudFront · Fastly · Varnish · Imperva Incapsula · F5 BIG-IP · Barracuda · Sucuri · ModSecurity · AWS ELB

---

### `--ssl` — TLS/SSL Certificate Inspection

Uses Python's stdlib `ssl` module — no third-party libraries required.

**What it inspects:**
| Field | Details |
|-------|---------|
| Validity | Valid / Expired |
| Days until expiry | Countdown with severity thresholds |
| Expiry date | Human-readable |
| Issuer (CA) | Common name of the signing CA |
| Subject | `commonName` of the certificate |
| Self-signed | True if issuer == subject |
| Subject Alternative Names | Full list of covered domains |
| TLS Protocol Version | TLS 1.2 / 1.3 (flags TLS 1.0, 1.1, SSLv3 as high risk) |
| Cipher Suite | Name and key size |

**Findings flagged:**
- 🔴 Certificate EXPIRED
- 🟠 Expiry < 14 days · Self-signed · Weak protocol (TLS < 1.2)
- 🟡 Expiry < 30 days

---

### `--headers` — HTTP Security Headers Audit

Checks for the presence of 6 critical security response headers.

| Header | Risk if Missing |
|--------|----------------|
| `Strict-Transport-Security` | Protocol downgrade & cookie hijacking |
| `Content-Security-Policy` | XSS and data injection attacks |
| `X-Frame-Options` | Clickjacking |
| `X-Content-Type-Options` | MIME-sniffing attacks |
| `Referrer-Policy` | Referrer information leakage |
| `Permissions-Policy` | Unauthorized access to browser APIs |

---

### `--cors` — CORS Misconfiguration Probe

Sends 4 distinct probes and inspects `Access-Control-Allow-Origin` (ACAO) and `Access-Control-Allow-Credentials` (ACAC) headers.

| Probe | Origin Sent | Dangerous If |
|-------|------------|--------------|
| Reflected origin | `https://evil-<target>.attacker.com` | ACAO reflects it exactly |
| Wildcard | `https://attacker.com` | ACAO returns `*` |
| Null origin | `null` | ACAO returns `null` |
| Credentials + origin | `https://attacker.com` + `Cookie: test=1` | ACAO reflects + ACAC = `true` |

**Finding severities:**
- 🔴 Critical — Origin reflection or credentials + reflection
- 🟠 High — Null origin accepted
- 🟡 Medium — Wildcard ACAO (no credential risk, but data exposure)

---

### `--exposed` — Exposed Sensitive Files

Sends individual GET requests for each path and flags any that return HTTP 200 with a non-empty body.

**Paths checked (15+):**

| Path | Sensitivity |
|------|------------|
| `.git/HEAD` | Source code leak → full repo extraction |
| `.env` / `.env.local` | Credentials, API keys, DB passwords |
| `wp-config.php.bak` | WordPress database credentials |
| `backup.zip` / `backup.sql` | Full application/database backup |
| `.DS_Store` | Directory listing reconstruction |
| `id_rsa` | Private SSH key |
| `.aws/credentials` | AWS access key + secret |
| `phpinfo.php` | Server configuration disclosure |
| `.svn/entries` | Source control metadata |
| `docker-compose.yml` | Infrastructure topology disclosure |
| `server-status` | Apache mod_status info |
| `.htaccess` | Server configuration |
| `config.php.bak` | Generic config backup |

---

### `--ports` — Port Scan

Concurrent TCP connect scan using Python's stdlib `socket` and `concurrent.futures.ThreadPoolExecutor` (30 workers).

**Ports scanned (27):**

| Port | Service | Risk Level |
|------|---------|-----------|
| 21 | FTP | 🔴 High |
| 22 | SSH | 🟡 Medium |
| 23 | Telnet | 🔴 Critical |
| 25 | SMTP | 🟡 Medium |
| 53 | DNS | 🟡 Medium |
| 80 | HTTP | 🟢 Info |
| 110 | POP3 | 🟡 Medium |
| 135 | MSRPC | 🟠 High |
| 139 | NetBIOS | 🟠 High |
| 143 | IMAP | 🟡 Medium |
| 443 | HTTPS | 🟢 Info |
| 445 | SMB | 🔴 Critical |
| 993 | IMAPS | 🟢 Info |
| 995 | POP3S | 🟢 Info |
| 1433 | MSSQL | 🟠 High |
| 1521 | Oracle | 🟠 High |
| 3306 | MySQL | 🟡 Medium |
| 3389 | RDP | 🔴 Critical |
| 5432 | PostgreSQL | 🟡 Medium |
| 5900 | VNC | 🔴 Critical |
| 6379 | Redis | 🔴 Critical |
| 8000 | HTTP-Alt | 🟡 Medium |
| 8080 | HTTP-Proxy | 🟡 Medium |
| 8443 | HTTPS-Alt | 🟡 Medium |
| 9200 | Elasticsearch | 🔴 Critical |
| 27017 | MongoDB | 🔴 Critical |

---

### `--reflect` — Reflected Parameter Discovery (XSS Surface)

Appends a benign canary string (`vsCanary12345`) to each parameter and checks if it appears **unescaped** in the HTTP response body.

**Parameters tested:**
`q` · `search` · `id` · `page` · `ref` · `redirect` · `url` · `name` · `query` · `keyword` · `lang` · `category`

> ⚠️ Unescaped reflection is a **precondition** for XSS, not proof of XSS. Always manually verify with Burp Suite before reporting.

---

### `--vulns` — CVE / Vulnerability Hints

Cross-references the technology stack from `--tech` against a curated local CVE table. **Does not perform active exploitation.**

**Coverage (sample):**

| Technology | Notable CVEs |
|-----------|-------------|
| Next.js | CVE-2025-29927 (auth bypass), CVE-2024-46982 (cache poisoning) |
| WordPress | CVE-2022-21661 (SQLi), CVE-2021-29447 (XXE) |
| Apache | CVE-2021-41773/42013 (path traversal RCE), CVE-2022-22720 (request smuggling) |
| Laravel | CVE-2021-3129 (RCE via debug mode), CVE-2018-15133 (unserialize RCE) |
| Django | CVE-2022-28347 (SQLi), CVE-2023-36053 (ReDoS) |
| Nginx | CVE-2021-23017 (buffer overwrite), CVE-2019-9511 (HTTP/2 DoS) |
| jQuery | CVE-2020-11022 (XSS), CVE-2019-11358 (prototype pollution) |
| Drupal | CVE-2018-7600/7602 (Drupalgeddon 2 & 3, RCE) |

---

## 📊 HTML Report

Every scan generates two output files:
- `reports/<name>.json` — machine-readable structured data
- `reports/<name>.html` — animated visual report

### Report Features

**Animated Background**  
A canvas-based particle network (pure vanilla JS, no external libraries) draws animated nodes and connections on a dark background.

**Risk Gauge**  
An SVG arc gauge animates from 0 to the computed risk score (0–100) on page load. A needle sweeps to the score position. The score is calculated by weighting all findings: Critical (+25), High (+15), Medium (+8), Low (+3), capped at 100.

**Severity Counter Cards**  
Five cards (Critical / High / Medium / Low / Info) count up with a JavaScript animation on page load.

**Module Accordion Cards**  
Each module gets a glassmorphism card. Cards with findings auto-expand. Each card shows finding severity badges, a chevron toggle, and detailed data (tables, port heatmap chips, SAN pills, progress bars).

**Port Heatmap**  
Open ports are displayed as coloured chips:
- 🔴 Red — Telnet, SMB, RDP, VNC, Redis, Elasticsearch, MongoDB (critical services)
- 🟠 Orange — SSH, MySQL, HTTP-Proxy (moderate risk)
- 🟢 Green — HTTP, HTTPS, IMAPS, POP3S (standard services)

**Print Mode**  
`Ctrl+P` or browser print freezes all animations and renders a clean white-background version.

### Sample JSON Output Structure

```json
{
  "target": "example.com",
  "version": "2.0.0",
  "timestamp": "2025-07-01T08:00:00Z",
  "risk_score": 42,
  "modules": {
    "whois": { "status": "ok", "registrar": "...", "expires": "2026-01-01", "findings": [] },
    "subdomains": { "status": "ok", "count": 14, "subdomains": ["api.example.com", "..."] },
    "ssl": { "status": "ok", "valid": true, "days_left": 180, "tls_version": "TLSv1.3", "findings": [] },
    "headers": { "status": "ok", "missing": [{"header": "Content-Security-Policy", "risk": "..."}], "present": {} },
    "cors": { "status": "ok", "findings": [] },
    "waf": { "status": "ok", "detected_wafs": ["Cloudflare"], "findings": [] },
    "ports": { "status": "ok", "resolved_ip": "93.184.216.34", "open_ports": [{"port": 80, "service": "HTTP"}] },
    "vuln_hints": { "status": "ok", "hints": [], "findings": [] }
  }
}
```

---

## 🐛 Bug Bounty Workflow

VulnScout is purpose-built for bug bounty reconnaissance. Here is a recommended workflow:

### Step 1 — Scope Verification
Before running anything, confirm the target is **explicitly in-scope** in the program's scope table (HackerOne, Bugcrowd, Intigriti, etc.).

### Step 2 — Full Recon Scan
```bash
python3 vulnscout.py -d target.com --all -o recon_target_$(date +%Y%m%d)
```

### Step 3 — Confirm Scope
Type `I CONFIRM` at the prompt. This is not optional — it's a deliberate friction point.

### Step 4 — Review the HTML Report
Open `reports/recon_target_<date>.html` in your browser. Review findings by severity. Start with 🔴 Critical.

### Step 5 — Triage by Category

| Finding Type | Next Step |
|-------------|-----------|
| Missing security headers | Verify in browser DevTools → report directly |
| Exposed `.env` / `.git` | Download and examine content manually before reporting |
| CORS misconfiguration | Manually craft PoC in browser / Burp Suite |
| Reflected parameters | Use Burp Suite to verify actual XSS exploitability |
| CVE hints | Check running version against NVD, craft targeted PoC |
| Open dangerous ports | Attempt service enumeration if in scope |
| SSL expiry / weak TLS | Screenshot + report — usually low-hanging P3/P4 |

### Step 6 — Manual Verification
**Never submit a VulnScout finding directly.** Every finding must be manually verified before submission. VulnScout identifies potential surface — humans confirm exploitability.

### Step 7 — Targeted Scans
```bash
# Deep-dive on specific areas after initial triage
python3 vulnscout.py -d api.target.com --headers --cors --ssl
python3 vulnscout.py -d target.com --tech --vulns
```

---

## 🎯 Example Commands

```bash
# Full scan — all 12 modules + auto-report name
python3 vulnscout.py -d example.com --all

# Full scan — custom report name
python3 vulnscout.py -d example.com --all -o pentest_example_2025

# Passive intelligence only (no active connections to target)
python3 vulnscout.py -d example.com --whois --subdomains

# Security header + TLS audit (quick wins)
python3 vulnscout.py -d example.com --headers --ssl

# Full security audit (no passive intel)
python3 vulnscout.py -d example.com --headers --ssl --cors --exposed --reflect

# Technology + CVE surface (what am I facing?)
python3 vulnscout.py -d example.com --tech --waf --vulns

# Network exposure check
python3 vulnscout.py -d example.com --ports

# CI / pipeline use (authorization pre-confirmed, no prompt)
python3 vulnscout.py -d example.com --all --yes -o ci_scan_$(date +%Y%m%d)

# Scan with explicit report path
python3 vulnscout.py -d example.com --all -o reports/my_report
```

---

## 📁 Project Structure

```
vulnscout/
│
├── vulnscout.py                  # Entry point: CLI parsing, orchestration, risk scoring
│
├── modules/
│   ├── __init__.py               # Package init
│   ├── animation.py              # Spinner, ProgressBar, TypeWriter, GlitchText, colour helpers
│   ├── banner.py                 # Animated ASCII art startup banner
│   ├── scope_gate.py             # Mandatory I CONFIRM authorization prompt
│   ├── report.py                 # HTML + JSON report writer
│   │
│   ├── subdomains.py             # Passive subdomain enumeration (crt.sh)
│   ├── headers_check.py          # HTTP security header audit
│   ├── exposed_files.py          # Exposed sensitive file probe
│   ├── tech_fingerprint.py       # Technology stack fingerprinting
│   ├── port_scan.py              # Concurrent TCP port scanner
│   ├── reflected_params.py       # Reflected parameter / XSS surface discovery
│   │
│   ├── ssl_check.py              # TLS/SSL certificate inspection
│   ├── cors_check.py             # CORS misconfiguration probe
│   ├── waf_detect.py             # WAF / CDN fingerprinting
│   ├── whois_lookup.py           # WHOIS domain intelligence
│   ├── robots_parser.py          # robots.txt & sitemap surface mapper
│   └── vuln_hints.py             # CVE surface hints for detected tech
│
├── reports/                      # Generated scan reports (git-ignored)
│   ├── *.html                    # Animated HTML reports
│   └── *.json                    # Structured JSON data
│
├── .github/
│   ├── workflows/ci.yml          # GitHub Actions CI (Python 3.10/3.11/3.12)
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml        # Structured bug report template
│   │   └── feature_request.yml   # Feature request template
│   ├── PULL_REQUEST_TEMPLATE.md  # PR checklist
│   └── FUNDING.yml               # GitHub Sponsors / Ko-fi
│
├── requirements.txt              # Python dependencies
├── install.sh                    # Kali/Debian/Ubuntu installer script
├── README.md                     # This file
├── CONTRIBUTING.md               # Contribution guide
├── CHANGELOG.md                  # Version history (Keep a Changelog format)
├── SECURITY.md                   # Responsible disclosure policy
├── CODE_OF_CONDUCT.md            # Contributor Covenant v2.1
├── DISCLAIMER.md                 # Authorized-use terms
└── LICENSE                       # MIT License
```

---

## 🔄 Roadmap

### v2.1 (Next)
- [ ] Async HTTP (`httpx`/`aiohttp`) for dramatically faster multi-target scans
- [ ] `--wordlist` flag for active subdomain brute-force (opt-in, separate from passive)
- [ ] `--output-format markdown` for direct paste into HackerOne reports

### v2.2
- [ ] Nuclei template integration (`--nuclei` flag)
- [ ] Burp Suite `.bambdas` export format
- [ ] Slack / Discord webhook notification on scan completion

### v3.0 (Future)
- [ ] Interactive TUI (built with `textual`)
- [ ] Multi-target batch scanning from file
- [ ] GitHub Actions template for automated scheduled scans
- [ ] Plugin system for community-contributed modules

---

## 🤝 Contributing

Contributions are what make open source amazing. Every contribution counts — from fixing a typo to writing a full new module.

### Quick Contribution Guide

```bash
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/vulnscout.git
cd vulnscout

# 2. Create a feature branch
git checkout -b feat/my-new-module

# 3. Set up dev environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install flake8

# 4. Make your changes

# 5. Lint your code
flake8 vulnscout.py modules/ --max-line-length=110

# 6. Test against example.com (safe target)
python3 vulnscout.py -d example.com --yes --headers

# 7. Commit and push
git commit -m "feat(my-module): add XYZ detection"
git push origin feat/my-new-module

# 8. Open a PR on GitHub
```

Read the full guide in [CONTRIBUTING.md](CONTRIBUTING.md).

### Good First Issues

Look for issues tagged [`good first issue`](https://github.com/shridhar3902/vulnscout/issues?q=label%3A%22good+first+issue%22) on GitHub.

### Hard Rules for All Contributors

1. **The scope-confirmation gate (`scope_gate.py`) must never be weakened or bypassed.** Any PR that removes or circumvents the `I CONFIRM` prompt will not be merged.
2. **No auto-exploitation.** Modules must only gather and present information — never send attack payloads or modify target data.
3. **No real credentials or target data** in PRs, commits, or issues.

---

## ❓ FAQ

**Q: Does VulnScout need any API keys?**  
A: No. All data sources are free and public: crt.sh for CT logs, public WHOIS servers, direct HTTP requests, and Python's stdlib SSL module.

**Q: Can I use VulnScout on Windows?**  
A: Yes. It automatically detects Windows terminals and falls back to ASCII-safe characters if your terminal doesn't support Unicode block characters. Use Windows Terminal for the best experience.

**Q: Can I use `--yes` to skip the scope prompt?**  
A: Only if authorization has been verified before running the tool — for example in a CI pipeline where you know exactly what's being scanned. Never use it to bypass the ethical check on targets you haven't confirmed authorization for.

**Q: VulnScout found an exposed `.env` file. What do I do?**  
A: Do NOT read or download the file contents if you are on a bug bounty program — document that the path returns HTTP 200 with a non-zero response size, screenshot it, and submit the finding. The fact that it's accessible is the finding; you don't need to prove credential content to report it.

**Q: The CVE hints module flagged CVE-XXXX. Am I definitely vulnerable?**  
A: No. CVE hints are surface intelligence, not confirmed findings. The module cross-references detected technology names — it doesn't know what version you're running. Check the CVE's affected version range against the target's actual version before treating it as valid.

**Q: Why does VulnScout scan ports if it's a "web" recon tool?**  
A: Because open database ports (MySQL, Redis, Elasticsearch, MongoDB) and remote access services (RDP, VNC, Telnet) exposed to the internet are critical web application attack surface, not just network findings. A publicly-accessible Redis on port 6379 is often more impactful than a missing header.

**Q: How is the risk score calculated?**  
A: A weighted sum of all findings across all modules: Critical = +25, High = +15, Medium = +8, Low = +3, Info = +0. The total is capped at 100. It is a relative indicator, not a CVSS score.

**Q: Can I add VulnScout to my own bug bounty toolkit?**  
A: Absolutely. It's MIT licensed. Use it, fork it, build on it. Just keep the scope gate intact and don't use it against unauthorized targets.

**Q: The WHOIS module returns an error. Why?**  
A: Some TLDs (especially newer gTLDs and some ccTLDs) have restricted WHOIS access or rate limiting. The module logs the specific error. Try again in a few minutes or check the domain's registrar directly.

---

## 📄 Legal & Ethics

### License
MIT License — see [LICENSE](LICENSE) for full text.

### Authorized Use
VulnScout is built exclusively for:
- ✅ Assets you personally own
- ✅ Targets in-scope for a bug bounty program you are **enrolled in** (HackerOne, Bugcrowd, Intigriti, YesWeHack, etc.)
- ✅ Lab and training environments (TryHackMe, HackTheBox, DVWA, VulnHub, etc.)
- ✅ Penetration testing engagements with written client authorization

### Prohibited Use
- ❌ Any target you do not own or have explicit written permission to test
- ❌ Out-of-scope assets in bug bounty programs (check the scope table carefully)
- ❌ Systems belonging to third parties without authorization
- ❌ Any use that violates local laws or regulations

### Legal Framework
Running active reconnaissance (port scans, path enumeration, header probes) against unauthorized targets may violate:
- **USA:** Computer Fraud and Abuse Act (CFAA)
- **UK:** Computer Misuse Act 1990
- **India:** Information Technology Act 2000 (Section 43, 66)
- **EU:** Directive 2013/40/EU on attacks against information systems
- **Other jurisdictions:** Equivalent cybercrime legislation

**You are solely responsible** for ensuring you have proper authorization before using this tool. The author and contributors accept no liability for misuse.

Read the full policy in [DISCLAIMER.md](DISCLAIMER.md).

### Responsible Disclosure
Found a security issue in VulnScout itself? Please report it privately — see [SECURITY.md](SECURITY.md).

---

## 📬 Contact & Community

- **GitHub Issues:** [Bug reports & feature requests](https://github.com/shridhar3902/vulnscout/issues)
- **GitHub Discussions:** [Questions & ideas](https://github.com/shridhar3902/vulnscout/discussions)
- **Security Reports:** See [SECURITY.md](SECURITY.md) — do NOT use public issues

---

<div align="center">

Built with ❤️ by [Shridhar Vinayak Kirtane](https://github.com/shridhar3902)

If VulnScout saved you time on a recon, consider giving it a ⭐ — it helps more people find the tool!

[![Star on GitHub](https://img.shields.io/github/stars/shridhar3902/vulnscout?style=social)](https://github.com/shridhar3902/vulnscout)

</div>

# Changelog

All notable changes to VulnScout will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [2.0.0] — 2025-07-01

### Added

#### New Scanning Modules
- `--ssl` **TLS/SSL Certificate Inspection** — validity, expiry countdown, issuer, SANs, cipher, self-signed detection (stdlib only)
- `--cors` **CORS Misconfiguration Probe** — 4-strategy origin testing: reflected, null, wildcard, credentials + origin
- `--waf` **WAF / CDN Fingerprinting** — detects Cloudflare, Akamai, Fastly, Imperva, F5 BIG-IP, ModSecurity, Barracuda, Sucuri via headers, cookies, and probe behaviour
- `--whois` **WHOIS Domain Intelligence** — registrar, expiry, nameservers, status flags, transfer-lock check (via python-whois)
- `--robots` **robots.txt & Sitemap Surface Mapper** — disallowed paths, sensitive pattern detection, sitemap URL enumeration
- `--vulns` **CVE Hints Module** — cross-references detected tech stack against a curated CVE database (WordPress, Drupal, Joomla, Laravel, Django, Next.js, jQuery, Nginx, Apache, Cloudflare)

#### Terminal Animation Engine (`modules/animation.py`)
- `Spinner` — thread-based braille-frame spinner with colour cycling
- `ProgressBar` — in-place animated fill bar using Unicode block characters
- `typewriter()` — character-by-character print with configurable delay
- `glitch_print()` — Matrix-style glitch-reveal effect for ASCII art
- `section_header()` — styled section dividers between modules
- `summary_table()` — colour-coded results table printed at scan end
- `risk_score_display()` — animated progress bar + severity label for risk score

#### Animated Banner (`modules/banner.py`)
- Large Unicode box-drawing ASCII logo with wave colour animation (per-line ANSI codes)
- Typewriter tagline
- Glitch-reveal effect before final clean render

#### Cinematic HTML Report (`modules/report.py`)
- Canvas particle network background (animated, WebGL-free)
- SVG animated risk gauge (0–100) with needle and count-up text
- Severity counter cards with JavaScript count-up animation on load
- Glassmorphism accordion module cards with slide-in CSS animation
- Port heatmap chips (red = dangerous, orange = moderate, green = standard)
- Per-finding severity badges with advisory links (CVE hints module)
- Progress bar rows for SSL/TLS and tech data
- Subject Alternative Name (SAN) pill display
- Auto-expands cards that have findings
- Print-freeze mode (animations paused, white background)
- Renderers for all 12 modules

#### CLI
- `--version` flag
- `--vulns` flag (CVE hints)
- `--ssl`, `--cors`, `--waf`, `--whois`, `--robots` flags
- Animated `section_header()` dividers between modules
- Final `summary_table()` with risk score per module
- Risk score computation (weighted by finding severity)
- `risk_score` saved to JSON output

#### GitHub Community Files
- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `.github/ISSUE_TEMPLATE/feature_request.yml`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/FUNDING.yml`
- `.github/workflows/ci.yml` (Python 3.10/3.11/3.12 matrix)
- `CONTRIBUTING.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`

### Changed
- `vulnscout.py` — complete orchestration rewrite; all print statements replaced with colour-coded ANSI output
- `modules/report.py` — complete HTML template rewrite
- `modules/banner.py` — complete rewrite with animation
- `modules/__init__.py` — exports all 16 modules
- `requirements.txt` — added `python-whois>=0.9.4`, `colorama>=0.4.6`
- `README.md` — complete rewrite with badges, feature matrix, module table, cross-platform install instructions

### Fixed
- WHOIS lookup correctly strips `www.` prefix before querying
- Exposed files check now uses `allow_redirects=False` correctly
- `vuln_hints` gracefully handles empty `detected_tech` list

---

## [1.0.0] — 2025-06-01

### Added
- Initial release
- Passive subdomain enumeration via crt.sh
- Security header audit (6 headers)
- Exposed sensitive file detection (15 paths)
- Technology fingerprinting (12 signatures)
- Common port scan (27 ports, concurrent)
- Reflected parameter / XSS surface discovery
- JSON + HTML report output
- Mandatory scope-confirmation gate
- `--yes` flag for scripted/CI use
- `install.sh` for Kali Linux

[Unreleased]: https://github.com/shridhar3902/vulnscout/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/shridhar3902/vulnscout/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/shridhar3902/vulnscout/releases/tag/v1.0.0

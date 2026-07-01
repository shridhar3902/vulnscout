"""
vuln_hints.py — CVE surface matcher / known-vulnerability hints module.

Cross-references the technology stack detected by tech_fingerprint against
a curated table of known CVEs and vulnerability classes for each technology.

This module does NOT perform active exploitation. It provides intelligence
hints to guide manual investigation. Always verify against the official
NVD / vendor advisories before reporting.
"""

from modules.animation import Spinner, RED, YELLOW, CYAN, BOLD

# CVE hint database: {tech_keyword: [(cve_id, severity, description, advisory_url)]}
CVE_HINTS = {
    "WordPress": [
        ("CVE-2023-2745", "medium", "Directory traversal via theme file loading", "https://wpscan.com/vulnerability/4e3d5e28"),
        ("CVE-2022-21661", "high",   "SQL injection via WP_Query", "https://wordpress.org/news/2022/01/wordpress-5-8-3-security-release/"),
        ("CVE-2021-29447", "medium", "XXE via media file upload (PHP 8+)", "https://nvd.nist.gov/vuln/detail/CVE-2021-29447"),
    ],
    "Drupal": [
        ("CVE-2018-7600", "critical", "Drupalgeddon2 — unauthenticated RCE", "https://www.drupal.org/sa-core-2018-002"),
        ("CVE-2018-7602", "critical", "Drupalgeddon3 — authenticated RCE", "https://www.drupal.org/sa-core-2018-004"),
    ],
    "Joomla": [
        ("CVE-2023-23752", "medium", "Unauthorized information disclosure via REST API", "https://developer.joomla.org/security-centre/894-20230201-core-improper-access-check.html"),
        ("CVE-2015-8562", "critical", "Remote code execution via PHP object injection", "https://nvd.nist.gov/vuln/detail/CVE-2015-8562"),
    ],
    "Laravel": [
        ("CVE-2021-3129", "critical", "RCE via debug mode + Ignition package chain", "https://nvd.nist.gov/vuln/detail/CVE-2021-3129"),
        ("CVE-2018-15133", "high",    "Unserialise RCE via APP_KEY exposure", "https://nvd.nist.gov/vuln/detail/CVE-2018-15133"),
    ],
    "Django": [
        ("CVE-2023-36053", "high",   "ReDoS in EmailValidator / URLValidator", "https://nvd.nist.gov/vuln/detail/CVE-2023-36053"),
        ("CVE-2022-28347", "critical","SQL injection via QuerySet.explain()", "https://nvd.nist.gov/vuln/detail/CVE-2022-28347"),
    ],
    "React": [
        ("CWE-79", "info", "Client-side XSS via dangerouslySetInnerHTML misuse — review code", "https://owasp.org/www-community/attacks/xss/"),
    ],
    "Next.js": [
        ("CVE-2025-29927", "critical","Authorization bypass via x-middleware-subrequest header", "https://nvd.nist.gov/vuln/detail/CVE-2025-29927"),
        ("CVE-2024-46982", "high",   "Cache poisoning via crafted request headers", "https://nvd.nist.gov/vuln/detail/CVE-2024-46982"),
    ],
    "jQuery": [
        ("CVE-2020-11022", "medium", "XSS via $.htmlPrefilter when processing HTML", "https://nvd.nist.gov/vuln/detail/CVE-2020-11022"),
        ("CVE-2019-11358", "medium", "Prototype pollution in jQuery.extend()", "https://nvd.nist.gov/vuln/detail/CVE-2019-11358"),
    ],
    "Nginx": [
        ("CVE-2021-23017", "critical","1-byte buffer overwrite in NGINX resolver", "https://nvd.nist.gov/vuln/detail/CVE-2021-23017"),
        ("CVE-2019-9511",  "high",    "HTTP/2 DoS — Data Dribble attack", "https://nvd.nist.gov/vuln/detail/CVE-2019-9511"),
    ],
    "Apache": [
        ("CVE-2021-41773", "critical","Path traversal / RCE in Apache 2.4.49", "https://nvd.nist.gov/vuln/detail/CVE-2021-41773"),
        ("CVE-2021-42013", "critical","Path traversal / RCE in Apache 2.4.49–50", "https://nvd.nist.gov/vuln/detail/CVE-2021-42013"),
        ("CVE-2022-22720", "high",    "HTTP request smuggling via keep-alive abuse", "https://nvd.nist.gov/vuln/detail/CVE-2022-22720"),
    ],
    "Cloudflare": [
        ("INFO-001", "info", "Cloudflare detected — real IP may be discoverable via historical DNS or subdomains", "https://github.com/christophetd/CloudFlair"),
    ],
}

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def run(target: str, detected_tech: list[str]) -> dict:
    out = {
        "status":       "ok",
        "target":       target,
        "matched_tech": [],
        "hints":        [],
        "findings":     [],
    }

    spinner = Spinner(f"Matching CVE hints for {len(detected_tech)} detected tech(s)")
    spinner.start()

    for tech in detected_tech:
        # Case-insensitive tech key lookup
        matched_key = next((k for k in CVE_HINTS if k.lower() == tech.lower()), None)
        if matched_key:
            out["matched_tech"].append(matched_key)
            for cve_id, severity, desc, url in CVE_HINTS[matched_key]:
                out["hints"].append({
                    "tech":     matched_key,
                    "cve":      cve_id,
                    "severity": severity,
                    "desc":     desc,
                    "advisory": url,
                })
                out["findings"].append({
                    "severity": severity,
                    "msg":      f"[{cve_id}] {matched_key}: {desc}",
                })

    # Sort by severity
    out["hints"].sort(key=lambda h: SEVERITY_ORDER.get(h["severity"], 99))
    out["findings"].sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], 99))

    critical_count = sum(1 for h in out["hints"] if h["severity"] == "critical")
    high_count     = sum(1 for h in out["hints"] if h["severity"] == "high")

    spinner.stop(
        f"{len(out['hints'])} CVE hints matched "
        f"({critical_count} critical, {high_count} high) — manual verification required",
        success=True,
    )

    return out

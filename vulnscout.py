#!/usr/bin/env python3
"""
VulnScout v2.0 — Authorized Web Recon & Vulnerability Surface Mapper
Author: Shridhar Vinayak Kirtane  |  github.com/shridhar3902/vulnscout

A modular, terminal-animated reconnaissance and vulnerability-surface
mapping tool for authorized security testing (bug bounty programs you
are enrolled in, CTF/lab targets, or assets you own).

IMPORTANT: This tool requires explicit scope confirmation before it
will run any module against a target. Do not use it against systems
you do not have written permission to test.
"""

import argparse
import datetime
import json
import os
import sys

from modules import (
    banner, scope_gate, subdomains, headers_check, exposed_files,
    tech_fingerprint, port_scan, reflected_params, report,
    ssl_check, cors_check, waf_detect, whois_lookup, robots_parser, vuln_hints,
)
from modules.animation import (
    section_header, summary_table, risk_score_display,
    CYAN, GREEN, RED, YELLOW, BOLD, MAGENTA, DIM,
)

VERSION = "2.0.0"


# ── CLI ───────────────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(
        prog="vulnscout",
        description="VulnScout v2 — Authorized web recon & vulnerability surface mapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python3 vulnscout.py -d example.com --all
  python3 vulnscout.py -d example.com --headers --ssl --cors
  python3 vulnscout.py -d example.com --all --yes -o my_report
        """,
    )
    p.add_argument("-d", "--domain",    required=True,       help="Target domain (e.g. example.com)")
    p.add_argument("-o", "--output",    default=None,        help="Report base name (no extension)")
    p.add_argument("--version",         action="version",    version=f"VulnScout {VERSION}")
    p.add_argument("--yes",             action="store_true", help="Skip interactive scope prompt")

    # Module flags
    g = p.add_argument_group("modules")
    g.add_argument("--all",        action="store_true", help="Run all modules")
    g.add_argument("--subdomains", action="store_true", help="Passive subdomain enumeration")
    g.add_argument("--headers",    action="store_true", help="Security header audit")
    g.add_argument("--exposed",    action="store_true", help="Exposed sensitive files")
    g.add_argument("--tech",       action="store_true", help="Technology fingerprinting")
    g.add_argument("--ports",      action="store_true", help="Common port scan (27 ports)")
    g.add_argument("--reflect",    action="store_true", help="Reflected parameter / XSS surface")
    g.add_argument("--ssl",        action="store_true", help="TLS/SSL certificate inspection")
    g.add_argument("--cors",       action="store_true", help="CORS misconfiguration probe")
    g.add_argument("--waf",        action="store_true", help="WAF / CDN fingerprinting")
    g.add_argument("--whois",      action="store_true", help="WHOIS domain intelligence")
    g.add_argument("--robots",     action="store_true", help="robots.txt & sitemap surface map")
    g.add_argument("--vulns",      action="store_true", help="CVE hints for detected tech stack")
    return p.parse_args()


# ── Risk scoring ──────────────────────────────────────────────────────────────
def _compute_risk(results: dict) -> int:
    """Compute a 0–100 risk score from all findings across modules."""
    severity_weights = {"critical": 25, "high": 15, "medium": 8, "low": 3, "info": 0}
    score = 0
    for mod_data in results.get("modules", {}).values():
        if isinstance(mod_data, dict):
            for finding in mod_data.get("findings", []):
                sev = finding.get("severity", "info").lower()
                score += severity_weights.get(sev, 0)
    return min(score, 100)


# ── Summary rows builder ──────────────────────────────────────────────────────
def _summary_row(name: str, data: dict) -> tuple:
    if not data:
        return (name, "skip", 0, "info")
    status   = data.get("status", "ok")
    findings = data.get("findings", [])
    count    = len(findings)
    if status == "error":
        return (name, "error", 0, "info")
    if count == 0:
        return (name, "ok", 0, "ok")
    sevs = [f.get("severity", "info") for f in findings]
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    top   = sorted(sevs, key=lambda s: order.get(s, 99))[0]
    return (name, "ok", count, top)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    banner.show(VERSION)
    args   = parse_args()
    target = (args.domain.strip().lower()
              .replace("https://", "").replace("http://", "").strip("/"))

    # Scope gate
    if not args.yes:
        if not scope_gate.confirm(target):
            print(f"\n{RED('[!]')} Scope not confirmed. Exiting without performing any action.")
            sys.exit(1)
    else:
        print(f"{CYAN('[i]')} --yes passed: assuming authorization confirmed for {BOLD(target)}")

    results = {
        "target":    target,
        "version":   VERSION,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat() + "Z",
        "modules":   {},
    }

    # Determine which modules to run
    explicit = any([
        args.subdomains, args.headers, args.exposed, args.tech,
        args.ports, args.reflect, args.ssl, args.cors, args.waf,
        args.whois, args.robots, args.vulns,
    ])
    run_all = args.all or not explicit

    # ── Passive intel ─────────────────────────────────────────────────────────
    if run_all or args.whois:
        section_header("WHOIS Domain Intelligence", "◈")
        results["modules"]["whois"] = whois_lookup.run(target)

    if run_all or args.subdomains:
        section_header("Passive Subdomain Enumeration", "◈")
        results["modules"]["subdomains"] = subdomains.run(target)

    if run_all or args.robots:
        section_header("robots.txt & Sitemap Surface", "◈")
        results["modules"]["robots"] = robots_parser.run(target)

    # ── Active fingerprinting ─────────────────────────────────────────────────
    if run_all or args.tech:
        section_header("Technology Stack Fingerprinting", "◈")
        results["modules"]["tech_fingerprint"] = tech_fingerprint.run(target)

    if run_all or args.waf:
        section_header("WAF / CDN Detection", "◈")
        results["modules"]["waf"] = waf_detect.run(target)

    if run_all or args.ssl:
        section_header("TLS / SSL Certificate Inspection", "◈")
        results["modules"]["ssl"] = ssl_check.run(target)

    if run_all or args.headers:
        section_header("HTTP Security Headers Audit", "◈")
        results["modules"]["headers"] = headers_check.run(target)

    if run_all or args.cors:
        section_header("CORS Misconfiguration Probe", "◈")
        results["modules"]["cors"] = cors_check.run(target)

    if run_all or args.exposed:
        section_header("Exposed Sensitive Files", "◈")
        results["modules"]["exposed_files"] = exposed_files.run(target)

    if run_all or args.ports:
        section_header("Port Scan (27 common services)", "◈")
        results["modules"]["ports"] = port_scan.run(target)

    if run_all or args.reflect:
        section_header("Reflected Parameter Discovery (XSS Surface)", "◈")
        results["modules"]["reflected_params"] = reflected_params.run(target)

    # ── CVE hints (uses tech_fingerprint results) ─────────────────────────────
    if run_all or args.vulns:
        section_header("CVE / Vulnerability Hints", "◈")
        detected_tech = []
        tf = results["modules"].get("tech_fingerprint", {})
        if tf:
            detected_tech = tf.get("detected", [])
        results["modules"]["vuln_hints"] = vuln_hints.run(target, detected_tech)

    # ── Summary ───────────────────────────────────────────────────────────────
    section_header("SCAN SUMMARY", "◉")
    mod_map = {
        "WHOIS":         "whois",
        "Subdomains":    "subdomains",
        "robots.txt":    "robots",
        "Tech Stack":    "tech_fingerprint",
        "WAF/CDN":       "waf",
        "SSL/TLS":       "ssl",
        "Sec Headers":   "headers",
        "CORS":          "cors",
        "Exposed Files": "exposed_files",
        "Port Scan":     "ports",
        "Reflected Param":"reflected_params",
        "CVE Hints":     "vuln_hints",
    }
    rows = [
        _summary_row(label, results["modules"].get(key, {}))
        for label, key in mod_map.items()
        if key in results["modules"]
    ]
    summary_table(rows)

    risk = _compute_risk(results)
    results["risk_score"] = risk
    risk_score_display(risk)

    # ── Write reports ─────────────────────────────────────────────────────────
    ts       = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_base = args.output or f"vulnscout_{target}_{ts}"
    os.makedirs("reports", exist_ok=True)
    json_path, html_path = report.write(results, out_base)

    print(f"\n{GREEN('[+]')} Scan complete  —  risk score: {BOLD(str(risk))}/100")
    print(f"{GREEN('[+]')} JSON report : {CYAN(json_path)}")
    print(f"{GREEN('[+]')} HTML report : {CYAN(html_path)}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED('[!]')} Interrupted by user. Exiting.")
        sys.exit(130)

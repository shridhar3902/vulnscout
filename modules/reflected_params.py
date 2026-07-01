"""
Reflected parameter discovery.

This module identifies GET parameters whose value is reflected
unescaped in the HTTP response — a common precondition for XSS.
It uses a benign, non-executing canary string and does NOT inject
script payloads or attempt exploitation. Manual verification with
a tool like Burp Suite is still required before reporting a finding.
"""
import requests
from urllib.parse import urlparse, parse_qs

COMMON_PARAMS = ["q", "search", "id", "page", "ref", "redirect", "url",
                  "name", "query", "keyword", "lang", "category"]

CANARY = "vsCanary12345"


def run(target):
    base = f"https://{target}"
    out = {"status": "ok", "tested": [], "reflected": []}
    try:
        resp = requests.get(base, timeout=15)
    except requests.RequestException as e:
        out["status"] = "error"
        out["error"] = str(e)
        return out

    for param in COMMON_PARAMS:
        test_url = f"{base}/?{param}={CANARY}"
        try:
            r = requests.get(test_url, timeout=10)
            out["tested"].append(param)
            if CANARY in r.text:
                out["reflected"].append({
                    "param": param,
                    "url": test_url,
                    "note": "Value reflected unescaped — verify manually for XSS, do not assume exploitability"
                })
        except requests.RequestException:
            continue

    print(f"    -> {len(out['reflected'])} parameters showed unescaped reflection (manual verification required)")
    return out

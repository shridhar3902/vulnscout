"""
waf_detect.py — WAF / CDN fingerprinting module.

Identifies Web Application Firewalls and CDN providers by inspecting:
  - Response headers (Server, Via, X-Cache, CF-RAY, X-Served-By, etc.)
  - Cookie names injected by WAF middleware
  - Response body error-page signatures when a suspicious request is sent
  - Timing/behavioural signals (response-time delta on malicious payload)

Detection is passive-first, then sends one benign-looking SQLi probe to
observe WAF interception behaviour (no actual exploitation attempted).
"""

import time
import requests
from modules.animation import Spinner, GREEN, YELLOW, RED, CYAN, BOLD


_TIMEOUT = 12

# Header-based fingerprints: {header_name: {header_value_fragment: waf_name}}
HEADER_SIGS = {
    "Server": {
        "cloudflare":    "Cloudflare",
        "awselb":        "AWS ELB",
        "akamaighost":   "Akamai",
        "bigip":         "F5 BIG-IP",
        "barracuda":     "Barracuda",
        "sucuri":        "Sucuri",
    },
    "Via": {
        "cloudfront":    "Amazon CloudFront",
        "akamai":        "Akamai",
        "varnish":       "Varnish CDN",
        "fastly":        "Fastly",
    },
    "X-Powered-By": {
        "imperva":       "Imperva Incapsula",
    },
    "CF-RAY":            {"*": "Cloudflare"},
    "X-Sucuri-ID":       {"*": "Sucuri"},
    "X-CDN":             {"*": "CDN (generic)"},
    "X-Cache":           {"*": "Caching proxy"},
    "X-Served-By":       {"*": "Fastly/Varnish"},
}

# Cookie name hints
COOKIE_SIGS = {
    "__cfduid":     "Cloudflare",
    "incap_ses":    "Imperva Incapsula",
    "visid_incap":  "Imperva Incapsula",
    "barra_counter_session": "Barracuda",
    "BIGipServer":  "F5 BIG-IP",
}

# Body-based error page signatures (sent after WAF probe)
BODY_SIGS = {
    "cloudflare":           "Cloudflare",
    "attention required":   "Cloudflare",
    "incapsula incident":   "Imperva Incapsula",
    "sucuri cloudproxy":    "Sucuri",
    "akamai error":         "Akamai",
    "you have been blocked":"Generic WAF",
    "request blocked":      "Generic WAF",
    "access denied":        "Generic WAF",
    "mod_security":         "ModSecurity",
}


def _header_detect(resp: requests.Response) -> list[str]:
    found = []
    for header, sigs in HEADER_SIGS.items():
        val = resp.headers.get(header, "").lower()
        if not val:
            continue
        if "*" in sigs and val:
            # generic presence signal
            found.append(sigs["*"])
        for fragment, waf in sigs.items():
            if fragment != "*" and fragment in val:
                found.append(waf)
    return found


def _cookie_detect(resp: requests.Response) -> list[str]:
    found = []
    for cookie_name in resp.cookies.keys():
        for sig, waf in COOKIE_SIGS.items():
            if sig.lower() in cookie_name.lower():
                found.append(waf)
    return found


def _body_detect(body: str) -> list[str]:
    body_lower = body.lower()
    return [waf for sig, waf in BODY_SIGS.items() if sig in body_lower]


def run(target: str) -> dict:
    url  = f"https://{target}"
    out  = {
        "status":        "ok",
        "url":           url,
        "detected_wafs": [],
        "headers_seen":  {},
        "probe_blocked": False,
        "findings":      [],
    }

    spinner = Spinner(f"Fingerprinting WAF/CDN on {target}")
    spinner.start()

    try:
        # Normal request
        r1 = requests.get(url, timeout=_TIMEOUT,
                          headers={"User-Agent": "Mozilla/5.0 (compatible; VulnScout/2.0)"})
        out["headers_seen"] = dict(r1.headers)

        detected = set()
        detected.update(_header_detect(r1))
        detected.update(_cookie_detect(r1))

        # Probe request — benign SQLi string to trigger WAF interception
        probe_url = f"{url}/?id=1'+OR+'1'%3D'1"
        t0 = time.time()
        r2 = requests.get(probe_url, timeout=_TIMEOUT,
                          headers={"User-Agent": "Mozilla/5.0 (compatible; VulnScout/2.0)"})
        latency = time.time() - t0

        detected.update(_header_detect(r2))
        detected.update(_body_detect(r2.text))

        if r2.status_code in (403, 406, 429, 503):
            out["probe_blocked"] = True
            detected.add("Unknown WAF (block behaviour)")

        out["detected_wafs"] = sorted(detected)

        if detected:
            out["findings"].append({
                "severity": "info",
                "msg": f"WAF/CDN detected: {', '.join(out['detected_wafs'])}",
            })
        else:
            out["findings"].append({
                "severity": "info",
                "msg": "No WAF/CDN signatures matched — may be unprotected or custom WAF",
            })

        summary = ", ".join(out["detected_wafs"]) if out["detected_wafs"] else "none detected"
        spinner.stop(f"WAF/CDN: {summary}", success=True)

    except requests.RequestException as e:
        out["status"] = "error"
        out["error"]  = str(e)
        spinner.stop(f"Connection failed: {e}", success=False)

    return out

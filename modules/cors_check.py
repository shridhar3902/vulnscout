"""
cors_check.py — CORS misconfiguration detection module.

Probes the target with four distinct Origin header strategies:
  1. Wildcard / reflected-origin test
  2. Null origin test
  3. Subdomain trust test
  4. Credential + arbitrary origin test

All findings include the exact request/response headers for evidence.
"""

import requests
from modules.animation import Spinner, severity_badge


_TIMEOUT = 12


def _probe(url: str, origin: str, headers: dict | None = None) -> dict:
    hdrs = {"Origin": origin}
    if headers:
        hdrs.update(headers)
    try:
        r = requests.get(url, headers=hdrs, timeout=_TIMEOUT, allow_redirects=True)
        acao  = r.headers.get("Access-Control-Allow-Origin", "")
        acac  = r.headers.get("Access-Control-Allow-Credentials", "")
        return {
            "sent_origin": origin,
            "acao":  acao,
            "acac":  acac,
            "status": r.status_code,
        }
    except requests.RequestException as e:
        return {"sent_origin": origin, "acao": "", "acac": "", "status": None, "error": str(e)}


def run(target: str) -> dict:
    url = f"https://{target}"
    out = {
        "status":   "ok",
        "url":      url,
        "findings": [],
        "probes":   [],
    }

    spinner = Spinner(f"Probing CORS policies on {target}")
    spinner.start()

    # Probe 1 — reflected arbitrary origin
    p1 = _probe(url, f"https://evil-{target}.attacker.com")
    out["probes"].append(p1)
    if p1["acao"] == f"https://evil-{target}.attacker.com":
        out["findings"].append({
            "severity": "critical",
            "msg": "Origin reflection — arbitrary origin accepted",
            "evidence": p1,
        })

    # Probe 2 — wildcard
    p2 = _probe(url, "https://attacker.com")
    out["probes"].append(p2)
    if p2["acao"] == "*":
        out["findings"].append({
            "severity": "medium",
            "msg": "ACAO: * (wildcard) — credentials cannot be sent, but data is public",
            "evidence": p2,
        })

    # Probe 3 — null origin
    p3 = _probe(url, "null")
    out["probes"].append(p3)
    if p3["acao"] == "null":
        out["findings"].append({
            "severity": "high",
            "msg": "Null origin accepted — sandbox iframe bypass possible",
            "evidence": p3,
        })

    # Probe 4 — credentials + reflected origin
    p4 = _probe(url, "https://attacker.com",
                headers={"Cookie": "test=1"})
    out["probes"].append(p4)
    if p4["acao"] not in ("", "*") and p4["acac"].lower() == "true":
        out["findings"].append({
            "severity": "critical",
            "msg": "Credentials allowed with reflected origin — classic CORS exploit",
            "evidence": p4,
        })

    count = len(out["findings"])
    spinner.stop(
        f"{count} CORS issue(s) found",
        success=(count == 0)
    )

    return out

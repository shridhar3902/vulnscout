import requests

SECURITY_HEADERS = {
    "Strict-Transport-Security": "Protects against protocol downgrade / cookie hijacking",
    "Content-Security-Policy": "Mitigates XSS and data injection attacks",
    "X-Frame-Options": "Mitigates clickjacking",
    "X-Content-Type-Options": "Prevents MIME-sniffing",
    "Referrer-Policy": "Controls referrer leakage",
    "Permissions-Policy": "Restricts powerful browser features",
}


def run(target):
    url = f"https://{target}"
    out = {"status": "ok", "url": url, "missing": [], "present": {}, "server": None}
    try:
        resp = requests.get(url, timeout=15, allow_redirects=True)
        out["server"] = resp.headers.get("Server")
        for h, desc in SECURITY_HEADERS.items():
            if h in resp.headers:
                out["present"][h] = resp.headers[h]
            else:
                out["missing"].append({"header": h, "risk": desc})
        out["status_code"] = resp.status_code
        print(f"    -> {len(out['missing'])} missing security headers out of {len(SECURITY_HEADERS)} checked")
    except requests.RequestException as e:
        out["status"] = "error"
        out["error"] = str(e)
        print(f"    -> Could not connect: {e}")
    return out

import re
import requests

TECH_SIGNATURES = {
    "WordPress": [r"wp-content", r"wp-includes"],
    "Drupal": [r"sites/all/themes", r"Drupal\.settings"],
    "Joomla": [r"/media/jui/", r"Joomla!"],
    "Laravel": [r"laravel_session"],
    "Django": [r"csrfmiddlewaretoken"],
    "React": [r"__REACT_DEVTOOLS", r"data-reactroot"],
    "Next.js": [r"__NEXT_DATA__"],
    "jQuery": [r"jquery(\.min)?\.js"],
    "Bootstrap": [r"bootstrap(\.min)?\.css"],
    "Nginx": [r"nginx"],
    "Apache": [r"Apache"],
    "Cloudflare": [r"cloudflare"],
}


def run(target):
    url = f"https://{target}"
    out = {"status": "ok", "url": url, "server_header": None, "powered_by": None, "detected": []}
    try:
        resp = requests.get(url, timeout=15)
        out["server_header"] = resp.headers.get("Server")
        out["powered_by"] = resp.headers.get("X-Powered-By")
        haystack = resp.text + str(resp.headers)
        for tech, patterns in TECH_SIGNATURES.items():
            for pat in patterns:
                if re.search(pat, haystack, re.IGNORECASE):
                    out["detected"].append(tech)
                    break
        out["detected"] = sorted(set(out["detected"]))
        print(f"    -> Detected: {', '.join(out['detected']) if out['detected'] else 'no signatures matched'}")
    except requests.RequestException as e:
        out["status"] = "error"
        out["error"] = str(e)
        print(f"    -> Could not connect: {e}")
    return out

import requests


def run(target):
    """Passive subdomain enumeration using crt.sh certificate transparency logs."""
    found = set()
    try:
        resp = requests.get(f"https://crt.sh/?q=%25.{target}&output=json", timeout=20)
        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError:
                data = []
            for entry in data:
                name_value = entry.get("name_value", "")
                for sub in name_value.split("\n"):
                    sub = sub.strip().lower()
                    if sub.endswith(target) and "*" not in sub:
                        found.add(sub)
    except requests.RequestException as e:
        return {"status": "error", "error": str(e), "subdomains": []}

    subs = sorted(found)
    print(f"    -> Found {len(subs)} unique subdomains (passive, via crt.sh)")
    return {"status": "ok", "count": len(subs), "subdomains": subs}

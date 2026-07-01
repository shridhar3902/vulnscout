import requests

CANDIDATE_PATHS = [
    ".git/HEAD",
    ".env",
    ".env.local",
    "config.php.bak",
    "backup.zip",
    "backup.sql",
    ".DS_Store",
    "wp-config.php.bak",
    ".htaccess",
    "id_rsa",
    ".aws/credentials",
    "server-status",
    "phpinfo.php",
    ".svn/entries",
    "docker-compose.yml",
]


def run(target):
    base = f"https://{target}"
    findings = []
    for path in CANDIDATE_PATHS:
        url = f"{base}/{path}"
        try:
            resp = requests.get(url, timeout=8, allow_redirects=False)
            if resp.status_code == 200 and len(resp.content) > 0:
                findings.append({"path": path, "url": url, "status_code": resp.status_code,
                                  "size_bytes": len(resp.content)})
        except requests.RequestException:
            continue
    print(f"    -> {len(findings)} potentially exposed paths found out of {len(CANDIDATE_PATHS)} checked")
    return {"status": "ok", "checked": len(CANDIDATE_PATHS), "findings": findings}

"""
robots_parser.py — robots.txt and sitemap.xml surface mapper.

Fetches and parses robots.txt to extract:
  - Disallowed paths (attack surface hints)
  - Sitemap references
  - Per-agent rules

Then fetches sitemap.xml (or sitemap URL from robots.txt) to enumerate
publicly listed URLs that may expose admin panels, APIs, or staging paths.
"""

import re
import requests
from urllib.parse import urljoin, urlparse

from modules.animation import Spinner, YELLOW, GREEN, CYAN

_TIMEOUT = 12

# Patterns in disallowed paths that might indicate sensitive areas
SENSITIVE_PATTERNS = [
    r"admin", r"login", r"dashboard", r"api/", r"internal",
    r"staging", r"dev", r"test", r"backup", r"config",
    r"\.git", r"\.env", r"secret", r"private", r"hidden",
    r"wp-admin", r"phpmyadmin", r"cpanel", r"plesk",
]


def _flag_sensitive(path: str) -> str | None:
    for pat in SENSITIVE_PATTERNS:
        if re.search(pat, path, re.IGNORECASE):
            return pat
    return None


def _fetch(url: str) -> tuple[int, str]:
    try:
        r = requests.get(url, timeout=_TIMEOUT, allow_redirects=True,
                         headers={"User-Agent": "VulnScout/2.0"})
        return r.status_code, r.text
    except requests.RequestException:
        return 0, ""


def _parse_robots(text: str, base_url: str) -> dict:
    disallowed  = []
    allowed     = []
    sitemaps    = []
    user_agents = []
    current_ua  = "*"

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        key   = key.strip().lower()
        value = value.strip()
        if key == "user-agent":
            current_ua = value
            if value not in user_agents:
                user_agents.append(value)
        elif key == "disallow" and value:
            disallowed.append({"path": value, "agent": current_ua})
        elif key == "allow" and value:
            allowed.append(value)
        elif key == "sitemap":
            sitemaps.append(value)

    return {
        "user_agents": user_agents,
        "disallowed":  disallowed,
        "allowed":     allowed,
        "sitemaps":    sitemaps,
    }


def _parse_sitemap(text: str, limit: int = 50) -> list[str]:
    return re.findall(r"<loc>(.*?)</loc>", text, re.IGNORECASE)[:limit]


def run(target: str) -> dict:
    base_url = f"https://{target}"
    out = {
        "status":          "ok",
        "robots_found":    False,
        "sitemap_found":   False,
        "user_agents":     [],
        "disallowed":      [],
        "sitemaps":        [],
        "sitemap_urls":    [],
        "sensitive_paths": [],
        "findings":        [],
    }

    spinner = Spinner(f"Parsing robots.txt & sitemap for {target}")
    spinner.start()

    # Fetch robots.txt
    robots_status, robots_text = _fetch(f"{base_url}/robots.txt")
    if robots_status == 200 and robots_text:
        out["robots_found"] = True
        parsed = _parse_robots(robots_text, base_url)
        out.update({
            "user_agents": parsed["user_agents"],
            "disallowed":  parsed["disallowed"],
            "sitemaps":    parsed["sitemaps"],
        })

        # Flag sensitive disallowed paths
        for entry in parsed["disallowed"]:
            flag = _flag_sensitive(entry["path"])
            if flag:
                out["sensitive_paths"].append(entry["path"])
                out["findings"].append({
                    "severity": "medium",
                    "msg": f"Sensitive path in Disallow: {entry['path']} (matches '{flag}')",
                })

        if not parsed["disallowed"]:
            out["findings"].append({"severity": "info", "msg": "robots.txt found but no Disallow rules"})
    else:
        out["findings"].append({"severity": "info", "msg": "robots.txt not found (404)"})

    # Fetch sitemap
    sitemap_urls_to_try = out["sitemaps"] or [f"{base_url}/sitemap.xml"]
    for sm_url in sitemap_urls_to_try[:3]:
        sm_status, sm_text = _fetch(sm_url)
        if sm_status == 200 and sm_text:
            out["sitemap_found"] = True
            urls = _parse_sitemap(sm_text)
            out["sitemap_urls"].extend(urls)
            # Flag interesting sitemap URLs
            for url in urls:
                flag = _flag_sensitive(url)
                if flag and url not in [f["msg"] for f in out["findings"]]:
                    out["findings"].append({
                        "severity": "low",
                        "msg": f"Interesting sitemap URL: {url}",
                    })
            break

    spinner.stop(
        f"robots.txt: {'✔' if out['robots_found'] else '✘'}  |  "
        f"{len(out['sensitive_paths'])} sensitive paths  |  "
        f"{len(out['sitemap_urls'])} sitemap URLs",
        success=True,
    )

    return out

"""
whois_lookup.py — WHOIS domain intelligence module.

Retrieves and parses WHOIS records for the target domain using the
python-whois library. Falls back gracefully if the library is not
installed, instructing the user how to add it.

Information gathered:
  - Registrar & WHOIS server
  - Creation / expiration / updated dates
  - Name servers
  - Registrant organisation (if not redacted)
  - Domain status flags
"""

import datetime
from modules.animation import Spinner, YELLOW, RED, GREEN, CYAN


def _days_until(dt) -> int | None:
    if dt is None:
        return None
    if isinstance(dt, list):
        dt = dt[0]
    now = datetime.datetime.now()
    if hasattr(dt, "tzinfo") and dt.tzinfo is not None:
        now = datetime.datetime.now(datetime.timezone.utc)
    return (dt - now).days


def run(target: str) -> dict:
    # Strip www prefix for WHOIS lookup
    domain = target.lstrip("www.") if target.startswith("www.") else target

    out = {
        "status":     "ok",
        "domain":     domain,
        "registrar":  None,
        "created":    None,
        "expires":    None,
        "updated":    None,
        "nameservers": [],
        "status_flags": [],
        "org":        None,
        "days_until_expiry": None,
        "findings":   [],
    }

    spinner = Spinner(f"Querying WHOIS for {domain}")
    spinner.start()

    try:
        import whois  # python-whois
    except ImportError:
        out["status"] = "error"
        out["error"]  = "python-whois not installed. Run: pip install python-whois"
        spinner.stop("python-whois not installed", success=False)
        return out

    try:
        w = whois.whois(domain)

        out["registrar"]   = getattr(w, "registrar",   None)
        out["org"]         = getattr(w, "org",          None)
        out["nameservers"] = [ns.lower() for ns in (getattr(w, "name_servers", []) or []) if ns]

        def _fmt(val):
            if val is None:
                return None
            if isinstance(val, list):
                val = val[0]
            return val.strftime("%Y-%m-%d") if hasattr(val, "strftime") else str(val)

        out["created"] = _fmt(getattr(w, "creation_date",    None))
        out["expires"] = _fmt(getattr(w, "expiration_date",  None))
        out["updated"] = _fmt(getattr(w, "updated_date",     None))

        exp_raw = getattr(w, "expiration_date", None)
        out["days_until_expiry"] = _days_until(exp_raw)

        status_raw = getattr(w, "status", []) or []
        if isinstance(status_raw, str):
            status_raw = [status_raw]
        out["status_flags"] = [str(s).split(" ")[0] for s in status_raw]

        # Findings
        ddays = out["days_until_expiry"]
        if ddays is not None:
            if ddays < 0:
                out["findings"].append({"severity": "critical", "msg": "Domain registration has EXPIRED"})
            elif ddays < 30:
                out["findings"].append({"severity": "high",   "msg": f"Domain expires in {ddays} days"})
            elif ddays < 90:
                out["findings"].append({"severity": "medium", "msg": f"Domain expires in {ddays} days"})

        if "clientTransferProhibited" not in " ".join(out["status_flags"]):
            out["findings"].append({"severity": "low", "msg": "Transfer lock not set — domain hijack risk"})

        summary = f"Registrar: {out['registrar'] or '?'}  |  Expires: {out['expires'] or '?'}  ({ddays}d)"
        spinner.stop(summary, success=True)

    except Exception as e:
        out["status"] = "error"
        out["error"]  = str(e)
        spinner.stop(f"WHOIS query failed: {e}", success=False)

    return out

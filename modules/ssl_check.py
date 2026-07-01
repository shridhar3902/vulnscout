"""
ssl_check.py — TLS/SSL certificate inspection module.

Inspects the TLS certificate for the target:
  - Validity period & days until expiry
  - Issuer and subject details
  - Subject Alternative Names (SAN)
  - Protocol version negotiated
  - Self-signed detection

No third-party libraries required beyond the standard ssl module.
"""

import ssl
import socket
import datetime

from modules.animation import Spinner, severity_badge, GREEN, YELLOW, RED, CYAN


def _days_until(dt: datetime.datetime) -> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return (dt - now).days


def _get_cert(hostname: str, port: int = 443, timeout: float = 10.0) -> dict:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with socket.create_connection((hostname, port), timeout=timeout) as raw:
        with ctx.wrap_socket(raw, server_hostname=hostname) as conn:
            return {
                "cert":    conn.getpeercert(),
                "cipher":  conn.cipher(),
                "version": conn.version(),
            }


def run(target: str) -> dict:
    out = {
        "status":       "ok",
        "host":         target,
        "valid":        False,
        "days_left":    None,
        "expires":      None,
        "issued_to":    None,
        "issued_by":    None,
        "sans":         [],
        "cipher":       None,
        "tls_version":  None,
        "self_signed":  False,
        "findings":     [],
    }

    spinner = Spinner(f"Probing TLS on {target}:443")
    spinner.start()

    try:
        data    = _get_cert(target)
        cert    = data["cert"]
        cipher  = data["cipher"]
        version = data["version"]

        out["cipher"]      = f"{cipher[0]} ({cipher[2]}-bit)"
        out["tls_version"] = version

        # Parse subject / issuer
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer", []))
        out["issued_to"] = subject.get("commonName", "—")
        out["issued_by"] = issuer.get("commonName",  "—")
        out["self_signed"] = subject == issuer

        # Expiry
        not_after = cert.get("notAfter")
        if not_after:
            exp_dt = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            out["expires"]   = exp_dt.strftime("%Y-%m-%d")
            out["days_left"] = _days_until(exp_dt)
            out["valid"]     = out["days_left"] > 0

        # SANs
        sans = []
        for kind, value in cert.get("subjectAltName", []):
            if kind == "DNS":
                sans.append(value)
        out["sans"] = sans

        # Findings
        if out["self_signed"]:
            out["findings"].append({"severity": "high", "msg": "Certificate is self-signed"})
        if out["days_left"] is not None and out["days_left"] < 0:
            out["findings"].append({"severity": "critical", "msg": "Certificate has EXPIRED"})
        elif out["days_left"] is not None and out["days_left"] < 14:
            out["findings"].append({"severity": "high", "msg": f"Certificate expires in {out['days_left']} days"})
        elif out["days_left"] is not None and out["days_left"] < 30:
            out["findings"].append({"severity": "medium", "msg": f"Certificate expires in {out['days_left']} days"})
        if version in ("TLSv1", "TLSv1.1", "SSLv3", "SSLv2"):
            out["findings"].append({"severity": "high", "msg": f"Weak protocol in use: {version}"})

        summary = f"TLS {version} | expires {out['expires']} ({out['days_left']}d) | {len(sans)} SANs"
        spinner.stop(summary, success=True)
        print(f"    -> Issuer: {out['issued_by']}  |  Self-signed: {out['self_signed']}")

    except ssl.SSLError as e:
        out["status"] = "error"
        out["error"]  = f"SSL error: {e}"
        spinner.stop(f"SSL error: {e}", success=False)
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        out["status"] = "error"
        out["error"]  = str(e)
        spinner.stop(f"Connection failed: {e}", success=False)

    return out

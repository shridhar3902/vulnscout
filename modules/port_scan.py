import socket
import concurrent.futures

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 111: "RPCbind", 135: "MSRPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
    1433: "MSSQL", 1521: "Oracle", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 6379: "Redis", 8000: "HTTP-Alt", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt", 9200: "Elasticsearch", 27017: "MongoDB",
}


def _check(ip, port, timeout=1.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((ip, port)) == 0:
                return port
    except socket.error:
        return None
    return None


def run(target):
    out = {"status": "ok", "open_ports": []}
    try:
        ip = socket.gethostbyname(target)
        out["resolved_ip"] = ip
    except socket.gaierror as e:
        out["status"] = "error"
        out["error"] = f"DNS resolution failed: {e}"
        return out

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(_check, ip, port): port for port in COMMON_PORTS}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            if future.result() == port:
                out["open_ports"].append({"port": port, "service": COMMON_PORTS[port]})

    out["open_ports"] = sorted(out["open_ports"], key=lambda x: x["port"])
    print(f"    -> {len(out['open_ports'])} open ports found (out of {len(COMMON_PORTS)} checked)")
    return out

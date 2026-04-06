import socket
import requests
import ssl
import os
import json
import dns.resolver
import whois
from colorama import Fore, Style
from config.settings import HACKERTARGET_URL, TIMEOUT, REPORT_DIR

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "api", "dev", "test", "staging",
    "blog", "shop", "store", "app", "mobile", "m", "portal", "vpn",
    "remote", "secure", "login", "auth", "cdn", "static", "assets",
    "media", "img", "images", "video", "upload", "download", "files",
    "docs", "help", "support", "status", "monitor", "dashboard",
    "panel", "cpanel", "webmail", "smtp", "pop", "imap",
    "ns1", "ns2", "mx", "beta", "alpha", "old", "new",
    "v1", "v2", "backup", "db", "database", "sql", "mysql"
]

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def get_dns_records(domain):
    records = {}
    for rtype in ["A", "MX", "TXT", "NS", "CNAME", "AAAA", "SOA"]:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records[rtype] = [str(r) for r in answers]
        except:
            records[rtype] = []
    return records

def get_subdomains_crt(domain):
    subdomains = []
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            data = r.json()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    sub = sub.strip().lstrip("*.")
                    if sub and sub not in subdomains:
                        subdomains.append(sub)
    except:
        pass
    return subdomains

def dns_bruteforce(domain):
    print(f"{Fore.YELLOW}[*] DNS Bruteforce Running...{Style.RESET_ALL}")
    found = []
    for sub in COMMON_SUBDOMAINS:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            found.append({"subdomain": target, "ip": ip})
            print(f"{Fore.GREEN}    [FOUND] {target} -> {ip}{Style.RESET_ALL}")
        except:
            pass
    return found

def get_ssl_info(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(TIMEOUT)
            s.connect((domain, 443))
            cert = s.getpeercert()
            return {
                "subject": dict(x[0] for x in cert.get("subject", [])),
                "issuer": dict(x[0] for x in cert.get("issuer", [])),
                "valid_from": cert.get("notBefore"),
                "valid_until": cert.get("notAfter"),
                "san": [x[1] for x in cert.get("subjectAltName", [])]
            }
    except:
        return {}

def get_wayback(domain):
    try:
        url = f"http://archive.org/wayback/available?url={domain}"
        r = requests.get(url, timeout=TIMEOUT)
        data = r.json()
        snapshot = data.get("archived_snapshots", {}).get("closest", {})
        return {
            "available": snapshot.get("available"),
            "url": snapshot.get("url"),
            "timestamp": snapshot.get("timestamp")
        }
    except:
        return {}

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": str(w.registrar),
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "emails": w.emails,
            "country": str(w.country)
        }
    except:
        return {}

def get_tech_stack(domain):
    tech = []
    try:
        r = requests.get(f"http://{domain}", timeout=TIMEOUT)
        headers = r.headers
        if "X-Powered-By" in headers:
            tech.append(headers["X-Powered-By"])
        if "Server" in headers:
            tech.append(headers["Server"])
        if "wp-content" in r.text:
            tech.append("WordPress")
        if "Joomla" in r.text:
            tech.append("Joomla")
        if "Drupal" in r.text:
            tech.append("Drupal")
        if "Laravel" in r.text:
            tech.append("Laravel")
        if "Django" in r.text:
            tech.append("Django")
        if "React" in r.text:
            tech.append("React")
        if "Vue" in r.text:
            tech.append("Vue.js")
        if "bootstrap" in r.text.lower():
            tech.append("Bootstrap")
    except:
        pass
    return list(set(tech))

def run_domain_osint(domain):
    print(f"\n{Fore.CYAN}[+] Domain Analysis: {domain}{Style.RESET_ALL}")
    result = {"target": domain, "type": "domain"}

    print(f"{Fore.YELLOW}[*] Resolving IP Address...{Style.RESET_ALL}")
    result["ip"] = get_ip(domain)
    print(f"{Fore.GREEN}    IP: {result['ip']}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Fetching DNS Records...{Style.RESET_ALL}")
    result["dns"] = get_dns_records(domain)

    print(f"{Fore.YELLOW}[*] Finding Subdomains via CRT.sh...{Style.RESET_ALL}")
    crt_subs = get_subdomains_crt(domain)
    print(f"{Fore.GREEN}    Found {len(crt_subs)} via CRT.sh{Style.RESET_ALL}")

    brute_subs = dns_bruteforce(domain)
    print(f"{Fore.GREEN}    Found {len(brute_subs)} via Bruteforce{Style.RESET_ALL}")

    result["subdomains"] = list(set(crt_subs))
    result["bruteforce_subdomains"] = brute_subs

    print(f"{Fore.YELLOW}[*] Fetching SSL Certificate Info...{Style.RESET_ALL}")
    result["ssl"] = get_ssl_info(domain)
    if result["ssl"]:
        print(f"{Fore.GREEN}    SSL Valid Until: {result['ssl'].get('valid_until')}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Checking Wayback Machine...{Style.RESET_ALL}")
    result["wayback"] = get_wayback(domain)
    if result["wayback"].get("available"):
        print(f"{Fore.GREEN}    Snapshot Found: {result['wayback'].get('url')}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Fetching WHOIS Info...{Style.RESET_ALL}")
    result["whois"] = get_whois(domain)

    print(f"{Fore.YELLOW}[*] Detecting Tech Stack...{Style.RESET_ALL}")
    result["tech_stack"] = get_tech_stack(domain)

    # Auto Save
    os.makedirs(REPORT_DIR, exist_ok=True)
    save_path = f"{REPORT_DIR}/domain_{domain.replace('.', '_')}.txt"
    mode = "a" if os.path.exists(save_path) else "w"
    with open(save_path, mode) as f:
        f.write(f"\n=== Scan: {domain} ===\n")
        f.write(json.dumps(result, indent=2, default=str))

    print(f"{Fore.GREEN}[+] Auto Saved: {save_path}{Style.RESET_ALL}")
    return result

import requests
import socket
from colorama import Fore, Style
from config.settings import IPAPI_URL, HACKERTARGET_URL, TIMEOUT

def get_ip_info(ip):
    try:
        r = requests.get(f"{IPAPI_URL}{ip}", timeout=TIMEOUT)
        return r.json()
    except:
        return {}

def get_reverse_dns(ip):
    try:
        r = requests.get(f"{HACKERTARGET_URL}/reversedns/?q={ip}", timeout=TIMEOUT)
        return r.text.strip()
    except:
        return None

def get_open_ports(ip):
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

def get_reverse_ip(ip):
    try:
        r = requests.get(f"{HACKERTARGET_URL}/reverseiplookup/?q={ip}", timeout=TIMEOUT)
        domains = [d.strip() for d in r.text.splitlines() if d.strip()]
        return domains
    except:
        return []

def run_ip_osint(ip):
    print(f"\n{Fore.CYAN}[+] IP Analysis: {ip}{Style.RESET_ALL}")
    result = {"target": ip, "type": "ip"}

    print(f"{Fore.YELLOW}[*] Fetching IP Information...{Style.RESET_ALL}")
    info = get_ip_info(ip)
    result["location"] = {
        "country": info.get("country"),
        "region": info.get("regionName"),
        "city": info.get("city"),
        "isp": info.get("isp"),
        "org": info.get("org"),
        "lat": info.get("lat"),
        "lon": info.get("lon")
    }
    print(f"{Fore.GREEN}    Location: {result['location']['city']}, {result['location']['country']}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Checking Reverse DNS...{Style.RESET_ALL}")
    result["reverse_dns"] = get_reverse_dns(ip)

    print(f"{Fore.YELLOW}[*] Scanning Open Ports...{Style.RESET_ALL}")
    result["open_ports"] = get_open_ports(ip)
    print(f"{Fore.GREEN}    Open Ports: {result['open_ports']}{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Running Reverse IP Lookup...{Style.RESET_ALL}")
    result["reverse_ip_domains"] = get_reverse_ip(ip)
    print(f"{Fore.GREEN}    Found {len(result['reverse_ip_domains'])} Domains{Style.RESET_ALL}")

    return result

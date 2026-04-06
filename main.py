import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
from modules.domain import run_domain_osint
from modules.ip import run_ip_osint
from modules.email_osint import run_email_osint
from modules.username import run_username_osint
from modules.report import generate_report
from modules.dorking import run_dorking
from modules.risk_score import run_risk_score
from modules.pdf_report import generate_pdf
from modules.correlation import correlate

init(autoreset=True)

def banner():
    print(f"""{Fore.CYAN}
╔══════════════════════════════════════════════╗
║          OSINTool - Advanced v2.0            ║
║       Open Source Intelligence Tool         ║
║          For Educational Use Only           ║
╚══════════════════════════════════════════════╝
{Style.RESET_ALL}""")

def detect_target(target):
    import re
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        return "ip"
    elif "@" in target:
        return "email"
    elif re.match(r'^[a-zA-Z0-9_\-\.]+$', target) and "." not in target:
        return "username"
    else:
        return "domain"

def full_scan(target, ttype):
    result = None
    if ttype == "domain":
        result = run_domain_osint(target)
    elif ttype == "ip":
        result = run_ip_osint(target)
    elif ttype == "email":
        result = run_email_osint(target)
    elif ttype == "username":
        result = run_username_osint(target)

    if result:
        # Correlation
        correlation = correlate(result)
        result["correlation"] = correlation

        # Risk Score
        risk = run_risk_score(result)
        result["risk"] = {
            "score": risk["score"],
            "level": risk["level"],
            "breakdown": risk["breakdown"]
        }

        # Reports
        json_path, html_path = generate_report(result)
        pdf_path = generate_pdf(result, risk)

        print(f"\n{Fore.GREEN}[+] All Reports Saved!")
        print(f"    JSON : {json_path}")
        print(f"    HTML : {html_path}")
        print(f"    PDF  : {pdf_path}{Style.RESET_ALL}")

    return result

def main():
    banner()

    while True:
        print(f"""
{Fore.YELLOW}[1]  Domain Analysis
[2]  IP Analysis
[3]  Email Analysis
[4]  Username Search
[5]  Auto Detect & Full Scan
[6]  Google Dork Generator
[0]  Exit{Style.RESET_ALL}
""")
        choice = input(f"{Fore.CYAN}Select Option: {Style.RESET_ALL}").strip()

        if choice == "0":
            print(f"{Fore.RED}Goodbye! 👋{Style.RESET_ALL}")
            break

        elif choice == "6":
            target = input(f"{Fore.CYAN}Enter Domain: {Style.RESET_ALL}").strip()
            run_dorking(target)

        elif choice in ["1", "2", "3", "4", "5"]:
            target = input(f"{Fore.CYAN}Enter Target: {Style.RESET_ALL}").strip()

            if choice == "1":
                full_scan(target, "domain")
            elif choice == "2":
                full_scan(target, "ip")
            elif choice == "3":
                full_scan(target, "email")
            elif choice == "4":
                full_scan(target, "username")
            elif choice == "5":
                ttype = detect_target(target)
                print(f"{Fore.GREEN}[*] Auto Detected: {ttype}{Style.RESET_ALL}")
                full_scan(target, ttype)
        else:
            print(f"{Fore.RED}[!] Invalid Option!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

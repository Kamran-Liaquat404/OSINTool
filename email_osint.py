import requests
import re
import os
import json
import hashlib
from colorama import Fore, Style
from config.settings import TIMEOUT, REPORT_DIR

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def get_email_domain_info(email):
    domain = email.split("@")[1]
    try:
        import dns.resolver
        mx = dns.resolver.resolve(domain, "MX")
        return {"domain": domain, "mx_records": [str(r) for r in mx]}
    except:
        return {"domain": domain, "mx_records": []}

def check_gravatar(email):
    email_hash = hashlib.md5(email.lower().encode()).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
    try:
        r = requests.get(url, timeout=TIMEOUT)
        if r.status_code == 200:
            return f"https://www.gravatar.com/avatar/{email_hash}"
        return None
    except:
        return None

def check_disposable(email):
    disposable_domains = [
        "mailinator.com", "guerrillamail.com", "tempmail.com",
        "throwaway.email", "yopmail.com", "10minutemail.com",
        "trashmail.com", "fakeinbox.com", "sharklasers.com"
    ]
    domain = email.split("@")[1].lower()
    return domain in disposable_domains

def analyze_email_pattern(email):
    username = email.split("@")[0]
    patterns = []
    if re.match(r'^[a-z]+\.[a-z]+$', username):
        patterns.append("firstname.lastname format")
    if re.match(r'^[a-z]+[0-9]+$', username):
        patterns.append("name + numbers format")
    if "_" in username:
        patterns.append("underscore separator")
    return patterns

def find_related_usernames(email):
    username = email.split("@")[0]
    variations = [
        username,
        username.replace(".", "_"),
        username.replace(".", ""),
        username.replace("_", "."),
        username.lower(),
    ]
    return list(set(variations))

def run_email_osint(email):
    print(f"\n{Fore.CYAN}[+] Email Analysis: {email}{Style.RESET_ALL}")
    result = {"target": email, "type": "email"}

    if not validate_email(email):
        print(f"{Fore.RED}[!] Invalid Email Format!{Style.RESET_ALL}")
        return result

    print(f"{Fore.YELLOW}[*] Fetching Domain Info...{Style.RESET_ALL}")
    result["domain_info"] = get_email_domain_info(email)

    print(f"{Fore.YELLOW}[*] Checking Gravatar...{Style.RESET_ALL}")
    result["gravatar"] = check_gravatar(email)
    if result["gravatar"]:
        print(f"{Fore.GREEN}    Gravatar Found!{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Checking Disposable Email...{Style.RESET_ALL}")
    result["is_disposable"] = check_disposable(email)
    if result["is_disposable"]:
        print(f"{Fore.RED}    [!] Disposable Email Detected!{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}    Legitimate Email Domain{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}[*] Analyzing Email Pattern...{Style.RESET_ALL}")
    result["patterns"] = analyze_email_pattern(email)

    print(f"{Fore.YELLOW}[*] Finding Related Usernames...{Style.RESET_ALL}")
    result["possible_usernames"] = find_related_usernames(email)

    # Auto Save
    os.makedirs(REPORT_DIR, exist_ok=True)
    safe_name = email.replace("@", "_at_").replace(".", "_")
    save_path = f"{REPORT_DIR}/email_{safe_name}.txt"
    mode = "a" if os.path.exists(save_path) else "w"
    with open(save_path, mode) as f:
        f.write(f"\n=== Scan: {email} ===\n")
        f.write(json.dumps(result, indent=2, default=str))

    print(f"{Fore.GREEN}[+] Auto Saved: {save_path}{Style.RESET_ALL}")
    return result

from colorama import Fore, Style

def generate_dorks(target):
    dorks = {
        "Sensitive Files": [
            f'site:{target} ext:pdf',
            f'site:{target} ext:xls OR ext:xlsx',
            f'site:{target} ext:doc OR ext:docx',
            f'site:{target} ext:txt',
            f'site:{target} ext:log',
            f'site:{target} ext:sql',
            f'site:{target} ext:env',
            f'site:{target} ext:config',
        ],
        "Login Pages": [
            f'site:{target} inurl:login',
            f'site:{target} inurl:admin',
            f'site:{target} inurl:dashboard',
            f'site:{target} inurl:portal',
            f'site:{target} inurl:wp-admin',
            f'site:{target} inurl:cpanel',
        ],
        "Exposed Info": [
            f'site:{target} intext:password',
            f'site:{target} intext:username',
            f'site:{target} intext:api_key',
            f'site:{target} intext:secret',
            f'site:{target} intext:"index of"',
        ],
        "Subdomains": [
            f'site:*.{target}',
            f'site:{target} -www',
        ],
        "Cached Pages": [
            f'cache:{target}',
            f'related:{target}',
        ]
    }
    return dorks

def run_dorking(target):
    print(f"\n{Fore.CYAN}[+] Google Dork Generator: {target}{Style.RESET_ALL}")
    result = {"target": target, "type": "dorking", "dorks": {}}

    dorks = generate_dorks(target)

    for category, dork_list in dorks.items():
        print(f"\n{Fore.YELLOW}  [{category}]{Style.RESET_ALL}")
        result["dorks"][category] = dork_list
        for dork in dork_list:
            print(f"{Fore.GREEN}    {dork}{Style.RESET_ALL}")

    total = sum(len(v) for v in dorks.values())
    print(f"\n{Fore.CYAN}[+] Total Dorks Generated: {total}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[!] Copy and paste these in Google manually{Style.RESET_ALL}")

    return result

from colorama import Fore, Style

def correlate(data):
    print(f"\n{Fore.CYAN}[+] Running Auto Correlation Engine...{Style.RESET_ALL}")
    links = []

    target = data.get("target")
    dtype = data.get("type")

    # Domain correlations
    if dtype == "domain":
        ip = data.get("ip")
        if ip:
            links.append(f"Domain [{target}] --> IP [{ip}]")

        subdomains = data.get("subdomains", [])
        for sub in subdomains[:5]:
            links.append(f"Domain [{target}] --> Subdomain [{sub}]")

        whois = data.get("whois", {})
        emails = whois.get("emails", [])
        if emails:
            if isinstance(emails, list):
                for email in emails:
                    links.append(f"Domain [{target}] --> Email [{email}]")
            else:
                links.append(f"Domain [{target}] --> Email [{emails}]")

        tech = data.get("tech_stack", [])
        for t in tech:
            links.append(f"Domain [{target}] --> Technology [{t}]")

    # IP correlations
    elif dtype == "ip":
        location = data.get("location", {})
        city = location.get("city")
        isp = location.get("isp")
        if city:
            links.append(f"IP [{target}] --> Location [{city}]")
        if isp:
            links.append(f"IP [{target}] --> ISP [{isp}]")

        reverse_domains = data.get("reverse_ip_domains", [])
        for domain in reverse_domains[:5]:
            links.append(f"IP [{target}] --> Hosted Domain [{domain}]")

        ports = data.get("open_ports", [])
        for port in ports:
            links.append(f"IP [{target}] --> Open Port [{port}]")

    # Email correlations
    elif dtype == "email":
        username = target.split("@")[0]
        domain = target.split("@")[1]
        links.append(f"Email [{target}] --> Username [{username}]")
        links.append(f"Email [{target}] --> Domain [{domain}]")

        possible = data.get("possible_usernames", [])
        for u in possible:
            if u != username:
                links.append(f"Email [{target}] --> Possible Username [{u}]")

        if data.get("gravatar"):
            links.append(f"Email [{target}] --> Gravatar Profile Found")

    # Username correlations
    elif dtype == "username":
        found = data.get("found", [])
        for platform in found:
            links.append(f"Username [{target}] --> {platform['platform']} [{platform['url']}]")

    # Print
    print(f"\n{Fore.YELLOW}  Correlation Map:{Style.RESET_ALL}")
    for link in links:
        print(f"{Fore.GREEN}    [-->] {link}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}[+] Total Connections Found: {len(links)}{Style.RESET_ALL}")

    return {"links": links, "total": len(links)}

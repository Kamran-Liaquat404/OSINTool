from colorama import Fore, Style

DANGEROUS_PORTS = [21, 22, 23, 25, 445, 3389, 3306]

def calculate_risk(data):
    score = 0
    breakdown = []

    # Open Ports Check
    open_ports = data.get("open_ports", [])
    for port in open_ports:
        if port in DANGEROUS_PORTS:
            score += 15
            breakdown.append(f"Dangerous port open: {port} (+15)")
        else:
            score += 5
            breakdown.append(f"Port open: {port} (+5)")

    # Subdomains
    subdomains = data.get("subdomains", [])
    if len(subdomains) > 20:
        score += 20
        breakdown.append(f"Large attack surface - {len(subdomains)} subdomains (+20)")
    elif len(subdomains) > 10:
        score += 10
        breakdown.append(f"Medium attack surface - {len(subdomains)} subdomains (+10)")
    elif len(subdomains) > 0:
        score += 5
        breakdown.append(f"Small attack surface - {len(subdomains)} subdomains (+5)")

    # Emails Exposed
    whois_data = data.get("whois", {})
    emails = whois_data.get("emails", [])
    if emails:
        score += 10
        breakdown.append(f"Emails exposed in WHOIS (+10)")

    # Tech Stack
    tech = data.get("tech_stack", [])
    if tech:
        score += 10
        breakdown.append(f"Tech stack visible: {', '.join(tech)} (+10)")

    # Username found on platforms
    found_platforms = data.get("found", [])
    if len(found_platforms) > 5:
        score += 15
        breakdown.append(f"High social media exposure - {len(found_platforms)} platforms (+15)")
    elif len(found_platforms) > 0:
        score += 5
        breakdown.append(f"Social media presence found (+5)")

    # Cap at 100
    score = min(score, 100)

    # Risk Level
    if score >= 70:
        level = "CRITICAL"
        color = Fore.RED
    elif score >= 50:
        level = "HIGH"
        color = Fore.YELLOW
    elif score >= 30:
        level = "MEDIUM"
        color = Fore.CYAN
    else:
        level = "LOW"
        color = Fore.GREEN

    return {
        "score": score,
        "level": level,
        "breakdown": breakdown,
        "color": color
    }

def run_risk_score(data):
    print(f"\n{Fore.CYAN}[+] Calculating Risk Score...{Style.RESET_ALL}")
    risk = calculate_risk(data)

    print(f"\n{risk['color']}  Risk Score : {risk['score']}/100")
    print(f"  Risk Level : {risk['level']}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}  Breakdown:{Style.RESET_ALL}")
    for item in risk['breakdown']:
        print(f"{Fore.WHITE}    - {item}{Style.RESET_ALL}")

    return risk

# OSINTool v2.0 – Complete OSINT Recon & Investigation Suite

[![GitHub Repo Size](https://img.shields.io/github/repo-size/Kamran-Liaquat404/OSINTool)](https://github.com/Kamran-Liaquat404/OSINTool)
[![License](https://img.shields.io/github/license/Kamran-Liaquat404/OSINTool)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)

**OSINTool v2.0** is a powerful all‑in‑one OSINT (Open Source Intelligence) tool for cybersecurity enthusiasts, bug bounty hunters, and digital investigators. It performs domain, IP, email, and username recon with automated correlation, risk scoring, and multi‑format report generation.

---

## 🚀 Features

- **Domain Analysis:** IP resolution, DNS records, subdomain finder (CRT.sh), DNS bruteforce, SSL checks, Wayback snapshots, WHOIS lookup, tech stack detection  
- **IP Analysis:** Geolocation, ISP info, reverse DNS, open port scanning, reverse IP lookup  
- **Email Analysis:** Validation, MX check, Gravatar detection, disposable email detection, email pattern analysis  
- **Username & Social Analysis:** 55+ platform checks, multi‑threaded scans, saved results  
- **Google Dork Generator:** Sensitive files, login pages, exposed info, subdomains, cached pages  
- **Auto Correlation Engine:** Link domains → IPs → subdomains → emails → usernames  
- **Risk Scoring:** 0–100 score with LOW/MEDIUM/HIGH/CRITICAL levels  
- **Reports:** JSON, HTML, PDF, and TXT formats  
- **Technical:** Termux & Linux compatible, multi‑threaded scanning, no API keys required

---

## 📥 Installation (Termux & Linux)

**Termux:**
```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Kamran-Liaquat404/OSINTool.git
cd OSINTool
pip install -r requirements.txt
chmod +x run.sh
./run.sh

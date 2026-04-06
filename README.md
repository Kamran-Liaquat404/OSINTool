# OSINTool v2.0 – Complete OSINT Recon & Investigation Suite

[![GitHub Repo Size](https://img.shields.io/github/repo-size/Kamran-Liaquat404/OSINTool)](https://github.com/Kamran-Liaquat404/OSINTool)
[![License](https://img.shields.io/github/license/Kamran-Liaquat404/OSINTool)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)

**OSINTool v2.0** is a powerful all-in-one OSINT (Open Source Intelligence) tool for cybersecurity enthusiasts, bug bounty hunters, and digital investigators. It provides domain, IP, email, and username analysis with automated correlation, risk scoring, and multi-format report generation. Fully compatible with Termux (Android) and Linux-based systems. Multi-threaded and no API keys required.

---

## 🌐 Features

- **Domain Analysis:** IP resolution, DNS records (A, MX, TXT, NS, CNAME, AAAA, SOA), subdomain finder (CRT.sh), DNS bruteforce, SSL checks, Wayback snapshots, WHOIS lookup, tech stack detection  
- **IP Analysis:** Geolocation, ISP info, reverse DNS, open port scanning, reverse IP lookup  
- **Email Analysis:** Validation, MX check, Gravatar detection, disposable email detection, email pattern analysis  
- **Username & Social Analysis:** 55+ platform checks, multi-threaded scanning, auto-save results  
- **Google Dork Generator:** Sensitive files, login pages, exposed info, subdomains, cached pages  
- **Auto Correlation Engine:** Domain → IP → Subdomains → Emails, Email → Username → Platforms, IP → Location → ISP → Domains  
- **Risk Scoring:** 0–100 score with LOW / MEDIUM / HIGH / CRITICAL levels  
- **Reports:** JSON, HTML, PDF, and TXT formats  
- **Technical:** Termux & Linux compatible, multi-threaded scanning, no API keys required, auto target detection

---

## 📥 Installation (Termux & Linux)

✅ Termux:

pkg update && pkg upgrade -y

pkg install python git -y

git clone https://github.com/Kamran-Liaquat404/OSINTool.git
cd OSINTool

pip install -r requirements.txt

chmod +x run.sh

./run.sh


✅ Linux (Kali / Ubuntu / Parrot OS):

sudo apt update && sudo apt upgrade -y 

sudo apt install python3 git -y 

git clone https://github.com/Kamran-Liaquat404/OSINTool.git

cd OSINTool 

pip3 install -r requirements.txt

chmod +x run.sh 

./run.sh

## Usage

python osintool.py

1. Enter your license key  
2. Select the recon module (Domain / IP / Email / Username / Google Dorks)  
3. Run scans and generate reports automatically  

## License

OSINTool Pro License v1.0 - For personal and professional use only. Redistribution or resale without permission is prohibited. Reverse engineering is strictly prohibited. Commercial use requires a valid paid license.

## Disclaimer

This tool is for educational and legal professional use only. Do NOT use it for unethical or illegal activities. The developer is not responsible for misuse.

## Contact

Email: thekamranliaquat@gmail.com  
Telegram: https://t.me/spider404lab

## Changelog

v2.0 - Added auto correlation engine, multi-threaded scanning, enhanced risk scoring and reporting system

import requests
import os
import json
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from config.settings import TIMEOUT, THREADS, REPORT_DIR

PLATFORMS = {
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "Twitter": "https://twitter.com/{}",
    "Instagram": "https://instagram.com/{}",
    "Reddit": "https://reddit.com/user/{}",
    "LinkedIn": "https://linkedin.com/in/{}",
    "YouTube": "https://youtube.com/@{}",
    "TikTok": "https://tiktok.com/@{}",
    "Pinterest": "https://pinterest.com/{}",
    "Telegram": "https://t.me/{}",
    "Medium": "https://medium.com/@{}",
    "Dev.to": "https://dev.to/{}",
    "Hackernews": "https://news.ycombinator.com/user?id={}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Twitch": "https://twitch.tv/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Keybase": "https://keybase.io/{}",
    "Gravatar": "https://gravatar.com/{}",
    "Flickr": "https://flickr.com/people/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "WordPress": "https://{}.wordpress.com",
    "About.me": "https://about.me/{}",
    "Behance": "https://behance.net/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Fiverr": "https://fiverr.com/{}",
    "ProductHunt": "https://producthunt.com/@{}",
    "Stackoverflow": "https://stackoverflow.com/users/{}",
    "Quora": "https://quora.com/profile/{}",
    "Goodreads": "https://goodreads.com/{}",
    "Last.fm": "https://last.fm/user/{}",
    "Chess.com": "https://chess.com/member/{}",
    "Lichess": "https://lichess.org/@/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "PSN": "https://psnprofiles.com/{}",
    "Roblox": "https://roblox.com/user.aspx?username={}",
    "Codecademy": "https://codecademy.com/profiles/{}",
    "Hackerrank": "https://hackerrank.com/{}",
    "Leetcode": "https://leetcode.com/{}",
    "Codeforces": "https://codeforces.com/profile/{}",
    "Replit": "https://replit.com/@{}",
    "NPM": "https://npmjs.com/~{}",
    "PyPI": "https://pypi.org/user/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "VK": "https://vk.com/{}",
    "Xing": "https://xing.com/profile/{}",
    "Imgur": "https://imgur.com/user/{}",
    "9GAG": "https://9gag.com/u/{}",
    "Giphy": "https://giphy.com/{}",
    "Snapchat": "https://snapchat.com/add/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Slideshare": "https://slideshare.net/{}",
    "Academia": "https://academia.edu/{}",
    "ResearchGate": "https://researchgate.net/profile/{}",
    "Etsy": "https://etsy.com/shop/{}",
    "eBay": "https://ebay.com/usr/{}",
}

def check_platform(username, platform, url):
    try:
        full_url = url.format(username)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(full_url, timeout=TIMEOUT, allow_redirects=True, headers=headers)
        if r.status_code == 200:
            return {"platform": platform, "url": full_url, "status": "Found"}
    except:
        pass
    return None

def run_username_osint(username):
    print(f"\n{Fore.CYAN}[+] Username Analysis: {username}{Style.RESET_ALL}")
    result = {"target": username, "type": "username", "found": []}

    print(f"{Fore.YELLOW}[*] Checking {len(PLATFORMS)} Platforms...{Style.RESET_ALL}")

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [
            executor.submit(check_platform, username, platform, url)
            for platform, url in PLATFORMS.items()
        ]
        for future in futures:
            res = future.result()
            if res:
                result["found"].append(res)
                print(f"{Fore.GREEN}    [FOUND] {res['platform']}: {res['url']}{Style.RESET_ALL}")

    # Auto Save
    os.makedirs(REPORT_DIR, exist_ok=True)
    save_path = f"{REPORT_DIR}/username_{username}.txt"
    mode = "a" if os.path.exists(save_path) else "w"
    with open(save_path, mode) as f:
        f.write(f"\n=== Scan: {username} ===\n")
        for item in result["found"]:
            f.write(f"[FOUND] {item['platform']}: {item['url']}\n")

    print(f"{Fore.CYAN}[+] Total Found: {len(result['found'])}/{len(PLATFORMS)} Platforms{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Auto Saved: {save_path}{Style.RESET_ALL}")
    return result

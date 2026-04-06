import json
import os
from datetime import datetime
from config.settings import REPORT_DIR

def save_json(data, filename):
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = f"{REPORT_DIR}/{filename}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4, default=str)
    return path

def save_html(data, filename):
    os.makedirs(REPORT_DIR, exist_ok=True)
    path = f"{REPORT_DIR}/{filename}.html"
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>OSINT Report - {data.get('target')}</title>
    <style>
        body {{ font-family: monospace; background: #0d0d0d; color: #00ff00; padding: 20px; }}
        h1 {{ color: #00ffff; }}
        h2 {{ color: #ffff00; border-bottom: 1px solid #333; }}
        pre {{ background: #1a1a1a; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>OSINT Report</h1>
    <p>Target: {data.get('target')}</p>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <pre>{json.dumps(data, indent=4, default=str)}</pre>
</body>
</html>"""
    with open(path, "w") as f:
        f.write(html)
    return path

def generate_report(data):
    target = data.get("target", "unknown").replace(".", "_").replace("@", "_at_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{target}_{timestamp}"
    json_path = save_json(data, filename)
    html_path = save_html(data, filename)
    return json_path, html_path

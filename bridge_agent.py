import os
import requests
import json
import time
from datetime import datetime
import base64

GITHUB_TOKEN = os.getenv("AGENT_TOKEN")
REPO = "Tom-debug-design/atomicbot-agent"
BRANCH = "main"
FILE_NAME = "heartbeat.txt"

def commit_file(filename, content, message):
    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    get_resp = requests.get(url, headers=headers)
    if get_resp.status_code == 200:
        sha = get_resp.json()["sha"]
    else:
        sha = None

    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH
    }

    if sha:
        payload["sha"] = sha

    resp = requests.put(url, headers=headers, data=json.dumps(payload))
    print(f"Commit status: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    print("Bridge-agent startet og holder seg aktiv 🟢")

    while True:
        timestamp = datetime.utcnow().isoformat()
        content = f"Bridge heartbeat: {timestamp}Z"
        commit_file(FILE_NAME, content, f"Auto heartbeat commit {timestamp}")
        print("✅ Heartbeat pushed to GitHub.")
        time.sleep(60)
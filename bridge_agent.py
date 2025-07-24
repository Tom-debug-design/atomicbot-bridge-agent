import os
import requests
import json

# Krever GITHUB_TOKEN som env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = "Tom-debug-design/atomicbot-agent"
BRANCH = "main"

def commit_file(filename, content, commit_msg):
    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Hent SHA for eksisterende fil
    get = requests.get(url, headers=headers)
    sha = get.json().get("sha") if get.status_code == 200 else None

    payload = {
        "message": commit_msg,
        "content": content.encode("utf-8").decode("utf-8"),
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    print("Status:", response.status_code)
    print("Respons:", response.json())

if __name__ == "__main__":
    print("Bridge-agent klar (placeholder)")

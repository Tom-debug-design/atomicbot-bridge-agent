import os
import requests
from datetime import datetime
import time
import subprocess

GITHUB_TOKEN = os.getenv("AGENT_TOKEN")
REPO = "Tom-debug-design/atomicbot-bridge-agent"
FILE_NAME = "bridge_heartbeat.txt"

def write_heartbeat():
    now = datetime.utcnow().isoformat()
    with open(FILE_NAME, "w") as f:
        f.write(f"Bridge heartbeat: {now}Z\n")

def git_commit_and_push():
    subprocess.run(["git", "config", "--global", "user.email", "bot@atomic.com"])
    subprocess.run(["git", "config", "--global", "user.name", "AtomicBot Bridge"])
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", f"https://x-access-token:{GITHUB_TOKEN}@github.com/{REPO}.git"])
    subprocess.run(["git", "add", FILE_NAME])
    subprocess.run(["git", "commit", "-m", f"Bridge ping {datetime.utcnow().isoformat()}"])
    subprocess.run(["git", "branch", "-M", "main"])
    subprocess.run(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    while True:
        try:
            write_heartbeat()
            git_commit_and_push()
            print("✅ Bridge heartbeat sent.")
        except Exception as e:
            print("❌ Error in bridge-agent:", e)
        time.sleep(60)
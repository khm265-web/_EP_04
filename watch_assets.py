import time
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets.json")

def get_mtime():
    return os.path.getmtime(ASSETS_PATH)

def git_sync():
    subprocess.run(["git", "add", "assets.json"], cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", "auto-sync assets.json"], cwd=BASE_DIR)
    subprocess.run(["git", "push"], cwd=BASE_DIR)
    print("✅ assets.json 已同步到 GitHub")

def watch():
    last_mtime = get_mtime()
    print("👀 開始監察 assets.json...")
    while True:
        time.sleep(5)
        current_mtime = get_mtime()
        if current_mtime != last_mtime:
            last_mtime = current_mtime
            time.sleep(1)
            git_sync()

if __name__ == "__main__":
    watch()
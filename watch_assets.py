import time
import subprocess
import os
import hashlib
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITIGNORE_PATH = os.path.join(BASE_DIR, ".gitignore")


def get_watch_files():
    """讀 .gitignore，攞返所有 `!` 開頭嘅白名單檔案"""
    files = []
    with open(GITIGNORE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("!") and line != "!.gitignore":
                files.append(line[1:])
    return files


def get_hash(path):
    full = os.path.join(BASE_DIR, path)
    if not os.path.exists(full):
        return None
    with open(full, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def git_sync(changed_files):
    subprocess.run(["git", "add"] + changed_files, cwd=BASE_DIR)
    subprocess.run(["git", "commit", "-m", f"auto-sync: {', '.join(changed_files)}"], cwd=BASE_DIR)
    result = subprocess.run(["git", "push"], cwd=BASE_DIR)
    if result.returncode == 0:
        print(f"✅ 已同步: {', '.join(changed_files)}")
    else:
        print("❌ Push 失敗，請檢查 git 狀態")


def watch():
    watch_files = get_watch_files()
    last_hashes = {f: get_hash(f) for f in watch_files}
    print(f"👀 開始監察 {len(watch_files)} 個檔案(來自 .gitignore)...")

    while True:
        time.sleep(5)

        # 每次 loop 重新讀 .gitignore，支援之後新增/移除白名單檔案
        current_files = get_watch_files()
        if set(current_files) != set(last_hashes.keys()):
            print("🔄 偵測到 .gitignore 白名單有變動，重新載入監察清單")
            last_hashes = {f: get_hash(f) for f in current_files}

        changed = []
        for f in current_files:
            current = get_hash(f)
            if current != last_hashes.get(f):
                last_hashes[f] = current
                changed.append(f)
        if changed:
            git_sync(changed)


if __name__ == "__main__":
    watch()
import os
import sys
import json
import glob

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
JOBS_DIR   = os.path.join(BASE_DIR, "jobs")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")

def resolve_assets():
    assets = {}
    if os.path.isdir(ASSETS_DIR):
        for path in glob.glob(os.path.join(ASSETS_DIR, "*")):
            if path.lower().endswith(IMAGE_EXTS):
                key = os.path.splitext(os.path.basename(path))[0]
                assets[key] = path
    return assets

ANGLES = [
    "front view, full body",
    "front view, half body close-up",
    "back view, full body",
    "back view, half body",
    "left side profile, full body",
    "right side profile, full body",
    "3/4 left angle, full body",
    "3/4 right angle, full body",
    "front facing close-up portrait",
    "back close-up",
    "left profile close-up",
    "right profile close-up",
    "looking up from below, full body",
    "looking down from above, full body",
    "low angle shot",
    "high angle shot",
    "walking pose, side view",
    "sitting pose, front view",
    "action pose, dynamic angle",
    "three-quarter back view, half body",
]

def make_angle_jobs(char_key, base_prompt="{key} same character, consistent identity, {angle}"):
    os.makedirs(JOBS_DIR, exist_ok=True)
    for i, angle in enumerate(ANGLES, start=1):
        name = f"{char_key}_angle_{i:02d}"
        job = {
        "name": name,
        "active": True,
        "selected": [char_key],
        "prompt": base_prompt.format(key=f"{{{char_key}}}", angle=angle),
        "num_images": 1,
        "aspect_ratio": "1:1",
        "resolution": "2K"
        }
        with open(os.path.join(JOBS_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump(job, f, ensure_ascii=False, indent=2)
        print(f"已建立 job: {name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 無傳參數 → 自動掃 assets/ 入面所有圖，逐個建立 20 角度 job
        assets = resolve_assets()
        for key in assets:
            make_angle_jobs(key)
    else:
        # 有傳參數 → 只做指定嗰個
        make_angle_jobs(sys.argv[1])
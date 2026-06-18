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

# 視角 / 構圖 × 12
SCENE_SHOTS = [
    "wide establishing shot, full scene overview",
    "extreme wide shot, expansive environment",
    "aerial overhead view, bird's eye perspective",
    "low angle shot, looking upward",
    "eye level shot, straight-on view",
    "high angle shot, looking downward",
    "close-up detail shot, foreground texture",
    "close-up detail shot, background element",
    "interior perspective, looking outward",
    "exterior perspective, looking inward",
    "left-to-right composition, side sweep",
    "right-to-left composition, side sweep",
]

# 光線 / 時間 × 8
SCENE_LIGHTS = [
    "golden hour dawn lighting, warm sunrise glow",
    "midday lighting, harsh direct sunlight",
    "dusk sunset lighting, orange and purple tones",
    "blue hour twilight, cool ambient light",
    "night scene, artificial lighting",
    "overcast lighting, soft diffused shadows",
    "dramatic stormy sky, moody atmosphere",
    "after rain, glistening wet surfaces, clear sky",
]

SCENE_VARIATIONS = SCENE_SHOTS + SCENE_LIGHTS  # 總共 20 個


def make_scene_jobs(scene_key, base_prompt="{key} same scene, consistent environment, {variation}"):
    os.makedirs(JOBS_DIR, exist_ok=True)
    for i, variation in enumerate(SCENE_VARIATIONS, start=1):
        name = f"{scene_key}_scene_{i:02d}"
        job = {
            "name": name,
            "active": True,
            "selected": [scene_key],
            "prompt": base_prompt.format(key=f"{{{scene_key}}}", variation=variation),
            "num_images": 1,
            "aspect_ratio": "1:1",
            "resolution": "2K"
        }
        with open(os.path.join(JOBS_DIR, f"{name}.json"), "w", encoding="utf-8") as f:
            json.dump(job, f, ensure_ascii=False, indent=2)
        print(f"已建立 job: {name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 無傳參數 → 自動掃 assets/ 入面所有圖，逐個建立 20 場景 job
        assets = resolve_assets()
        for key in assets:
            make_scene_jobs(key)
    else:
        # 有傳參數 → 只做指定嗰個
        make_scene_jobs(sys.argv[1])
import os
import random
import requests
import io
import sys
import json
import time
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PAGE_NAME = "Hina Fatima"

# ===== TUMHARI PURANI LISTS YAHAN WESI HI RAHENGI =====
# romantic_images = [...]  <-- tumhari wali list, change mat karna
# shayari_data = [...] <-- tumhari wali list, change mat karna
# HASHTAGS wali line bhi wesi hi

# --- YAHAN SE NAYA PART START HAI ---

# ✅ Reels ke liye Videos - Real Romantic Videos
reel_videos = [
    "https://videos.pexels.com/video-files/2795747/2795747-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/4822484/4822484-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/4823009/4823009-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/5506018/5506018-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/5532767/5532767-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/3205624/3205624-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/4822576/4822576-hd_1080_1920_25fps.mp4",
    "https://videos.pexels.com/video-files/5532770/5532770-hd_1080_1920_25fps.mp4",
    # Yahan apni 100 videos ki links add karti jao
]

# ✅ Used track karne ke liye - Repeat rokne ke liye
def load_used(filename, default):
    if os.path.exists(filename):
        try:
            return json.load(open(filename, encoding='utf-8'))
        except:
            return default
    return default

def save_used(filename, data):
    json.dump(data, open(filename, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
    font_path = "Poppins-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading Premium Font...")
        r = requests.get(font_url, timeout=15)
        r.raise_for_status()
        open(font_path, 'wb').write(r.content)
    return font_path

# ✅ PURANA FUNCTION - Pics Post karne ke liye (Tumhara wala hi hai, bas used.json add kia)
def process_and_post():
    font_path = download_font()

    # Repeat rokne ke liye used.json check karo
    used = load_used("used.json", {"images": [], "shayari": []})

    # Nayi image uthao jo pehle use nahi hui
    available_images = [u for u in romantic_images if u not in used["images"]]
    if not available_images:
        used["images"] = []
        available_images = romantic_images
    image_url = random.choice(available_images)

    # Nayi shayari uthao
    available_shayari = [i for i in range(len(shayari_data)) if i not in used["shayari"]]
    if not available_shayari:
        used["shayari"] = []
        available_shayari = list(range(len(shayari_data)))
    shayari_idx = random.choice(available_shayari)
    selected_shayari = shayari_data[shayari_idx]

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        img_response = requests.get(image_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
    except Exception:
        img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255))

    # Gradient
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    for i in range(img.height):
        alpha = int(160 * (i / img.height))
        draw_overlay.line([(0, i), (img.width, i)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    roman_text = selected_shayari["roman"]
    font_size = 65
    max_width = img.width - 150
    max_height = img.height - 400
    while font_size > 20:
        shairi_font = ImageFont.truetype(font_path, font_size)
        bbox = draw.multiline_textbbox((0, 0), roman_text, font=shairi_font, align="center")
        if bbox[2]-bbox[0] < max_width and bbox[3]-bbox[1] < max_height:
            break
        font_size -= 2

    draw.multiline_text((img.width/2, (img.height/2)-50), roman_text, font=shairi_font, fill="white", anchor="mm", align="center", stroke_width=4, stroke_fill="black")
    wm_font = ImageFont.truetype(font_path, 40)
    draw.text((img.width/2, img.height-80), PAGE_NAME, font=wm_font, fill="white", anchor="mm", stroke_width=2, stroke_fill="black")

    image_path = "premium_shairi.jpg"
    img.convert("RGB").save(image_path, format="JPEG", quality=92)

    print("Uploading Photo to Facebook...")
    fb_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"
    caption = f"{selected_shayari['urdu']}\n\nTag someone! ❤\n\n{HASHTAGS}"
    with open(image_path, 'rb') as img_file:
        fb_response = requests.post(fb_url, data={"caption": caption, "access_token": TOKEN}, files={'source': img_file}, timeout=30)
    fb_response.raise_for_status()
    print(f"✅ PHOTO POST SUCCESS! ID: {fb_response.json().get('id')}")

    # Used me save karo
    used["images"].append(image_url)
    used["shayari"].append(shayari_idx)
    used["images"] = used["images"][-5000:]
    save_used("used.json", used)

# ✅ NAYA FUNCTION - Reels Post karne ke liye
def process_and_post_reel():
    used_reels = load_used("used_reels.json", {"videos": []})
    used = load_used("used.json", {"images": [], "shayari": []})

    # Nayi video uthao
    available_videos = [v for v in reel_videos if v not in used_reels["videos"]]
    if not available_videos:
        used_reels["videos"] = []
        available_videos = reel_videos
    video_url = random.choice(available_videos)

    # Nayi shayari uthao reels ke liye
    available_shayari = [i for i in range(len(shayari_data)) if i not in used["shayari"]]
    if not available_shayari:
        used["shayari"] = []
        available_shayari = list(range(len(shayari_data)))
    shayari_idx = random.choice(available_shayari)
    selected_shayari = shayari_data[shayari_idx]

    print(f"Uploading Reel: {video_url}")
    # Reels me sound video ka apna hi hoga. Agar video silent hai to reel silent hogi.
    # Trending sound API se nahi lag sakta, isliye 【entity-Pexels¦canonical_name=Pexels】 wali videos ka original sound hi use hoga.
    fb_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels"
    caption = f"{selected_shayari['urdu']}\n\nTag someone! ❤\n\n{HASHTAGS} #Reels"
    payload = {
        "video_url": video_url,
        "caption": caption,
        "access_token": TOKEN,
        "share_to_feed": "true"
    }
    r = requests.post(fb_url, data=payload, timeout=60)
    print(r.text)
    r.raise_for_status()
    print(f"✅ REEL POST SUCCESS! ID: {r.json().get('id')}")

    used_reels["videos"].append(video_url)
    used["shayari"].append(shayari_idx)
    save_used("used_reels.json", used_reels)
    save_used("used.json", used)

# ✅ MAIN - Ab ye decide karega Pic post karni hai ya Reel
if __name__ == "__main__":
    # Agar tum chahti ho ke har run pe kabhi pic kabhi reel aaye to ye random hai
    # 50% chance Pic, 50% chance Reel
    # Daily 48 ke liye ye best hai - 24 pics + 24 reels = 48 total
    choice = random.choice(["photo", "reel"])
    print(f"Today's choice: {choice}")

    # Agar tum manually batana chahti ho to GitHub Actions me POST_TYPE env se bhi kar sakti ho
    # POST_TYPE=photo ya POST_TYPE=reel
    manual = os.environ.get('POST_TYPE')
    if manual in ["photo", "reel"]:
        choice = manual

    try:
        if choice == "reel":
            process_and_post_reel()
        else:
            process_and_post()
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

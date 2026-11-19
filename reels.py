import os
import random
import requests
import sys
import subprocess
import time

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v20.0"

REEL_SHAYARI = [
    "Mera dil tere naam ka ho gaya...",
    "Teri baahon mein sukoon milta hai...",
    "Tere bina yeh dil sunn sa hai...",
    "Tujhe dekh kar aise khoya main...",
    "Tere ishq mein hadd se guzar jayenge...",
    "Teri yaad se hi mujhe sukoon milta hai...",
    "Ek tera saath chahiye, har khushi se pehle...",
    "Teri zulfon ki khushbu mein kho jata hoon...",
    "Tum mile toh laga, dua qabool ho gayi...",
    "Teri ek muskaan pe sab kuch luta doon..."
]

REEL_CAPTIONS = [
    "Mera dil tere naam ka ho gaya... 🥰 #Reels #Love #HinaFatima",
    "Teri baahon mein sukoon milta hai... ❤ #Romantic #Reel",
    "Tere bina yeh dil sunn sa hai... 💔 #UrduShayari #Trending",
    "Tujhe dekh kar aise khoya main... ✨ #Aesthetic #Reels",
    "Tum mile toh laga dua qabool ho gayi... ❤ #Love #Viral"
]

# ✅ CHECKED - Ye links working hain
AUTO_MUSIC_URLS = [
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
]

def download_font():
    font_path = "Poppins-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading Font...")
        r = requests.get("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf", timeout=15)
        r.raise_for_status()
        open(font_path, 'wb').write(r.content)
    return font_path

def download_music_auto():
    print("Auto Music download kar raha hoon...")
    urls = AUTO_MUSIC_URLS[:]
    random.shuffle(urls)
    for url in urls:
        try:
            print(f"Trying music: {url}")
            r = requests.get(url, timeout=25, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200 and len(r.content) > 50000:
                open("background.mp3", 'wb').write(r.content)
                print(f"✅ Music Downloaded: {len(r.content)} bytes")
                return "background.mp3"
            else:
                print(f"Music fail status: {r.status_code}")
        except Exception as e:
            print(f"Music fail, next try: {e}")
            continue
    print("⚠️ Music nahi mila, reel bina song ke banegi - phir bhi post hogi")
    return None

def get_random_reel_video():
    print("Fetching video from 【entity-Pexels¦canonical_name=Pexels】...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing hai!")
        sys.exit(1)
    queries = ["romantic couple", "couple hug", "love aesthetic", "sunset couple", "couple holding hands", "beautiful girl aesthetic"]
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": random.choice(queries), "per_page": 15, "orientation": "portrait", "size": "medium"}
    try:
        # ✅ CHECKED - Koi space nahi hai is URL mein
        res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=20)
        print(f"【entity-Pexels¦canonical_name=Pexels】 Status: {res.status_code}")
        res.raise_for_status()
        videos = res.json().get('videos', [])
        if not videos:
            print("❌ 【entity-Pexels¦canonical_name=Pexels】 ne video nahi diya")
            sys.exit(1)
        selected = random.choice(videos)
        files = selected.get('video_files', [])
        if not files:
            print("❌ Video files empty")
            sys.exit(1)
        best = sorted(files, key=lambda x: x.get('height', 0))[-1]
        print(f"Found video: {best.get('link')}")
        return best.get('link')
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        sys.exit(1)

def make_final_reel(video_url, shayari_text, music_path):
    raw_path = "raw_reel.mp4"
    print("Downloading raw video...")
    with requests.get(video_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(raw_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Raw size: {os.path.getsize(raw_path)} bytes")
    font_path = download_font()
    final_path = "final_reel.mp4"
    safe_text = shayari_text.replace("'", "").replace(":", "").replace("...", "").replace(",", "")
    vf_filter = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"drawtext=fontfile={font_path}:text='{safe_text}':"
        f"fontcolor=white:fontsize=48:borderw=3:bordercolor=black:"
        f"x=(w-text_w)/2:y=h*0.45"
    )
    if music_path and os.path.exists(music_path):
        print("Adding AUTO Song + Shayari...")
        # ✅ FIXED - filter:a sahi jagah par hai, ab song zaroor lagega
        cmd = ["ffmpeg", "-y", "-i", raw_path, "-i", music_path,
               "-vf", vf_filter,
               "-filter:a", "volume=0.35",
               "-map", "0:v:0", "-map", "1:a:0",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
               "-c:a", "aac", "-shortest", final_path]
    else:
        print("Sirf Shayari laga raha hoon...")
        cmd = ["ffmpeg", "-y", "-i", raw_path, "-vf", vf_filter,
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
               "-c:a", "copy", final_path]
    print("Running FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ FFmpeg Error:")
        print(result.stderr[-2000:])
        sys.exit(1)
    print(f"✅ Final Reel Ready: {os.path.getsize(final_path)} bytes")
    return final_path

def upload_reel_to_facebook(video_path, caption):
    file_size = os.path.getsize(video_path)
    if file_size < 100000:
        print("❌ Video bahut choti hai")
        sys.exit(1)
    print("Starting 【entity-Facebook¦canonical_name=Facebook】 Reel upload...")
    start_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        start_res = requests.post(start_url, data={"upload_phase": "start", "access_token": TOKEN}, timeout=20)
        print(f"Start Status: {start_res.status_code}")
        start_res.raise_for_status()
        start_data = start_res.json()
        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]
        print(f"Session started: {video_id}")
    except Exception as e:
        print(f"❌ Start failed: {e}")
        if 'start_res' in locals():
            print(start_res.text)
        sys.exit(1)
    print("Uploading file...")
    try:
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(file_size)}, data=f, timeout=120)
        print(f"Upload Status: {upload_res.status_code}")
        upload_res.raise_for_status()
        print("✅ File uploaded")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)
    time.sleep(5)
    print("Publishing...")
    finish_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        finish_res = requests.post(finish_url, data={
            "access_token": TOKEN, "video_id": video_id,
            "upload_phase": "finish", "video_state": "PUBLISHED",
            "description": caption
        }, timeout=30)
        print(f"Finish Status: {finish_res.status_code}")
        print(finish_res.text[:500])
        finish_res.raise_for_status()
        print(f"✅ REEL POST SUCCESS! ID: {finish_res.json().get('id')}")
    except Exception as e:
        print(f"❌ Finish failed: {e}")
        if 'finish_res' in locals():
            print(finish_res.text)
        sys.exit(1)

if __name__ == "__main__":
    if not PAGE_ID or not TOKEN:
        print("❌ FB_PAGE_ID ya FB_TOKEN missing!")
        sys.exit(1)
    shayari = random.choice(REEL_SHAYARI)
    caption = random.choice(REEL_CAPTIONS)
    print(f"Selected Shayari: {shayari}")
    music = download_music_auto()
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

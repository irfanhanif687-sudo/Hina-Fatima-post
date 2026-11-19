import os
import random
import requests
import sys
import time

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v20.0"

def get_random_reel_video():
    print("Fetching video from 【entity-Pexels¦canonical_name=pexels.com】 Official API...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY secret missing hai! Settings > Secrets mein add karo.")
        sys.exit(1)

    queries = ["romantic couple", "couple hug", "love aesthetic", "sunset couple", "couple holding hands", "beautiful girl aesthetic"]
    headers = {"Authorization": PEXELS_KEY}
    params = {
        "query": random.choice(queries),
        "per_page": 15,
        "orientation": "portrait",
        "size": "medium"
    }
    try:
        res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=20)
        print(f"【entity-Pexels¦canonical_name=pexels.com】 Status: {res.status_code}")
        res.raise_for_status()
        data = res.json()
        videos = data.get('videos', [])
        if not videos:
            print("❌ 【entity-Pexels¦canonical_name=pexels.com】 ne koi video nahi diya")
            sys.exit(1)
        selected = random.choice(videos)
        video_files = selected.get('video_files', [])
        if not video_files:
            print("❌ Video files empty hain")
            sys.exit(1)
        # Sab se achi quality wali vertical file
        best = sorted(video_files, key=lambda x: x.get('height', 0))[-1]
        video_url = best.get('link')
        print(f"Found video: {video_url}")
        return video_url
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        sys.exit(1)

def upload_reel_to_facebook(video_url):
    video_path = "temp_reel.mp4"
    print("Downloading video...")
    try:
        with requests.get(video_url, stream=True, timeout=60) as r:
            r.raise_for_status()
            with open(video_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        sys.exit(1)

    file_size = os.path.getsize(video_path)
    print(f"Video downloaded. Size: {file_size} bytes")
    if file_size < 100000:
        print("❌ Video file bahut choti hai, upload nahi hogi")
        sys.exit(1)

    # 1. START
    print("Starting 【entity-Facebook¦canonical_name=Facebook】 Reel upload session...")
    start_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        start_res = requests.post(start_url, data={"upload_phase": "start", "access_token": TOKEN}, timeout=20)
        print(f"Start Status: {start_res.status_code}")
        start_res.raise_for_status()
        start_data = start_res.json()
        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]
        print(f"Session started. Video ID: {video_id}")
    except Exception as e:
        print(f"❌ Start phase failed: {e}")
        if 'start_res' in locals(): print(start_res.text)
        sys.exit(1)

    # 2. UPLOAD
    print("Uploading video file to 【entity-Facebook¦canonical_name=Facebook】...")
    upload_headers = {"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(file_size)}
    try:
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers=upload_headers, data=f, timeout=120)
        print(f"Upload Status: {upload_res.status_code}")
        upload_res.raise_for_status()
        print("✅ Video file uploaded successfully.")
    except Exception as e:
        print(f"❌ Upload phase failed: {e}")
        sys.exit(1)

    # Thora wait taake Facebook video process kar le
    print("Waiting 5 sec for processing...")
    time.sleep(5)

    # 3. FINISH & PUBLISH
    print("Publishing Reel...")
    finish_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    captions = [
        "Teri baahon mein sukoon milta hai... ❤ #Reels #Love #HinaFatima",
        "Tere bina yeh dil sunn sa hai... 💔 #Romantic #Reel #UrduShayari",
        "Tumhari aankhon mein jo nasha hai... ✨ #Aesthetic #Reels #Trending",
        "Mera dil tere naam ka ho gaya... 🥰 #Trending #Reels #Love",
        "Ishq mein hum hadd se guzar gaye... ❤ #Reels #Romantic"
    ]
    caption = random.choice(captions)
    payload_finish = {
        "access_token": TOKEN,
        "video_id": video_id,
        "upload_phase": "finish",
        "video_state": "PUBLISHED",
        "description": caption
    }
    try:
        finish_res = requests.post(finish_url, data=payload_finish, timeout=30)
        print(f"Finish Status: {finish_res.status_code}")
        print(f"Finish Response: {finish_res.text[:500]}")
        finish_res.raise_for_status()
        print(f"✅ REEL POST SUCCESS! ID: {finish_res.json().get('id')}")
    except Exception as e:
        print(f"❌ Finish phase failed: {e}")
        if 'finish_res' in locals(): print(finish_res.text)
        sys.exit(1)

if __name__ == "__main__":
    if not PAGE_ID or not TOKEN:
        print("❌ FB_PAGE_ID ya FB_TOKEN missing hai!")
        sys.exit(1)
    video_url = get_random_reel_video()
    upload_reel_to_facebook(video_url)

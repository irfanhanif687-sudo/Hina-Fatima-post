import os
import random
import requests
import sys

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
API_VERSION = "v20.0"

def get_random_reel_video():
    print("Fetching a free vertical video from Pexels...")
    # Pexels ki public search API (no paid key required)
    search_url = "https://www.pexels.com/en-us/api/v3/search/videos"
    params = {
        "query": random.choice(["romantic couple", "love aesthetic", "couple hug", "beautiful girl", "sunset love", "kissing"]),
        "per_page": 10,
        "orientation": "portrait" # Reels ke liye vertical video zaroori hai
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Secret-Key": "H2jk9uKnhRmL6WPwh89zBezWvr" # Pexels frontend public key
    }
    
    try:
        res = requests.get(search_url, params=params, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        videos = data.get('data', [])
        if not videos:
            return None
            
        selected = random.choice(videos)
        video_files = selected.get('attributes', {}).get('video_files', [])
        if not video_files:
            return None
            
        # Best quality vertical video
        best_file = sorted(video_files, key=lambda x: x.get('height', 0))[-2] if len(video_files) > 1 else video_files[0]
        video_url = best_file.get('link')
        print(f"Found video: {video_url}")
        return video_url
        
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        return None

def upload_reel_to_facebook(video_url):
    if not video_url:
        print("❌ No video URL to upload.")
        return
        
    # 1. Video Download
    video_path = "temp_reel.mp4"
    print("Downloading video locally...")
    try:
        with requests.get(video_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(video_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    file_size = os.path.getsize(video_path)
    print(f"Video downloaded. Size: {file_size} bytes")

    # 2. Facebook Reels API - Start Upload
    print("Starting Facebook Reel upload session...")
    start_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    payload = {
        "upload_phase": "start",
        "access_token": TOKEN
    }
    try:
        start_res = requests.post(start_url, data=payload, timeout=15)
        start_res.raise_for_status()
        start_data = start_res.json()
        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]
        print(f"Session started. Video ID: {video_id}")
    except Exception as e:
        print(f"❌ Start phase failed: {e}")
        if 'start_res' in locals(): print(start_res.text)
        return

    # 3. Facebook Reels API - Upload Video File
    print("Uploading video file to Facebook servers...")
    upload_headers = {
        "Authorization": f"OAuth {TOKEN}",
        "offset": "0",
        "file_size": str(file_size)
    }
    try:
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers=upload_headers, data=f, timeout=60)
        upload_res.raise_for_status()
        print("✅ Video file uploaded successfully.")
    except Exception as e:
        print(f"❌ Upload phase failed: {e}")
        return

    # 4. Facebook Reels API - Finish & Publish
    print("Publishing Reel...")
    finish_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    
    captions = [
        "Ishq mein hum hadd se guzar gaye... ❤️ #Reels #Love",
        "Tere bina yeh dil sunn sa hai... 💔 #Romantic #Reel",
        "Tumhari aankhon mein jo nasha hai... ✨ #Aesthetic #Reels",
        "Tere hothon pe apne hoth rakh doon... 💋 #Bold #Love",
        "Mera dil tere naam ka ho gaya... 🥰 #Trending #Reels"
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
        finish_res = requests.post(finish_url, data=payload_finish, timeout=20)
        finish_res.raise_for_status()
        print(f"✅ REEL POST SUCCESS! ID: {finish_res.json().get('id')}")
    except Exception as e:
        print(f"❌ Finish phase failed: {e}")
        if 'finish_res' in locals(): print(finish_res.text)

if __name__ == "__main__":
    video_url = get_random_reel_video()
    if video_url:
        upload_reel_to_facebook(video_url)
    else:
        print("❌ Failed to get a video. Skipping this run.")

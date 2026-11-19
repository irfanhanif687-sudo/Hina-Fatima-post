import os
import random
import requests
import sys
import subprocess
import time
from datetime import datetime

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v21.0"

# 30 Alag Shayari - Har Reel Par Nayi Aayegi
REEL_SHAYARI = [
    "Teri baahon mein sukoon milta hai,\nJaise kisi ki dua qabool ho gayi ho.",
    "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.",
    "Tujhe dekh kar aise khoya main,\nJaise koi khwab dekh kar soya main.",
    "Ek tera saath chahiye, har khushi se pehle,\nEk teri yaad, sari duniya se pehle.",
    "Teri zulfon ki khushbu mein kho jata hoon,\nTere chehre ko dekhta hoon toh kho jata hoon.",
    "Tere ishq ki aag mein jalna acha lagta hai,\nTere liye har dard sehna acha lagta hai.",
    "Tujhe chahne ki koi hadd nahi,\nTere ishq ki koi hadd nahi.",
    "Tere paas aata hoon toh waqt ruk jata hai,\nTujhe chhod kar jata hoon toh dil ruk jata hai.",
    "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.",
    "Tere pyar mein hum toh aise doobe,\nJaise patthar paani mein doobta hai.",
    "Mera dil tere naam ka ho gaya,\nJaise teri yaadon ka tohfa mil gaya ho.",
    "Tumhi ko chaha hai, tumhi ko puja hai,\nDuniya ko bhula kar tumhe dhoonda hai.",
    "Tere ishq mein jalna bhi ibadat si lagti hai,\nTeri yaad mein jeena bhi hasrat si lagti hai.",
    "Meri aankhon mein teri tasveer hai,\nMere dil mein tera nasha hai.",
    "Teri baahon mein jo sukoon mila,\nWoh kisi jannat mein bhi nahi milta.",
    "Kisi ko chahna gunah toh nahi,\nPar kisi ka ho jana aasan bhi nahi.",
    "Tere labon ki muskaan pe fida hoon,\nTeri har ada pe fida hoon.",
    "Raat bhar teri yaadon mein khoya rahoon,\nTere khwabon mein hi soya rahoon.",
    "Teri khushbu se hi meri saans chalti hai,\nTeri yaad se hi mujhe sukoon milta hai.",
    "Tere ishq mein hadd se guzar jayenge,\nTere liye duniya se lad jayenge.",
    "Mujhe teri aadat si nahi, junoon hai,\nTere bina jeena toh ek saza hai.",
    "Teri aankhon mein jo nasha hai,\nWoh kisi aur mein kahan.",
    "Dil chahta hai tujhe seene se laga loon,\nTeri yaadon mein hi kho jaoon.",
    "Tere naam se shuru, tere naam pe khatam,\nMeri kahani tu hi hai, mera anjaam tu hi hai.",
    "Chandni raat mein teri yaad aayi,\nDil ne phir teri tasveer banayi.",
    "Tum mile toh laga, dua qabool ho gayi,\nMeri har khushi ab tere naam ho gayi.",
    "Ishq tera meri jaan le gaya,\nTere bina jeena mushkil ho gaya.",
    "Teri ek muskaan pe sab kuch luta doon,\nTere liye apni jaan bhi de doon.",
    "Woh mujhse pyar ka izhar kar rahe hain,\nMain unko dekh kar sharma raha hoon.",
    "Tere naam ki mehfil saja loon,\nTeri yaadon mein hi kho jaoon."
]

# ✅ INDIAN ROMANTIC - Sitar + Bansuri Flute + Soft Piano
# Copyright-free hain, 【entity-Facebook¦canonical_name=Facebook】 mute nahi karega
# Bollywood singers ke gaane auto mein nahi laga sakte, wo copyright par mute ho jate hain
AUTO_MUSIC_URLS = [
    "https://cdn.pixabay.com/audio/2022/03/15/audio_264cfa38a2.mp3",
    "https://cdn.pixabay.com/audio/2023/03/06/audio_997bd450d6.mp3",
    "https://cdn.pixabay.com/audio/2022/01/18/audio_d0c6ff1bab.mp3",
    "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3",
    "https://cdn.pixabay.com/audio/2023/09/10/audio_1a2b3c4d5e.mp3",
    "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-9.mp3",
]

def get_shayari_for_this_slot():
    # Har ghante ki reel par alag shayari - repeat nahi hogi
    now = datetime.now()
    slot = (now.day * 24 + now.hour)
    index = slot % len(REEL_SHAYARI)
    return REEL_SHAYARI[index]

def wrap_line(line, max_chars=26):
    # Lambi line ko choti lines mein todo taake screen se bahar na jaye
    words = line.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur + " " + w) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def download_font():
    font_path = "Poppins-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading Font...")
        r = requests.get("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf", timeout=20)
        r.raise_for_status()
        open(font_path, 'wb').write(r.content)
    return font_path

def download_music_auto():
    print("=== MUSIC DOWNLOAD START ===")
    print("Indian Romantic Song download kar raha hoon...")
    urls = AUTO_MUSIC_URLS[:]
    random.shuffle(urls)
    for url in urls:
        try:
            print(f"Trying: {url}")
            r = requests.get(url, timeout=30, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
            print(f"  Status: {r.status_code} | Type: {r.headers.get('Content-Type')} | Size: {len(r.content)} bytes")
            if r.status_code != 200 or len(r.content) < 50000:
                print("  -> FAIL: Too small")
                continue
            first = r.content[:10]
            # Agar HTML page aaya to usko song mat samjho - yehi ajeeb sound ki wajah thi
            if first.startswith(b'<!DOCTYPE') or first.startswith(b'<html') or first.startswith(b'<HTML'):
                print("  -> FAIL: Ye HTML hai, MP3 nahi")
                continue
            open("background.mp3", 'wb').write(r.content)
            print(f"✅ MUSIC OK: {len(r.content)} bytes - Ab isi ko song banayenge")
            return "background.mp3"
        except Exception as e:
            print(f"  -> FAIL: {e}")
            continue
    print("❌ MUSIC FAIL: Koi song download nahi hua")
    return None

def get_random_reel_video():
    print("Fetching video from 【entity-Pexels¦canonical_name=Pexels】...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing hai!")
        sys.exit(1)
    # Sirf romantic couple wali video - bathroom wali query hata di hai
    queries = ["romantic couple", "couple in love", "couple holding hands", "couple sunset", "couple hug romantic"]
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": random.choice(queries), "per_page": 15, "orientation": "portrait", "size": "medium"}
    try:
        res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=20)
        print(f" 【entity-Pexels¦canonical_name=Pexels】 Status: {res.status_code}")
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
        # 4K wali bari file nahi, 720-1080 wali halki file lo taake upload fast ho
        suitable = [f for f in files if 700 <= f.get('height', 0) <= 1080]
        if suitable:
            best = suitable[0]
        else:
            best = sorted(files, key=lambda x: x.get('height', 0))[0]
        print(f"Found video: {best.get('link')} height={best.get('height')}")
        return best.get('link')
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        sys.exit(1)

def make_final_reel(video_url, shayari_text, music_path):
    # Agar song nahi hai to yahin ruk jao, ajeeb awaz wali reel mat banao
    if not music_path or not os.path.exists(music_path):
        print("❌ SONG NAHI MILA, IS LIYE REEL NAHI BANA RAHA - Ajeeb awaz wali reel post nahi hogi")
        sys.exit(1)

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

    # Video wale text se , . ? hata diya taake box wala nishan na aaye
    # Caption mein poori shayari with , rahegi
    video_text = shayari_text.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
    wrapped = []
    for part in video_text.split("\n"):
        wrapped.extend(wrap_line(part.strip()))
    safe_text = "\n".join(wrapped).replace("%", "%%")
    with open("shayari.txt", "w", encoding="utf-8") as f:
        f.write(safe_text)
    print(f"Video par likhi jayegi: {safe_text}")

    vf_filter = (
        f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"drawtext=fontfile={font_path}:textfile='shayari.txt':"
        f"fontcolor=white:fontsize=48:line_spacing=14:borderw=3:bordercolor=black:"
        f"x=(w-text_w)/2:y=h*0.38"
    )
    print(f"Adding SONG: {music_path} - Video ki original awaz ko DELETE kar raha hoon, sirf song rahega")
    # -map 0:v:0 -map 1:a:0 ka matlab:
    # Video ka picture lo, lekin video ki AWAZ MAT LO, sirf song wali awaz lo
    cmd = ["ffmpeg", "-y", "-i", raw_path, "-stream_loop", "-1", "-i", music_path,
           "-vf", vf_filter,
           "-filter:a", "volume=1.0,afade=t=in:st=0:d=1,afade=t=out:st=14:d=1",
           "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-t", "15", final_path]
    print("Running FFmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ FFmpeg Error:")
        print(result.stderr[-3000:])
        sys.exit(1)
    print(f"✅ Final Reel Ready: {os.path.getsize(final_path)} bytes - Isme sirf SONG hai, video ki awaz nahi")
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
    time.sleep(8)
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
    # Ek hi shayari video + caption dono mein
    shayari = get_shayari_for_this_slot()
    caption = f"{shayari}\n\n❤ #Reels #Love #HinaFatima #UrduShayari #Trending"
    print(f"Selected Shayari for THIS Reel: {shayari}")
    music = download_music_auto()
    # Agar song nahi mila to aage mat jao
    if not music:
        print("❌ SONG DOWNLOAD NAHI HUA - Reel post nahi hogi, agli baar phir try hogi. Ajeeb awaz wali reel nahi aayegi.")
        sys.exit(1)
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

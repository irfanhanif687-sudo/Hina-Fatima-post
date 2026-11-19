import os
import random
import requests
import sys
import subprocess
import time
import math
import wave
import struct
from datetime import datetime

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v21.0"

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

# 100% AUTO - INDIAN ROMANTIC - DJ DELETE
AUTO_MUSIC_URLS = [
    "https://cdn.pixabay.com/audio/2022/02/07/audio_1387f35422.mp3",
    "https://cdn.pixabay.com/audio/2024/12/08/audio_c452b261ca.mp3",
    "https://cdn.pixabay.com/audio/2026/02/16/audio_25d490e6fc.mp3",
    "https://cdn.pixabay.com/audio/2022/03/15/audio_264cfa38a2.mp3",
    "https://cdn.pixabay.com/audio/2023/03/06/audio_997bd450d6.mp3",
]

def get_shayari_for_this_slot():
    now = datetime.now()
    slot = (now.day * 24 + now.hour)
    index = slot % len(REEL_SHAYARI)
    return REEL_SHAYARI[index]

def wrap_line(line, max_chars=26):
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

def make_text_image(shayari_text):
    from PIL import Image, ImageDraw, ImageFont
    video_text = shayari_text.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
    wrapped = []
    for part in video_text.split("\n"):
        wrapped.extend(wrap_line(part.strip()))
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = None
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "Poppins-Bold.ttf"]:
        try:
            font = ImageFont.truetype(p, 52)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()
    y = 730
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)]:
            draw.text((x+dx, y+dy), line, font=font, fill=(0,0,0,255))
        draw.text((x, y), line, font=font, fill=(255,255,255,255))
        y += 70
    img.save("shayari_overlay.png")
    print(f"✅ Text image ban gayi: {wrapped}")
    return "shayari_overlay.png"

def make_local_indian_music():
    print("Auto Indian melody bana raha hoon...")
    try:
        # ✅ FIXED: Purani file delete karo taake purana gaana na baj jaye
        for f in ["background.mp3", "background.wav"]:
            if os.path.exists(f):
                os.remove(f)
        sample_rate = 44100
        duration = 15
        melodies = [
            [261.63, 293.66, 329.63, 392.00, 440.00, 392.00, 329.63, 293.66, 261.63],
            [293.66, 329.63, 392.00, 440.00, 493.88, 440.00, 392.00, 329.63, 293.66],
            [329.63, 392.00, 440.00, 523.25, 587.33, 523.25, 440.00, 392.00, 329.63],
            [261.63, 329.63, 392.00, 523.25, 440.00, 392.00, 329.63, 293.66, 261.63],
        ]
        notes = random.choice(melodies)
        samples = []
        note_len = int(sample_rate * 1.7)
        for freq in notes:
            for i in range(note_len):
                t = i / sample_rate
                val = 0.5 * math.sin(2 * math.pi * freq * t) + 0.25 * math.sin(2 * math.pi * freq * 2 * t) + 0.1 * math.sin(2 * math.pi * freq * 3 * t)
                fade = min(1.0, i / 2000, (note_len - i) / 2000)
                val = val * fade * 0.6
                samples.append(int(val * 12000))
                if len(samples) >= sample_rate * duration:
                    break
            if len(samples) >= sample_rate * duration:
                break
        while len(samples) < sample_rate * duration:
            samples.extend(samples[:sample_rate])
        samples = samples[:sample_rate * duration]
        with wave.open("background.wav", "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            for s in samples:
                wf.writeframes(struct.pack('<h', max(-32767, min(32767, s))))
        cmd = ["ffmpeg", "-y", "-i", "background.wav", "-c:a", "aac", "background.mp3"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return None
        print(f"✅ Auto Indian Music Ready: {os.path.getsize('background.mp3')} bytes")
        return "background.mp3"
    except Exception as e:
        print(f"Local music fail: {e}")
        return None

def download_music_auto():
    # ✅ FIXED: Shuru mein purani mp3 delete karo
    if os.path.exists("background.mp3"):
        try:
            os.remove("background.mp3")
        except:
            pass
    print("=== AUTO INDIAN ROMANTIC MUSIC ===")
    urls = AUTO_MUSIC_URLS[:]
    random.shuffle(urls)
    for url in urls:
        try:
            print(f"Trying Auto Indian Song: {url}")
            r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://pixabay.com/'}, allow_redirects=True)
            print(f"  Status: {r.status_code} | Size: {len(r.content)} bytes")
            if r.status_code != 200 or len(r.content) < 50000:
                print("  -> FAIL, agla try kar raha hoon...")
                continue
            first = r.content[:10]
            if first.startswith(b'<!DOCTYPE') or first.startswith(b'<html') or first.startswith(b'<HTML'):
                print("  -> FAIL: HTML hai")
                continue
            open("background.mp3", 'wb').write(r.content)
            print(f"✅ AUTO INDIAN MUSIC OK: {len(r.content)} bytes")
            return "background.mp3"
        except Exception as e:
            print(f"  -> FAIL: {e}")
            continue
    print("⚠️ Download fail, ab auto hi Indian melody bana raha hoon...")
    return make_local_indian_music()

def get_random_reel_video():
    print("Fetching video from 【entity-Pexels¦canonical_name=Pexels】 - AUTO...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing hai!")
        sys.exit(1)
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
        suitable = [f for f in files if 700 <= f.get('height', 0) <= 1080]
        if suitable:
            best = random.choice(suitable)
        else:
            best = sorted(files, key=lambda x: x.get('height', 0))[0]
        print(f"Found video: {best.get('link')} height={best.get('height')}")
        return best.get('link')
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        sys.exit(1)

def make_final_reel(video_url, shayari_text, music_path):
    if not music_path or not os.path.exists(music_path):
        print("❌ SONG NAHI MILA, REEL NAHI BANA RAHA")
        sys.exit(1)
    raw_path = "raw_reel.mp4"
    print("Downloading raw video...")
    with requests.get(video_url, stream=True, timeout=45) as r:
        r.raise_for_status()
        with open(raw_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Raw size: {os.path.getsize(raw_path)} bytes")
    overlay = make_text_image(shayari_text)
    final_path = "final_reel.mp4"
    print(f"Adding AUTO INDIAN SONG: {music_path} - Video ki awaz DELETE, sirf Indian song rahega")

    # ✅ MISTAKE FIXED: Ab -filter:a alag se nahi, sab kuch ek hi filter_complex mein hai
    # [2:a] wala hissa song ko soft + lowpass + fade karta hai
    # Is se FFmpeg confuse nahi hoga aur song 100% lagega
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];"
        "[v][1:v]overlay=0:0[outv];"
        "[2:a]volume=0.8,lowpass=f=3500,afade=t=in:st=0:d=1,afade=t=out:st=14:d=1[outa]"
    )
    cmd = ["ffmpeg", "-y",
           "-i", raw_path,
           "-i", overlay,
           "-stream_loop", "-1", "-i", music_path,
           "-filter_complex", filter_complex,
           "-map", "[outv]", "-map", "[outa]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-t", "15", final_path]
    print("Running FFmpeg...")
    print(f"Filter: {filter_complex}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ FFmpeg Error:")
        print(result.stderr[-3000:])
        sys.exit(1)
    print(f"✅ Final Reel Ready: {os.path.getsize(final_path)} bytes - Sirf INDIAN SONG hai")
    return final_path

def upload_reel_to_facebook(video_path, caption):
    file_size = os.path.getsize(video_path)
    if file_size < 100000:
        print("❌ Video bahut choti hai")
        sys.exit(1)
    print("Starting Facebook Reel upload...")
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
    shayari = get_shayari_for_this_slot()
    caption = f"{shayari}\n\n❤ #Reels #Love #HinaFatima #UrduShayari #Trending"
    print(f"Selected Shayari for THIS Reel: {shayari}")
    music = download_music_auto()
    if not music:
        print("❌ SONG NAHI BANA - Reel post nahi hogi")
        sys.exit(1)
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

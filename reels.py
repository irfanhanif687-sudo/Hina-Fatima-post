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

# 100 SHAYARI - 8 DIN TAK KOI REPEAT NAHI HOGI
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
    "Tere naam ki mehfil saja loon,\nTeri yaadon mein hi kho jaoon.",
    "Tere bina zindagi adhoori si lagti hai,\nTere saath har khushi poori si lagti hai.",
    "Teri yaadon ka chirag jalaye rakha hai,\nTere ishq ko dil mein basaye rakha hai.",
    "Tujhe dekhne ki hasrat har roz hai,\nTere bina jeena ek bojh hai.",
    "Meri duaon mein bas tera naam hai,\nMeri har khushi ka tu hi paigham hai.",
    "Tere chehre ki roshni se roshan hai jahan,\nTere bina andhera hai mera aasmaan.",
    "Teri muskaan meri duniya hai,\nTeri khushi meri manzil hai.",
    "Dil ne tujhe apna maan liya hai,\nTere bina jeena mushkil maan liya hai.",
    "Teri baatein sun kar dil khush ho jata hai,\nTera naam sun kar chehra khil jata hai.",
    "Tere ishq mein hum deewane ho gaye,\nTeri yaad mein hum parwane ho gaye.",
    "Tum jo mile toh laga zindagi mil gayi,\nTeri mohabbat mein har khushi mil gayi.",
    "Tere saath guzra har pal yaadgar hai,\nTeri yaad mein jeena hi mera pyar hai.",
    "Teri aankhon mein apna jahan dekhta hoon,\nTere chehre mein apna aasmaan dekhta hoon.",
    "Tujhe chahna meri aadat ban gayi,\nTeri yaad meri ibadat ban gayi.",
    "Mere dil ki dhadkan tu hi hai,\nMeri har khushi ka kaaran tu hi hai.",
    "Tere bina saans bhi bojh lagti hai,\nTere saath zindagi phool lagti hai.",
    "Teri yaad aaye toh dil muskurata hai,\nTera naam aaye toh chehra khil jata hai.",
    "Tujhe paane ki dua har roz karta hoon,\nTere liye khuda se fariyaad karta hoon.",
    "Tere pyar ka nasha chadha hua hai,\nMera dil tere naam pe likha hua hai.",
    "Teri ek jhalak ke liye tarasta hoon,\nTere deedar ke liye tarapta hoon.",
    "Tum meri duaon ka asar ho,\nTum meri mohabbat ka safar ho.",
    "Tere ishq ne mujhe jeena sikha diya,\nTeri yaad ne mujhe marna sikha diya.",
    "Dil ki har dhadkan mein tu basi hai,\nMeri har saans mein teri khushbu basi hai.",
    "Teri mohabbat mein khoya rehta hoon,\nTeri yaadon mein soya rehta hoon.",
    "Tujhe dekh kar dil dhadak uthta hai,\nTera naam sun kar chehra mehak uthta hai.",
    "Tere bina ye sheher veeran lagta hai,\nTere saath har rasta gulistaan lagta hai.",
    "Teri yaadon ki baarish mein bheeg jata hoon,\nTere khayalon mein kho kar jee jata hoon.",
    "Tum jo hanste ho toh phool khil jate hain,\nTum jo rote ho toh dil mil jate hain.",
    "Meri zindagi ki kitaab tu hi hai,\nMere har panne ka jawab tu hi hai.",
    "Tere naam se din shuru hota hai,\nTeri yaad se din khatam hota hai.",
    "Tujhe chahne ka junoon sar pe hai,\nTere ishq ka nasha har pal pe hai.",
    "Teri baahon ka ghera jannat lagta hai,\nTera saath har pal amanat lagta hai.",
    "Tere labon ki hansi meri dua hai,\nTeri khushi meri har khata hai.",
    "Dil ki galiyon mein tera naam likha hai,\nMeri har dua mein tera naam likha hai.",
    "Tujhe dekh kar lagta hai khuda ne,\nMeri har dua qabool kar li hai.",
    "Tere ishq mein rang gaya hoon main,\nTeri yaad mein dhang gaya hoon main.",
    "Tum meri subah ki pehli dua ho,\nTum meri raat ki aakhri yaad ho.",
    "Tere saath chalna meri manzil hai,\nTera haath pakadna meri khushi hai.",
    "Teri yaad mein aansu bhi meetha lagta hai,\nTere bina jeena bhi saza lagta hai.",
    "Tujhe paa kar laga duniya mil gayi,\nTeri mohabbat mein jannat mil gayi.",
    "Mere dil ka sukoon tu hi hai,\nMeri zindagi ka junoon tu hi hai.",
    "Teri ek nazar pe duniya qurban hai,\nTeri ek ada pe jaan qurban hai.",
    "Tujhe soch kar hi dil khush ho jata hai,\nTera naam le kar hi din guzar jata hai.",
    "Tere pyar mein hum bikhar gaye,\nTeri yaad mein hum nikhar gaye.",
    "Tum jo na mile toh kya hota,\nMera dil tere bina kya hota.",
    "Teri mohabbat ka rang chadha hai,\nMera dil tere naam pe likha hai.",
    "Tere bina chandni bhi kali lagti hai,\nTere saath andheri raat bhi roshan lagti hai.",
    "Teri yaadon ka silsila chalta rahe,\nTera pyar dil mein palta rahe.",
    "Tujhe chahna meri kismat hai,\nTere saath jeena meri jannat hai.",
    "Tere chehre ki muskaan pe mar jaoon,\nTeri ek ada pe sab kuch waar jaoon.",
    "Dil ne tujhe apni dua bana liya,\nTere naam ko apna khuda bana liya.",
    "Teri yaad mein shab guzar jati hai,\nTere khwab mein subah guzar jati hai.",
    "Tum meri zindagi ka noor ho,\nTum meri mohabbat ka suroor ho.",
    "Tere ishq mein hum fanaa ho gaye,\nTeri yaad mein hum deewana ho gaye.",
    "Tujhe dekh kar lagta hai,\nKhuda ne meri sun li hai.",
    "Tere bina dil ka haal bura hai,\nTere saath har pal suhana hai.",
    "Teri baatein meri jaan hain,\nTeri yaadein meri pehchan hain.",
    "Tum jo mile toh laga,\nMeri duniya badal gayi.",
    "Tere pyar ka diya jalaye rakha hai,\nTere naam ka diya jalaye rakha hai.",
    "Tujhe chahne ki wajah tu hi hai,\nMere jeene ki wajah tu hi hai.",
    "Tere saath har gham khushi lagta hai,\nTere bina har sukh bhi gham lagta hai.",
    "Teri yaad mein dil beqarar hai,\nTera pyar hi mera sansar hai.",
    "Tum meri har dua ka jawab ho,\nTum meri har khushi ka hisaab ho.",
    "Tere ishq mein hum kho gaye,\nTeri yaad mein hum so gaye.",
    "Dil ki kitaab mein tera naam hai,\nMeri har baat mein tera naam hai.",
    "Tujhe paa ke laga sab kuch paa liya,\nTere bina laga sab kuch ganwa diya.",
    "Teri mohabbat meri bandagi hai,\nTeri yaad meri zindagi hai.",
    "Tere chehre ko dekh kar jee leta hoon,\nTeri yaad mein hi mar kar jee leta hoon.",
    "Tum jo hanste ho toh dil khil jata hai,\nTum jo milte ho toh jahan mil jata hai.",
    "Tere bina ye dil udaas hai,\nTere saath har pal khaas hai.",
    "Teri yaadon mein khoya rehta hoon,\nTere pyar mein dooba rehta hoon."
]

HASHTAG_SETS = [
    "#UrduShayari #LoveShayari #HinaFatima #RomanticReels #DilKiBaat",
    "#RomanticReels #Ishq #Mohabbat #HinaFatima #TrendingReels",
    "#ShayariLovers #DilSe #LoveStatus #HinaFatima #ViralReels",
    "#SadShayari #IshqWalaLove #UrduPoetry #HinaFatima #ReelsViral",
    "#MohabbatShayari #Pyar #DilKiAwaaz #HinaFatima #Foryou",
    "#LovePoetry #ShayariVideo #RomanticShayari #HinaFatima #Explore",
    "#DilKaHaal #TeriYaad #IshqShayari #HinaFatima #ReelsInstagram",
    "#UrduLove #ShayariDaily #PyarMohabbat #HinaFatima #TrendingNow",
    "#HeartTouching #EmotionalShayari #LoveStory #HinaFatima #ViralVideo",
    "#ShayariStatus #RomanticStatus #DilKiBaat #HinaFatima #LoveReels",
]

CTA_LINES = [
    "Follow karo ❤️ - Roz nayi shayari ke liye",
    "Apne pyar ko tag karo 🥰",
    "Comment mein ❤️ likho agar dil ko lagi ho",
    "Share karo apne special wale ke saath 💕",
    "Follow kar lo, roz dil ki baat sunne ko milegi ✨",
    "Like karo agar ye shayari tumhare dil ki hai 💔❤️",
]

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

def get_hashtags_and_cta():
    now = datetime.now()
    slot = (now.day * 24 + now.hour)
    hashtags = HASHTAG_SETS[slot % len(HASHTAG_SETS)]
    cta = CTA_LINES[slot % len(CTA_LINES)]
    return hashtags, cta

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
    hashtags, cta = get_hashtags_and_cta()
    caption = f"{shayari}\n\n{cta}\n\n{hashtags}"
    print(f"Selected Shayari: {shayari}")
    print(f"Hashtags: {hashtags}")
    print(f"CTA: {cta}")
    music = download_music_auto()
    if not music:
        print("❌ SONG NAHI BANA - Reel post nahi hogi")
        sys.exit(1)
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

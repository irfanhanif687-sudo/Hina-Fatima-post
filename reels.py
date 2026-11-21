import os, random, requests, subprocess, textwrap, sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")
FB_TOKEN = os.environ.get("FB_TOKEN", "")
PEXELS_KEY = os.environ.get("PEXELS_KEY", "")

if not FB_PAGE_ID or not FB_TOKEN:
    print("ERROR: FB_PAGE_ID ya FB_TOKEN missing hai")
    sys.exit(1)

LOCAL_MUSIC_FILES = [
    "music/Song1.mp3",
    "music/Song2.mp3",
    "music/Song3.mp3",
    "music/Song4.mp3",
    "music/Song5.mp3",
    "music/Song6.mp3",
    "music/Song7.mp3",
    "music/Song8.mp3",
]

SHAYARI = [
    "Teri yaad mein raat bhar neend nahi aati, Tere ishq ne aisi aadat laga di.",
    "Aaj raat tujhe apni jaan bana loon, Tere ishq mein poora doob jaoon.",
    "Tere honthon ki khamoshi bhi shayari lagti hai, Teri ek nazar meri duniya badal deti hai.",
    "Chandni raat mein tera chehra yaad aaya, Dil ne phir tera naam pukara.",
    "Tere bina dil lagta nahi, Tu jo mile to jannat mil jaye.",
    "Teri zulfon ki chhaon mein so jaoon, Teri bahon mein duniya bhool jaoon.",
    "Ishq mein itna doob gaya hoon, Ab saans bhi tere naam se aati hai.",
    "Tere pyaar ka nasha chadha hai aise, Duniya ki har khushi feeki lagti hai.",
    "Raaton ko teri yaad sataati hai, Dil kehta hai tu paas aa jaye.",
    "Teri ek muskaan pe fida ho gaya, Ab dil kisi aur ka hone se raha.",
    "Tujhe dekh ke dil dhadakna bhool jata hai, Tu meri har dua ka jawab hai.",
    "Mohabbat mein teri had se guzar jaoon, Teri ek jhalak pe sab kuch luta doon.",
    "Tere ishq mein pagal ho gaya hoon, Log kehte hain deewana ho gaya hoon.",
    "Teri yaadein meri raaton ki rani hain, Tere bina ye raatein kitni veerani hain.",
    "Dil chahta hai tujhe seene se laga loon, Teri saanson mein apni saans mila loon.",
    "Tu jo hanse to phool khil jayein, Teri khushi pe meri jaan qurbaan.",
    "Tere naam ki mehndi laga loon, Tujhe apni dulhan bana loon.",
    "Aaj phir teri yaad ne rula diya, Dil ne phir tera naam liya.",
    "Tere pyaar mein jeena seekh liya, Tere bina marna bhi seekh liya.",
    "Teri aankhon mein doobna chahta hoon, Tere ishq mein kho jana chahta hoon.",
    "Tere ishq ka rang chadha hai mujh pe, Ab duniya ki koi rang acha nahi lagta.",
    "Teri ek jhalak ke liye taras gaya dil, Tu mile to zindagi mil jaye.",
    "Mohabbat teri itni gehri hai, Ke saans bhi tere naam se leti hoon.",
    "Tere pyaar mein khud ko bhool gayi hoon, Ab bas teri yaad mein jeeti hoon.",
    "Chand ko dekh ke teri yaad aati hai, Tu chand se zyada haseen lagti hai.",
    "Dil ki har dhadkan mein tera naam hai, Tu meri har dua mein shamil hai.",
    "Teri mohabbat ne deewana bana diya, Ab log mujhe tere naam se pukarte hain.",
    "Tere bina ye duniya veeran lagti hai, Tu jo paas ho to jannat lagti hai.",
    "Teri yaad ka diya jal raha hai, Mere dil mein tera naam pal raha hai.",
    "Ishq mein tere itna kho gayi, Ke khud ko bhi bhool gayi.",
]

HASHTAGS = [
    "#HinaFatima #Ishq #Mohabbat #RomanticShayari #Love",
    "#Shayari #UrduShayari #IshqWalaLove #Romantic #Dil",
    "#LoveStory #Tanhai #Yaadein #RomanticReels #Hina",
    "#DilKiBaat #IshqShayari #RomanticStatus #LoveShayari #Fatima",
    "#Pyar #MohabbatShayari #UrduPoetry #DilSe #Reels",
    "#RomanticVibes #IshqHai #ShayariLover #LoveQuotes #HinaFatima",
    "#TeriYaad #DilKaDard #RomanticPoetry #IshqKaNasha #Pyar",
    "#ShayariReels #LoveVibes #MohabbatHai #UrduReels #DilKiShayari",
    "#DilKiAwaaz #IshqMubarak #RomanticQuotes #PyarMohabbat #ShayariLove",
    "#YaadTeri #IshqWala #DilDiyanGallan #LoveLife #HinaFatimaReels",
    "#ShayariStatus #RomanticMood #TereIshqMein #DilSeDilTak #LoveStory",
    "#MohabbatZindabad #IshqKaRang #UrduShayariReels #RomanticLove #PyarKaNasha",
    "#DilKaRishta #TeriMohabbat #ShayariKaJadoo #IshqDiGali #RomanticDil",
    "#LoveKaIshq #RomanticDil #YaadeinTeri #MohabbatKiBaatein #ReelsLove",
    "#IshqTera #DilKaSukoon #ShayariDilSe #PyarKiDuniya #HinaFatimaLove",
    "#TeraMeraIshq #RomanticNights #DilKiDhadkan #MohabbatKaSafar #LoveReels",
    "#ShayariKaDard #IshqKiRaatein #UrduLove #DilKaIshq #RomanticQuotes",
    "#PyarKaEhsaas #TeriYaadein #RomanticShayariReels #MohabbatKaJadoo #Dil",
    "#IshqKaJunoon #LoveShayariReels #TereBina #DilKiBaatShayari #PyarShayari",
    "#HinaKiShayari #FatimaLove #IshqShayariReels #RomanticUrdu #PyarShayari",
    "#DilKaIshq #TeriChahat #MohabbatKiShayari #RomanticFeelings #IshqLove",
    "#Yaadein #TanhaiShayari #DilKaHaal #IshqKaDard #RomanticYaadein",
    "#MohabbatKaEhsaas #PyarKiShayari #DilKiDuniya #IshqKiBaatein #LovePoetry",
    "#TereLiye #MeriJaan #DilKaPyaar #IshqKiDuniya #RomanticBaatein",
    "#ShayariKaIshq #DilSeShayari #MohabbatKaPaigham #PyarKaPaigham #IshqKaPaigham",
    "#RomanticIshq #DilKaArmaan #TeriAarzoo #MohabbatKiRaat #IshqKiRaat",
    "#PyarKaSafar #IshqKaSafar #DilKaSafar #MohabbatKaSafar #RomanticSafar",
    "#TeriBewafai #DilKaDardShayari #IshqKaGham #MohabbatKaGham #YaadKaDard",
    "#DilKiTanhai #IshqKiTanhai #TanhaiKaDard #PyarKaDard #MohabbatKaDard",
    "#HinaFatimaShayari #FatimaKiShayari #HinaKaIshq #DilKaIshqShayari #RomanticHina",
]

HOOKS = [
    "Ye shayari kis ke liye hai? Comment mein uska naam likho ❤️",
    "Agar dil ko lagi to Follow kar lo, roz aisi shayari milegi 💕",
    "Save kar lo, jab uski yaad aaye to phir sun lena 🥺❤️",
    "Jis ko yaad karke ye suna, usko ye reel bhej do 💌",
    "Dil se lagi? To dil se Follow bhi kar do ✨",
    "Ye wali shayari usko suna do jiske bina neend nahi aati 🌙",
    "Comment mein ❤️ likho agar ye tumhari kahani hai",
    "Share kar do uske saath jisse tum bepanah mohabbat karte ho 💖",
    "Follow karo Hina Fatima ko, har raat ek nayi shayari ke liye 🌹",
    "Is shayari ko apni story pe lagao, wo dekh lega 😉❤️",
]

def get_pexels_video():
    queries = ["romantic couple","couple love","romantic sunset","couple holding hands","romantic night","love couple"]
    q = random.choice(queries)
    print(f"Pexels video search: {q}")
    try:
        headers = {"Authorization": PEXELS_KEY} if PEXELS_KEY else {}
        r = requests.get(f"https://api.pexels.com/videos/search?query={q}&per_page=15&orientation=portrait", headers=headers, timeout=20)
        videos = r.json().get("videos", [])
        print(f"Pexels videos found: {len(videos)}")
        if not videos:
            return None
        v = random.choice(videos)
        files = v.get("video_files", [])
        best = None
        for f in files:
            if f.get("width", 0) >= 720 and f.get("height", 0) >= 1280:
                best = f
                break
        if not best and files:
            best = files[0]
        url = best["link"]
        data = requests.get(url, timeout=60).content
        open("bg_video.mp4","wb").write(data)
        print(f"Video downloaded: {os.path.getsize('bg_video.mp4')} bytes")
        if os.path.getsize("bg_video.mp4") < 50000:
            return None
        return "bg_video.mp4"
    except Exception as e:
        print(f"Pexels video fail: {e}")
        return None

def make_text_overlay(shayari):
    img = Image.new("RGBA", (1080, 1920), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 650, 1080, 1150], fill=(0,0,0,110))
    try:
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 58)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 38)
    except:
        font_big = ImageFont.load_default()
        font_small = font_big
    lines = textwrap.wrap(shayari, width=24)
    y = 750
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=font_big)
        w = bbox[2]-bbox[0]
        draw.text(((1080-w)//2, y), line, font=font_big, fill=(255,255,255,255), stroke_width=3, stroke_fill=(0,0,0,255))
        y += 80
    txt = "— Hina Fatima —"
    bbox2 = draw.textbbox((0,0), txt, font=font_small)
    w2 = bbox2[2]-bbox2[0]
    draw.text(((1080-w2)//2, y+40), txt, font=font_small, fill=(255,200,220,255))
    img.save("text_overlay.png")
    return "text_overlay.png"

def pick_song(now):
    slot = (now.timetuple().tm_yday * 12 + now.hour // 2) % 8
    ordered = LOCAL_MUSIC_FILES[slot:] + LOCAL_MUSIC_FILES[:slot]
    for s in ordered:
        if os.path.exists(s) and os.path.getsize(s) > 100000:
            return s
    return None

def build_video(shayari, song):
    bg_video = get_pexels_video()
    overlay = make_text_overlay(shayari)
    if not bg_video:
        print("No Pexels video, using photo fallback")
        img = Image.new("RGB", (1080, 1920), (20, 10, 30))
        img.save("reel_frame.jpg", quality=95)
        for encoder in ["libx264", "mpeg4"]:
            cmd = ["ffmpeg","-y","-loop","1","-i","reel_frame.jpg","-i",song,"-t","15",
                   "-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
                   "-c:v",encoder,"-pix_fmt","yuv420p","-r","30","-c:a","aac","-ar","44100","-ac","2","-movflags","+faststart","-shortest","reel.mp4"]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode==0 and os.path.exists("reel.mp4") and os.path.getsize("reel.mp4")>10000:
                return True
        return False
    # FIXED: overlay ko -loop 1 kiya, aur overlay filter se shortest=1 hataya - ab video 15 sec ki banegi, 1 sec ki nahi
    for encoder in ["libx264", "mpeg4"]:
        cmd = [
            "ffmpeg", "-y",
            "-i", bg_video,
            "-i", song,
            "-loop", "1", "-i", overlay,
            "-t", "15",
            "-filter_complex",
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[bg];[bg][2:v]overlay=(W-w)/2:0[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", encoder, "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            "-movflags", "+faststart",
            "-shortest",
            "reel.mp4"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists("reel.mp4") and os.path.getsize("reel.mp4") > 10000:
            print(f"Moving Video OK with {encoder} - 15 sec")
            return True
        print(f"Moving video failed with {encoder}: {result.stderr[-800:]}")
    return False

def upload_reel_facebook(video_path, caption):
    file_size = os.path.getsize(video_path)
    print(f"Upload START - file size {file_size}")
    start_url = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/video_reels"
    r1 = requests.post(start_url, data={
        "access_token": FB_TOKEN,
        "upload_phase": "start",
        "file_size": str(file_size),
    }, timeout=60)
    print(f"START: {r1.status_code} - {r1.text}")
    if r1.status_code != 200:
        raise SystemExit(f"START Failed: {r1.text}")
    data1 = r1.json()
    video_id = data1.get("video_id")
    upload_url = data1.get("upload_url")
    if not video_id or not upload_url:
        raise SystemExit(f"START missing: {r1.text}")
    print(f"Upload TRANSFER - {video_id}")
    with open(video_path, "rb") as f:
        video_bytes = f.read()
    headers = {
        "Authorization": f"OAuth {FB_TOKEN}",
        "Offset": "0",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(video_bytes)),
        "X-Entity-Length": str(len(video_bytes)),
    }
    r2 = requests.post(upload_url, headers=headers, data=video_bytes, timeout=300)
    print(f"TRANSFER: {r2.status_code} - {r2.text}")
    if r2.status_code != 200:
        raise SystemExit(f"TRANSFER Failed: {r2.text}")
    print(f"Upload FINISH...")
    r3 = requests.post(start_url, data={
        "access_token": FB_TOKEN,
        "upload_phase": "finish",
        "video_id": video_id,
        "video_state": "PUBLISHED",
        "description": caption,
    }, timeout=120)
    print(f"FINISH: {r3.status_code} - {r3.text}")
    if r3.status_code != 200:
        raise SystemExit(f"FINISH Failed: {r3.text}")
    print("SUCCESS - Reel posted!")
    return True

def main():
    now = datetime.now()
    total_slot = now.timetuple().tm_yday * 12 + now.hour // 2
    song = pick_song(now)
    if not song:
        raise SystemExit("No valid song found")
    shayari = SHAYARI[total_slot % len(SHAYARI)]
    tags = HASHTAGS[total_slot % len(HASHTAGS)]
    hook = HOOKS[total_slot % len(HOOKS)]
    print(f"Slot {total_slot} - Song {song} - Shayari {shayari[:20]}")
    caption = f"{shayari}\n\n{hook}\n\n❤️ Hina Fatima ❤️\n\n{tags}"
    if not build_video(shayari, song):
        raise SystemExit("FFmpeg failed")
    upload_reel_facebook("reel.mp4", caption)

if __name__ == "__main__":
    main()

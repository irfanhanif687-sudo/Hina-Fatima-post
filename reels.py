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

# 30 HASHTAG SETS - SAFE, BAN WALE HATA DIYE - HAR BAAR ALAG
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

# ATTRACTIVE HOOK + FOLLOW CTA - HAR BAAR ALAG, LOG FOLLOW KARENGE
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

def make_black_bg():
    img = Image.new("RGB", (1080, 1920), (20, 10, 30))
    img.save("bg.jpg")
    return "bg.jpg"

def get_image():
    if not PEXELS_KEY:
        return make_black_bg()
    try:
        headers = {"Authorization": PEXELS_KEY}
        r = requests.get("https://api.pexels.com/v1/search?query=romantic%20couple%20night&per_page=15", headers=headers, timeout=20)
        photos = r.json().get("photos", [])
        if not photos:
            return make_black_bg()
        url = random.choice(photos)["src"]["large2x"]
        open("bg.jpg","wb").write(requests.get(url, timeout=20).content)
        test = Image.open("bg.jpg")
        test.verify()
        return "bg.jpg"
    except Exception as e:
        print(f"【entity-Pexels¦canonical_name=Pexels】 fail: {e}")
        return make_black_bg()

def make_reel_image(shayari):
    bg = get_image()
    try:
        img = Image.open(bg).convert("RGB")
    except:
        img = Image.new("RGB", (1080, 1920), (20, 10, 30))
    img = img.resize((1080, 1920))
    overlay = Image.new("RGBA", img.size, (0,0,0,90))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
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
        draw.text(((1080-w)//2, y), line, font=font_big, fill=(255,255,255), stroke_width=2, stroke_fill=(0,0,0))
        y += 80
    txt = "— Hina Fatima —"
    bbox2 = draw.textbbox((0,0), txt, font=font_small)
    w2 = bbox2[2]-bbox2[0]
    draw.text(((1080-w2)//2, y+40), txt, font=font_small, fill=(255,200,220))
    img.save("reel_frame.jpg", quality=95)
    return "reel_frame.jpg"

def pick_song(now):
    slot = (now.timetuple().tm_yday * 12 + now.hour // 2) % 8
    ordered = LOCAL_MUSIC_FILES[slot:] + LOCAL_MUSIC_FILES[:slot]
    for s in ordered:
        if os.path.exists(s) and os.path.getsize(s) > 100000:
            return s
    return None

def build_video(frame, song):
    for encoder in ["libx264", "mpeg4"]:
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-loop", "1", "-i", frame,
            "-i", song,
            "-t", "15",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
            "-c:v", encoder, "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-ar", "44100", "-ac", "2",
            "-movflags", "+faststart",
            "-shortest",
            "reel.mp4"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and os.path.exists("reel.mp4") and os.path.getsize("reel.mp4") > 10000:
            print(f"Video OK with {encoder}")
            return True
    return False

def main():
    now = datetime.now()
    # SAFE ROTATION - Har baar alag hashtag, alag shayari, alag hook
    # Din + ghanta + minute se hisaab, taake kabhi repeat na ho
    total_slot = now.timetuple().tm_yday * 12 + now.hour // 2
    song = pick_song(now)
    if not song:
        raise SystemExit("No valid song found")
    # Shayari bhi time se - har baar alag
    shayari = SHAYARI[total_slot % len(SHAYARI)]
    # Hashtag bhi time se - har baar alag, 30 mein se
    tags = HASHTAGS[total_slot % len(HASHTAGS)]
    # Hook bhi time se - har baar alag follow wali line
    hook = HOOKS[total_slot % len(HOOKS)]
    print(f"Slot {total_slot} - Song {song} - Shayari {shayari[:20]} - Tags {tags} - Hook {hook[:20]}")

    caption = f"{shayari}\n\n{hook}\n\n❤️ Hina Fatima ❤️\n\n{tags}"

    frame = make_reel_image(shayari)
    if not os.path.exists(frame) or os.path.getsize(frame) < 1000:
        raise SystemExit("Frame not created!")
    if not build_video(frame, song):
        raise SystemExit("FFmpeg failed")
    url = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/video_reels"
    with open("reel.mp4","rb") as f:
        r = requests.post(url, data={"access_token": FB_TOKEN, "description": caption}, files={"file": f}, timeout=300)
    print(f"Facebook: {r.status_code} - {r.text}")
    if r.status_code != 200:
        raise SystemExit(f"Facebook Failed: {r.text}")
    print("SUCCESS - Reel posted!")

if __name__ == "__main__":
    main()

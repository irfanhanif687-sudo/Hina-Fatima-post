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

# ✅ FINAL - SIRF INDIAN ROMANTIC - 6 TRACKS - Sab Direct MP3 - Koi WAV Nahi
# 1 = Sitar Moonlight, 2 = Bansuri Ambient, 3 = Indian Flute Meditation
# 4 = Sitar Romance 2, 5 = Bansuri + Tabla, 6 = Backup Sitar
FREE_MUSIC_URLS = [
    "https://cdn.pixabay.com/download/audio/2022/07/25/audio_25c05ffd84.mp3?filename=sitar-in-the-moonlight-115602.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=flute-ambient-112328.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_1c3a9d7da9.mp3?filename=indian-flute-meditation-music-22823.mp3",
    "https://cdn.pixabay.com/download/audio/2022/07/25/audio_25c05ffd84.mp3?filename=sitar-in-the-moonlight-115602.mp3",
    "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=flute-ambient-112328.mp3",
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_1c3a9d7da9.mp3?filename=indian-flute-meditation-music-22823.mp3",
]

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
    "Raat bhar teri baahon mein rehna chahta hoon,\nTeri saanson ki garmi mein kho jana chahta hoon.",
    "Tere honthon ki pyaas bujha doon,\nTujhe apni baahon mein sula doon.",
    "Teri gardan pe apne honth rakh doon,\nTeri har saans ko apna kar doon.",
    "Aaj raat tu paas aa ja,\nTere bina neend nahi aati mujhe.",
    "Tere seene se lag kar so jaoon,\nTeri dhadkan sun kar kho jaoon.",
    "Teri baahon ka takiya bana loon,\nTeri yaadon mein raat guzaar doon.",
    "Tujhe itna kareeb kar loon,\nKe saans bhi ek ho jaye hamari.",
    "Tere badan ki khushbu mujhe pagal kar deti hai,\nTeri ek nazar mujhe deewana kar deti hai.",
    "Raat ki tanhai mein tu yaad aati hai,\nTeri baahon ki kami bahut satati hai.",
    "Tere honthon pe apna naam likh doon,\nTeri har raat ko apni subah kar doon.",
    "Tujhe chhoo kar jo ehsaas hota hai,\nWoh jannat se bhi zyada khaas hota hai.",
    "Teri kamar pe haath rakh kar chalu,\nTujhe apni duniya bana loon.",
    "Aaj ki raat sirf teri ho jaoon,\nTere ishq mein poori tarah kho jaoon.",
    "Tere kaano mein dheere se keh doon,\nAaj raat tu meri hai, main tera hoon.",
    "Teri saans meri saans se takraye,\nAisa pyaar kabhi khatam na ho paye.",
    "Tujhe dekh kar dil beqabu ho jata hai,\nTere kareeb aate hi sab bhool jata hai.",
    "Teri zulfon mein ungliyaan phira doon,\nTeri har thakan ko mita doon.",
    "Tere honthon ki lali pe mar jaoon,\nTeri ek ada pe sab kuch waar jaoon.",
    "Raat ko jab tu paas hoti hai,\nMeri har dua qabool hoti hai.",
    "Tere seene ki dhadkan sunna chahta hoon,\nTujhe apni baahon mein rakhna chahta hoon.",
    "Tujhe itna pyaar doon ke tu sharma jaye,\nTeri har raat ko yaadgar bana jaye.",
    "Teri garmi mein pighal jaoon,\nTere ishq mein jal kar khaak ho jaoon.",
    "Aaj raat chandni mein tu aur main,\nBas pyaar ki baatein, aur koi nahi.",
    "Tere badan se lipat jaoon,\nTeri yaadon mein doob jaoon.",
    "Tujhe apne kareeb itna kar loon,\nKe duniya bhool jaye hum dono ko.",
    "Tere honthon ka nasha utarta hi nahi,\nTere bina dil kahin lagta hi nahi.",
    "Raat bhar tujhe dekhte rahoon,\nTeri baahon mein hi sote rahoon.",
    "Teri ek jhalak pe dil tadap jata hai,\nTere kareeb aate hi sab ruk jata hai.",
    "Tujhe seene se laga kar rakhoon,\nTeri har saans ko apna kar loon.",
    "Aaj raat tu mujhse door mat ja,\nTeri baahon mein hi sone de mujhe.",
    "Tere labon ki mithaas chakh loon,\nTeri har ada pe mar jaoon.",
    "Teri nazron ka jaadu chha gaya hai,\nMera dil tere naam ho gaya hai.",
    "Tujhe raat bhar pyaar karoon,\nTeri har khwahish ko poora karoon.",
    "Tere paas aate hi saans tez ho jati hai,\nTeri ek muskaan pe jaan nikal jati hai.",
    "Teri baahon mein jo aag hai,\nWoh kisi aur mein kahan.",
    "Tujhe apni god mein bitha loon,\nTeri zulfon ko sehla loon.",
    "Raat ki khamoshi mein sirf tu ho,\nAur meri baahon mein sirf tu ho.",
    "Tere ishq ka nasha sar chadha hai,\nTere bina dil kahin lagta nahi.",
    "Tujhe choom kar jo sukoon milta hai,\nWoh duniya mein kahin nahi milta.",
    "Teri saanson ki khushbu mein kho jaoon,\nTere pyaar mein doob jaoon.",
    "Aaj raat bas tu aur main,\nNa duniya, na koi parwah.",
    "Tere honthon se honth mila doon,\nTeri har pyaas ko bujha doon.",
    "Tujhe itna kareeb kar loon ke,\nTeri dhadkan meri dhadkan ban jaye.",
    "Teri baahon mein raat guzar jaye,\nTeri yaadon mein subah ho jaye.",
    "Tere badan ki garmi mujhe jala deti hai,\nTeri ek ada mujhe pagal kar deti hai.",
    "Tujhe pyaar karte karte raat ho jaye,\nTeri baahon mein hi subah ho jaye.",
    "Tere seene pe sar rakh kar so jaoon,\nTeri dhadkan sun kar kho jaoon.",
    "Tujhe dekh kar dil machal jata hai,\nTere kareeb aate hi sab badal jata hai.",
    "Raat bhar teri yaadon mein jalte rahe,\nTere ishq mein hum palte rahe.",
    "Teri ek raat ki khwahish hai mujhe,\nTeri baahon mein sone ki chahat hai mujhe.",
    "Teri chhat pe haath rakh ke so jaoon,\nTeri dhadkan ko apni lori bana loon.",
    "Tu jo sharma ke mere seene mein chhup jaye,\nMera dil or zor se dhadak jaye.",
    "Teri kamar ko pakad ke apne kareeb kar loon,\nTeri har saans ko apni bana loon.",
    "Aaj raat teri galiyon mein kho jaoon,\nTere honthon ki galiyon mein kho jaoon.",
    "Tere kaan ke peeche ek pyaar bhara kiss doon,\nTeri har thakan ko door kar doon.",
    "Tu jo mere honthon pe ungli rakh de,\nMeri saari baatein ruk jayen.",
    "Teri aankhon mein dekh ke lagta hai,\nJaise saari raat abhi baaki hai.",
    "Tujhe raat bhar apne seene se laga ke rakhoon,\nTeri garmi mein hi so jaoon.",
    "Tere honthon ki narmi ko mehsoos karoon,\nTeri har ada pe fida ho jaoon.",
    "Tu jab mere itne paas aati hai,\nMujhe apna aapa bhool jata hai.",
    "Teri saans jab mere chehre pe lagti hai,\nDil mein ek toofan sa uth jata hai.",
    "Aaj raat tujhe apni jaan bana loon,\nTere ishq mein poora doob jaoon.",
    "Tere badan ki har khushbu ko pee loon,\nTere pyaar mein khud ko bhool jaoon.",
    "Tujhe dekh ke dil kehta hai,\nKaash ye raat kabhi khatam na ho.",
    "Teri baahon mein aake lagta hai,\nJaise duniya ki har khushi mil gayi.",
    "Tu jo mere gaal pe haath phere,\nMera dil pighal jaye.",
    "Teri god mein sar rakh ke so jaoon,\nTeri ungliyon mein kho jaoon.",
    "Aaj raat tu meri baahon mein so ja,\nKal subah tak kahin mat ja.",
    "Tere honthon pe apni ungli phira doon,\nTeri har khamoshi ko samajh jaoon.",
    "Tujhe itna pyaar karoon ke tu thak jaye,\nPhir bhi mera dil na bhare.",
    "Teri raat wali khushbu mujhe pagal karti hai,\nTeri ek jhalak mujhe deewana karti hai.",
    "Tu jo hanste hue mere kareeb aaye,\nMera dil teri taraf khinch jaye.",
    "Tere seene ki garmi mein lipt jaoon,\nTeri yaadon mein hi mar jaoon.",
    "Aaj raat bas pyaar ki baarish ho,\nTu aur main, aur koi na ho.",
    "Tere honthon ka rang mere honthon pe lag jaye,\nAisa pyaar kabhi na mit paye.",
    "Tujhe baahon mein utha ke ghoom loon,\nTeri har muskaan ko choom loon.",
    "Teri neend mein bhi tujhe dekhta rahoon,\nTeri har saans ko ginta rahoon.",
    "Tu jo raat ko call pe dheere se bole,\nMera dil or zor se dhadak uthe.",
    "Tere pyaar mein raat bhar jaag loon,\nTeri yaadon mein hi so jaoon.",
    "Tujhe apne honthon se apna naam suna doon,\nTeri har raat ko apni bana loon.",
    "Teri kamar se lipat ke so jaoon,\nTeri khushbu mein hi kho jaoon.",
    "Aaj raat teri baahon ka nasha kar loon,\nTere ishq mein hi mar jaoon.",
    "Tu jo mere seene pe haath rakhe,\nMeri dhadkan teri ho jaye.",
    "Tere labon ki garmi ko mehsoos karoon,\nTeri har saans mein bas jaoon.",
    "Tujhe raat bhar apni aankhon mein rakhoon,\nTeri har ada ko yaad karoon.",
    "Teri ek raat ki mehmaan nawazi chahiye,\nTeri baahon mein sone ki ijazat chahiye.",
    "Tu jo paas aake mere kaan mein bole,\nMeri rooh tak kaamp jaye.",
    "Tere ishq mein raat din ek kar doon,\nTeri ek muskaan pe sab kuch kurban kar doon.",
    "Tujhe choom choom ke thak jaoon,\nPhir bhi tera pyaar na khatam ho.",
    "Aaj raat teri god mein duniya bhool jaoon,\nTere pyaar mein hi doob jaoon.",
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
    "#TeriYaad #DilKiBaat #RomanticShayari #HinaFatima #ForyouPage",
    "#LoveStory #IshqWala #UrduShayari #HinaFatima #ViralReels",
    "#PyarKiBaat #DilSeDil #ShayariReels #HinaFatima #ExplorePage",
    "#RomanticVibes #Tanhai #Mohabbat #HinaFatima #ReelsOfInstagram",
    "#IshqZada #DilKaDard #LoveShayari #HinaFatima #Trending",
    "#ShayariLover #RaatKiBaat #RomanticReels #HinaFatima #Viral",
    "#DilKiAwaaz #TeriMohabbat #UrduPoetry #HinaFatima #ReelsVideo",
    "#LoveQuotes #PyarMohabbat #Shayari #HinaFatima #ForYou",
    "#RomanticStatus #DilTootGaya #ShayariVideo #HinaFatima #TrendingReels",
    "#HinaFatima #IshqShayari #LoveReels #UrduShayari #DilKiBaat",
]

CTA_LINES = [
    "❤️ Follow karo - Roz raat ko nayi bold shayari ke liye, miss mat karna!",
    "🥰 Apne pyar ko tag karo + Follow karo - Roz aisi shayari ke liye",
    "💕 Comment mein ❤️ likho + Follow karo - Agli shayari tumhare naam hogi",
    "✨ Share karo apne special wale ke saath + Page ko Follow karo",
    "🔥 Follow kar lo - Roz 12 reels aati hain, ek bhi miss mat karo!",
    "❤️ Like + Follow - Agar ye shayari tumhare dil ki hai to",
    "👉 Follow nahi kiya to agli wali bold shayari miss ho jayegi!",
    "💔 Tag karo usko jiske liye ye shayari hai + Follow karo Hina Fatima ko",
    "🌙 Raat ki shayari ke liye Follow karo - Roz nayi feeling",
    "💌 Share + Follow - Apne pyar ko ye reel bhejo, wo khush ho jayega",
]

# ✅ FIX 1: Slot formula - ab har 2 ghante me alag shayari, alag hashtag, alag dhun
def get_slot():
    now = datetime.now()
    # Din + Ghanta + Aadha ghanta - har slot unique
    return (now.day * 100 + now.hour * 2 + (1 if now.minute >= 30 else 0))

def get_shayari_for_this_slot():
    slot = get_slot()
    index = slot % len(REEL_SHAYARI)
    return REEL_SHAYARI[index]

def get_hashtags_and_cta():
    slot = get_slot()
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
        if part.strip():
            wrapped.extend(wrap_line(part.strip()))
    # ✅ FIX 2: Transparent overlay - 1080x1920 fixed
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
        # Black border taake white text video pe saaf dikhe
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)]:
            draw.text((x+dx, y+dy), line, font=font, fill=(0,0,0,255))
        draw.text((x, y), line, font=font, fill=(255,255,255,255))
        y += 70
    # ✅ FIX 3: Purani file ho to pehle delete karo
    if os.path.exists("shayari_overlay.png"):
        try:
            os.remove("shayari_overlay.png")
        except:
            pass
    img.save("shayari_overlay.png")
    print(f"✅ Text image ban gayi: {wrapped}")
    return "shayari_overlay.png"

# ✅ FIX 4: Direct MP3 - Koi WAV, Koi Convert Nahi - Sirf Indian Romantic
def get_free_real_music():
    slot = get_slot()
    start_index = slot % len(FREE_MUSIC_URLS)
    ordered = FREE_MUSIC_URLS[start_index:] + FREE_MUSIC_URLS[:start_index]
    # Purani music file delete karo
    if os.path.exists("background.mp3"):
        try:
            os.remove("background.mp3")
        except:
            pass
    for i, url in enumerate(ordered):
        for attempt in range(2):
            try:
                print(f"Trying INDIAN ROMANTIC dhun {i+1}/6 - Attempt {attempt+1}/2 - {url[:60]}")
                headers = {"User-Agent": "Mozilla/5.0"}
                r = requests.get(url, headers=headers, timeout=40)
                print(f"Download status: {r.status_code} size: {len(r.content)}")
                # ✅ FIX 5: 100KB se choti file ko reject karo - khaali file nahi chalegi
                if r.status_code == 200 and len(r.content) > 100000:
                    with open("background.mp3", "wb") as f:
                        f.write(r.content)
                    time.sleep(1)
                    final_size = os.path.getsize("background.mp3")
                    print(f"✅ INDIAN ROMANTIC DHUN DOWNLOAD HO GAYI - {final_size} bytes")
                    if final_size > 100000:
                        return "background.mp3"
                else:
                    print("❌ File choti hai, agli dhun try...")
                    time.sleep(2)
            except Exception as e:
                print(f"❌ Download fail: {e}, 2 sec ruk ke dobara...")
                time.sleep(2)
                continue
    print("❌ Koi bhi Indian dhun download nahi hui - Reel bina dhun ke banegi")
    return None

def get_random_reel_video():
    print("Fetching video from Pexels - AUTO...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing hai!")
        sys.exit(1)
    queries = ["romantic couple", "couple in love", "couple holding hands", "couple sunset", "couple hug romantic"]
    headers = {"Authorization": PEXELS_KEY}
    for attempt in range(3):
        try:
            params = {"query": random.choice(queries), "per_page": 15, "orientation": "portrait", "size": "medium"}
            res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=25)
            print(f" Pexels Status Attempt {attempt+1}: {res.status_code}")
            res.raise_for_status()
            videos = res.json().get('videos', [])
            if not videos:
                print("❌ Pexels ne video nahi diya, dobara try...")
                time.sleep(2)
                continue
            selected = random.choice(videos)
            files = selected.get('video_files', [])
            if not files:
                print("❌ Video files empty, dobara try...")
                time.sleep(2)
                continue
            # ✅ FIX 6: Sirf portrait video lo - 700 se 1080 height wali
            suitable = [f for f in files if 700 <= f.get('height', 0) <= 1080]
            if suitable:
                best = random.choice(suitable)
            else:
                best = sorted(files, key=lambda x: x.get('height', 0))[0]
            print(f"Found video: {best.get('link')} height={best.get('height')}")
            return best.get('link')
        except Exception as e:
            print(f"❌ Video fetch error attempt {attempt+1}: {e}")
            time.sleep(3)
            continue
    print("❌ 3 baar try kiya, video nahi mila")
    sys.exit(1)

def make_final_reel(video_url, shayari_text, music_path):
    raw_path = "raw_reel.mp4"
    print("Downloading raw video - 1 se 2 minute lag sakta hai...")
    for attempt in range(2):
        try:
            if os.path.exists(raw_path):
                os.remove(raw_path)
            with requests.get(video_url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(raw_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            raw_size = os.path.getsize(raw_path)
            print(f"Raw size: {raw_size} bytes")
            if raw_size > 100000:
                break
            else:
                print("❌ Video choti hai, dobara download...")
                time.sleep(2)
                continue
        except Exception as e:
            print(f"❌ Video download fail attempt {attempt+1}: {e}")
            time.sleep(3)
            continue
    if not os.path.exists(raw_path) or os.path.getsize(raw_path) < 100000:
        print("❌ Video download nahi hua")
        sys.exit(1)
    overlay = make_text_image(shayari_text)
    final_path = "final_reel.mp4"
    if os.path.exists(final_path):
        try:
            os.remove(final_path)
        except:
            pass
    # ✅ FIX 7: Music hai to music wala filter, nahi hai to bina music wala - dono alag alag, koi mix nahi
    if music_path and os.path.exists(music_path) and os.path.getsize(music_path) > 100000:
        print(f"Adding INDIAN ROMANTIC DHUN: {music_path} - {os.path.getsize(music_path)} bytes")
        # [0:v]=video, [1:v]=overlay image, [2:a]=music
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];"
            "[v][1:v]overlay=0:0[outv];"
            "[2:a]volume=1.0,afade=t=in:st=0:d=0.5,afade=t=out:st=14:d=1[outa]"
        )
        cmd = ["ffmpeg", "-y",
               "-i", raw_path,
               "-i", overlay,
               "-stream_loop", "-1", "-i", music_path,
               "-filter_complex", filter_complex,
               "-map", "[outv]", "-map", "[outa]",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
               "-c:a", "aac", "-t", "15", final_path]
    else:
        print("Bina dhun ke reel bana raha hoon - music nahi mila")
        filter_complex = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];[v][1:v]overlay=0:0[outv]"
        cmd = ["ffmpeg", "-y",
               "-i", raw_path,
               "-i", overlay,
               "-filter_complex", filter_complex,
               "-map", "[outv]",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
               "-t", "15", final_path]
    print("Running FFmpeg final - 1 minute lag sakta hai...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ FFmpeg Final Error - POORA ERROR:")
        print(result.stderr[-2000:])
        sys.exit(1)
    final_size = os.path.getsize(final_path)
    print(f"✅ Final Reel Ready: {final_size} bytes")
    if final_size < 100000:
        print("❌ Final reel bahut choti hai")
        sys.exit(1)
    return final_path

def upload_reel_to_facebook(video_path, caption):
    file_size = os.path.getsize(video_path)
    if file_size < 100000:
        print("❌ Video bahut choti hai")
        sys.exit(1)
    print("Starting Facebook Reel upload...")
    start_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        start_res = requests.post(start_url, data={"upload_phase": "start", "access_token": TOKEN}, timeout=25)
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
    print("Uploading file - 1 minute lag sakta hai...")
    try:
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(file_size)}, data=f, timeout=120)
        print(f"Upload Status: {upload_res.status_code}")
        upload_res.raise_for_status()
        print("✅ File uploaded")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)
    print("Facebook ko 10 sec de raha hoon...")
    time.sleep(10)
    print("Publishing...")
    finish_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        finish_res = requests.post(finish_url, data={
            "access_token": TOKEN, "video_id": video_id,
            "upload_phase": "finish", "video_state": "PUBLISHED",
            "description": caption
        }, timeout=35)
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
    print("Shuru ho gaya - 1 se 4 minute lagega, Indian Romantic dhun ke saath...")
    music = get_free_real_music()
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

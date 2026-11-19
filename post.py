import os
import random
import requests
import sys
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v21.0"

SHAYARI = [
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
]

HASHTAG_SETS_PICS = [
    "#UrduShayari #LoveShayari #HinaFatima #DilKiBaat #Romantic",
    "#ShayariLovers #Mohabbat #Ishq #HinaFatima #UrduPoetry",
    "#LoveStatus #DilSe #HinaFatima #ShayariDaily #Trending",
    "#RomanticShayari #Pyar #HinaFatima #Emotional #Viral",
    "#SadShayari #DilKaHaal #HinaFatima #LoveStory #Foryou",
    "#UrduLove #ShayariVideo #HinaFatima #Explore #HeartTouching",
    "#IshqShayari #TeriYaad #HinaFatima #MohabbatShayari #Daily",
    "#DilKiAwaaz #PyarMohabbat #HinaFatima #TrendingNow #Love",
    "#ShayariStatus #RomanticStatus #HinaFatima #ViralPost #Dil",
    "#HeartTouchingShayari #LovePoetry #HinaFatima #ShayariLovers #New",
]

CTA_PICS = [
    "Follow karo ❤️",
    "Like karo agar dil ko lagi ho 💕",
    "Apne pyar ko tag karo 🥰",
    "Comment mein ❤️ likho",
    "Share karo 💕",
]

def get_slot():
    now = datetime.now()
    return (now.day * 24 + now.hour)

def get_image_from_pexels():
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing")
        sys.exit(1)
    queries = ["romantic couple", "couple in love", "couple sunset", "love couple", "couple holding hands"]
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": random.choice(queries), "per_page": 15, "orientation": "portrait"}
    res = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params, timeout=20)
    res.raise_for_status()
    photos = res.json().get('photos', [])
    if not photos:
        print("❌ No photo")
        sys.exit(1)
    photo = random.choice(photos)
    url = photo['src']['large']
    print(f"Photo: {url}")
    r = requests.get(url, timeout=20)
    return Image.open(BytesIO(r.content)).convert("RGB")

def make_post_image(shayari):
    base = get_image_from_pexels()
    base = base.resize((1080, 1350))
    overlay = Image.new("RGBA", base.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle([0, 850, 1080, 1350], fill=(0,0,0,140))
    base = base.convert("RGBA")
    base.alpha_composite(overlay)
    draw = ImageDraw.Draw(base)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    except:
        font = ImageFont.load_default()
    y = 900
    for line in shayari.split("\n"):
        bbox = draw.textbbox((0,0), line, font=font)
        w = bbox[2]-bbox[0]
        x = (1080-w)//2
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            draw.text((x+dx, y+dy), line, font=font, fill=(0,0,0,255))
        draw.text((x, y), line, font=font, fill=(255,255,255,255))
        y += 65
    base.convert("RGB").save("post_image.jpg", quality=92)
    return "post_image.jpg"

if __name__ == "__main__":
    if not PAGE_ID or not TOKEN:
        print("❌ FB_PAGE_ID ya FB_TOKEN missing")
        sys.exit(1)
    slot = get_slot()
    shayari = SHAYARI[slot % len(SHAYARI)]
    hashtags = HASHTAG_SETS_PICS[slot % len(HASHTAG_SETS_PICS)]
    cta = CTA_PICS[slot % len(CTA_PICS)]
    caption = f"{shayari}\n\n{cta}\n\n{hashtags}"
    print(f"Shayari: {shayari}")
    print(f"Hashtags: {hashtags}")
    img_path = make_post_image(shayari)
    url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/photos"
    with open(img_path, 'rb') as f:
        res = requests.post(url, data={"access_token": TOKEN, "caption": caption}, files={"source": f}, timeout=60)
    print(f"Status: {res.status_code}")
    print(res.text[:500])
    res.raise_for_status()
    print("✅ PHOTO POST SUCCESS")

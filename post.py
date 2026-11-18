import os, random, requests, io, sys, json, glob
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PAGE_NAME = "Hina Fatima"

def get_images():
    if os.path.exists("images.txt"):
        links = [l.strip() for l in open("images.txt", encoding='utf-8') if l.strip()]
        if links:
            return links
    return [
        "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=1080&auto=format&fit=crop",
    ]

shayari_data = [
    {"roman": "Teri baahon mein aake toh jaise,\nSari kayanat mil gayi ho.", "urdu": "تیری بانہوں میں آ کے تو جیسے،\nساری کائنات مل گئی ہو۔"},
    {"roman": "Teri zulfon ki khushbu mein kho jata hoon,\nTere chehre ko dekhta hoon toh kho jata hoon.", "urdu": "تیری زلفوں کی خوشبو میں کھو جاتا ہوں،\nتیرے چہرے کو دیکھتا ہوں تو کھو جاتا ہوں۔"},
    {"roman": "Tere paas aata hoon toh waqt ruk jata hai,\nTujhe dekh kar dil dhadak jata hai.", "urdu": "تیرے پاس آتا ہوں تو وقت رک جاتا ہے،\nتجھے دیکھ کر دل دھڑک جاتا ہے۔"},
    {"roman": "Ek tera saath chahiye, har khushi se pehle,\nEk teri baahon mein jagah, sari duniya se pehle.", "urdu": "ایک تیرا ساتھ چاہیے، ہر خوشی سے پہلے،\nایک تیری بانہوں میں جگہ، ساری دنیا سے پہلے۔"},
    {"roman": "Tere ishq ki aag mein jalna acha lagta hai,\nTere liye har dard sehna acha lagta hai.", "urdu": "تیرے عشق کی آگ میں جلنا اچھا لگتا ہے،\nتیرے لیے ہر درد سہنا اچھا لگتا ہے۔"},
    {"roman": "Tujhe dekh kar aise khoya main,\nJaise koi nasha kar ke soya main.", "urdu": "تجھے دیکھ کر ایسے کھویا میں،\nجیسے کوئی نشہ کر کے سویا میں۔"},
    {"roman": "Teri baahon mein sukoon milta hai,\nJaise kisi ki dua qabool ho gayi ho.", "urdu": "تیری بانہوں میں سکون ملتا ہے،\nجیسے کسی کی دعا قبول ہو گئی ہو۔"},
    {"roman": "Mera dil tere naam ka ho gaya,\nJaise kisi ne mujhe teri yaadon ka tohfa de diya ho.", "urdu": "میرا دل تیرے نام کا ہو گیا،\nجیسے کسی نے مجھے تیری یادوں کا تحفہ دے دیا ہو۔"},
    {"roman": "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.", "urdu": "تیرے بغیر یہ دل سن سن سا ہے،\nجیسے بغیر بارش کے موسم سونا ہے۔"},
    {"roman": "Tere pyar mein hum toh aise doobe,\nJaise patthar paani mein doobta hai.", "urdu": "تیرے پیار میں ہم تو ایسے ڈوبے،\nجیسے پتھر پانی میں ڈوبتا ہے۔"},
]

def get_videos():
    # Pehle Repo ke andar wali videos check karo - YE SABSE PAKKA HAI
    local = sorted(glob.glob("reel_videos/*.mp4"))
    if local:
        return ["local:" + f for f in local]
    # Agar local nahi hai to test wali Google videos - ye 100% download hoti hain
    if os.path.exists("videos.txt"):
        links = [l.strip() for l in open("videos.txt", encoding='utf-8') if l.strip()]
        if links:
            return links
    return [
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    ]

HASHTAGS = "#UrduShayari #RomanticShayari #LoveQuotes #Ishq #Mohabbat #HinaFatima #Viral #FYP #Trending"

def load_used(fn, default):
    if os.path.exists(fn):
        try: return json.load(open(fn, encoding='utf-8'))
        except: return default
    return default

def save_used(fn, data):
    json.dump(data, open(fn, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def download_font():
    p = "Poppins-Bold.ttf"
    if not os.path.exists(p):
        r = requests.get("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf", timeout=15)
        open(p, 'wb').write(r.content)
    return p

def post_photo():
    font_path = download_font()
    used = load_used("used.json", {"images": [], "shayari": []})
    all_images = get_images()
    avail_img = [u for u in all_images if u not in used["images"]]
    if not avail_img:
        used["images"] = []
        avail_img = all_images
    image_url = random.choice(avail_img)
    avail_sh = [i for i in range(len(shayari_data)) if i not in used["shayari"]]
    if not avail_sh:
        used["shayari"] = []
        avail_sh = list(range(len(shayari_data)))
    sh_idx = random.choice(avail_sh)
    sh = shayari_data[sh_idx]
    try:
        r = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        img = Image.open(io.BytesIO(r.content)).convert("RGBA")
    except:
        img = Image.new('RGBA', (1080, 1350), (20,20,20,255))
    img = img.resize((1080, 1350))
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    for y in range(img.height):
        if y > img.height*0.35:
            a = int(175 * ((y - img.height*0.35)/(img.height*0.65)))
            d.line([(0,y),(img.width,y)], fill=(0,0,0,a))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    font_size = 62
    while font_size > 28:
        f = ImageFont.truetype(font_path, font_size)
        bbox = draw.multiline_textbbox((0,0), sh["roman"], font=f, align="center", spacing=12)
        if bbox[2]-bbox[0] < img.width-120 and bbox[3]-bbox[1] < 550:
            break
        font_size -= 2
    draw.multiline_text((img.width/2, img.height*0.62), sh["roman"], font=f, fill="white", anchor="mm", align="center", spacing=12, stroke_width=3, stroke_fill=(0,0,0,180))
    wm = ImageFont.truetype(font_path, 36)
    draw.text((img.width/2, img.height-70), PAGE_NAME, font=wm, fill=(255,255,255,230), anchor="mm", stroke_width=2, stroke_fill=(0,0,0,150))
    img.convert("RGB").save("post.jpg", quality=92)
    caption = f"{sh['urdu']}\n\nTag someone! ❤\n\n{HASHTAGS}"
    fb_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"
    with open("post.jpg", 'rb') as file:
        res = requests.post(fb_url, data={"caption": caption, "access_token": TOKEN}, files={'source': file}, timeout=30)
    print(res.text)
    res.raise_for_status()
    used["images"].append(image_url)
    used["shayari"].append(sh_idx)
    used["images"] = used["images"][-5000:]
    save_used("used.json", used)
    print("✅ PHOTO SUCCESS")

def post_reel():
    used_reels = load_used("used_reels.json", {"videos": []})
    used = load_used("used.json", {"images": [], "shayari": []})
    all_videos = get_videos()
    avail_v = [v for v in all_videos if v not in used_reels["videos"]]
    if not avail_v:
        used_reels["videos"] = []
        avail_v = all_videos
    video_url = random.choice(avail_v)
    avail_sh = [i for i in range(len(shayari_data)) if i not in used["shayari"]]
    if not avail_sh:
        used["shayari"] = []
        avail_sh = list(range(len(shayari_data)))
    sh_idx = random.choice(avail_sh)
    sh = shayari_data[sh_idx]
    print(f"Selected Reel: {video_url}")
    # Local video hai to direct copy karo, warna download karo
    if video_url.startswith("local:"):
        import shutil
        shutil.copy(video_url[6:], "reel.mp4")
        size = os.path.getsize("reel.mp4")
        print(f"Local Video size: {size} bytes")
    else:
        print(f"Downloading Reel: {video_url}")
        vr = requests.get(video_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=90)
        open("reel.mp4", 'wb').write(vr.content)
        size = len(vr.content)
        print(f"Video size: {size} bytes")
        if size < 100000:
            print("Video download fail, skipping")
            used_reels["videos"].append(video_url)
            save_used("used_reels.json", used_reels)
            return
    caption = f"{sh['urdu']}\n\nTag someone! ❤\n\n{HASHTAGS} #Reels"
    print("Step 1: Start Upload...")
    start_url = f"https://graph.facebook.com/v21.0/{PAGE_ID}/video_reels"
    r1 = requests.post(start_url, data={"upload_phase": "start", "access_token": TOKEN}, timeout=30)
    print(r1.text)
    r1.raise_for_status()
    data = r1.json()
    video_id = data["video_id"]
    upload_url = data["upload_url"]
    print("Step 2: Uploading Video File...")
    with open("reel.mp4", 'rb') as f:
        video_bytes = f.read()
    headers = {"Authorization": f"OAuth {TOKEN}", "file_offset": "0", "Content-Type": "application/octet-stream"}
    r2 = requests.post(upload_url, headers=headers, data=video_bytes, timeout=180)
    print(f"Upload done: {r2.status_code} {r2.text[:800]}")
    r2.raise_for_status()
    print("Step 3: Finish & Publish...")
    r3 = requests.post(start_url, data={"upload_phase": "finish", "video_id": video_id, "caption": caption, "access_token": TOKEN, "share_to_feed": "true"}, timeout=30)
    print(r3.text)
    r3.raise_for_status()
    used_reels["videos"].append(video_url)
    used["shayari"].append(sh_idx)
    save_used("used_reels.json", used_reels)
    save_used("used.json", used)
    print("✅ REEL SUCCESS")

if __name__ == "__main__":
    manual = os.environ.get('POST_TYPE')
    if manual in ["photo", "reel"]:
        choice = manual
    else:
        choice = random.choice(["photo", "reel"])
    print(f"Choice: {choice}")
    if choice == "reel":
        post_reel()
    else:
        post_photo()

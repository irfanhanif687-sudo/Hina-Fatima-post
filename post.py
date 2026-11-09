import os
import random
import requests
import io
from PIL import Image, ImageEnhance

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Funny Captions (Yeh picture ke neeche Facebook par likhi jayengi)
captions = [
    "Ammi ne pakka yeh scene nahi dekhna chahiye tha 😂",
    "Kya acting hai waise! 🔥",
    "Yeh expression dekh ke toh meri hasi nahi ruk rahi 🤣",
    "Guys, yeh kaunsa drama hai? 😅",
    "Koi batao yeh actress kaun hai? 🤔",
    "Iska makeup toh kamaal ka hai 💄✨",
    "Bhai yeh actress toh har drama mein same acting karti hai 🤦‍♂️",
    "Ek episode dekh ke hi pata chal gaya ending kya hogi 😭",
    "Tag your drama lover friend! 👇"
]

# 35+ Viral Hashtags
HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial #DramaQueen 
#Fun #Laugh #Comedy #MemePage #DramaMeme #ViralMemes #ExplorePage #FYP 
"""

def get_desi_meme():
    subreddits = ["pakistanimemes", "desimemes", "chutyapa"]
    sub = random.choice(subreddits)
    url = f"https://meme-api.com/gimme/{sub}"
    
    print(f"Fetching meme from r/{sub}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('nsfw', False):
            return None
            
        meme_url = data.get('url')
        if meme_url and meme_url.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Found Meme: {meme_url}")
            return meme_url
        return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def process_and_post():
    image_url = get_desi_meme()
    if not image_url:
        print("❌ Meme nahi mila, agli baar try karega.")
        return
        
    try:
        # 1. Image Download
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        img_response = requests.get(image_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        
        # ✅ MODIFY STEP: Aggressive Cropping (Purane page ka UI hatane ke liye)
        width, height = img.size
        
        # Hum kinaron se 8% hissa kaat rahe hain (taake purana watermark/UI hat jaye)
        left = width * 0.05
        top = height * 0.05
        right = width * 0.95
        bottom = height * 0.88 # Neeche se zyada kaat rahe hain taake "Muhammad Ali" wala hissa hat jaye
        
        img = img.crop((left, top, right, bottom))

        # Quality Enhance
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)

        image_path = "clean_meme.jpg"
        img.save(image_path, format="JPEG", quality=100)

        # 2. Post to Facebook
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        
        random_caption = random.choice(captions)
        caption = f"{random_caption}\n\nFollow for more! 👇\n{HASHTAGS}"
        
        payload = {"caption": caption, "access_token": TOKEN}
        
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            fb_response = requests.post(fb_url, data=payload, files=files, timeout=20)
            
        fb_response.raise_for_status()
        print(f"✅ Post Success! ID: {fb_response.json().get('id')}")
        
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    print("Starting Copy, Crop & Post System...")
    process_and_post()

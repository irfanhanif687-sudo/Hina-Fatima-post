import os
import random
import requests
import io
import re
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Funny Lines
funny_lines = [
    "Ammi ne pakka yeh scene nahi dekhna chahiye tha",
    "Kya acting hai waise!", 
    "Yeh expression dekh ke toh meri hasi nahi ruk rahi",
    "Guys, yeh kaunsa drama hai?", 
    "Mujhe toh bas yeh jodi pasand hai",
    "Koi batao yeh actress kaun hai?", 
    "Aaj kal ke dramas mein bas rona hi rona hai",
    "Iska makeup toh kamaal ka hai", 
    "Iska expression toh ekdum Ammi ne daant di hai wala hai",
    "Mashallah, kitni pyari lag rahi hain!"
]

# 35+ Viral Hashtags
HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial #DramaQueen 
#Fun #Laugh #Comedy #MemePage #DramaMeme #ViralMemes #ExplorePage #FYP 
"""

def get_desi_meme():
    # ✅ Yeh API kabhi block nahi hoti aur direct Pakistani/Desi memes deti hai
    subreddits = ["pakistanimemes", "desimemes", "chutyapa", "pakistan"]
    sub = random.choice(subreddits)
    url = f"https://meme-api.com/gimme/{sub}"
    
    print(f"Fetching direct meme from r/{sub}...")
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
        
        # ✅ MODIFY STEP: Crop Edges (Instagram/Reddit watermark hatane ke liye)
        width, height = img.size
        left = width * 0.05
        top = height * 0.05
        right = width * 0.95
        bottom = height * 0.90 # Neeche se zyada kaat rahe hain taake UI hat jaye
        
        img = img.crop((left, top, right, bottom))

        # Quality Enhance
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)

        draw = ImageDraw.Draw(img)
        line = random.choice(funny_lines)
        line_text = re.sub(r'[^\w\s\?\.,!]', '', line).strip()

        # Text Auto-Fit
        font_size = 75
        max_width = img.width - 40
        while font_size > 10:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()
                break
            bbox = draw.textbbox((0, 0), line_text, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                break
            font_size -= 2

        bbox = draw.textbbox((0, 0), line_text, font=font)
        x = (img.width - (bbox[2] - bbox[0])) / 2
        y = img.height - 120
        
        # Text Outline
        for adj in range(-3, 4):
            draw.text((x+adj, y), line_text, font=font, fill="black")
            draw.text((x, y+adj), line_text, font=font, fill="black")
        draw.text((x, y), line_text, font=font, fill="white")
        
        image_path = "desi_meme.jpg"
        img.save(image_path, format="JPEG", quality=100)

        # Post to Facebook
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        caption = f"Tag your drama lover friend! 😂🔥\n\nAapko yeh meme kaisa laga? Comment below! 👇\n\n{HASHTAGS}"
        
        payload = {"caption": caption, "access_token": TOKEN}
        
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            fb_response = requests.post(fb_url, data=payload, files=files, timeout=20)
            
        fb_response.raise_for_status()
        print(f"✅ Post Success! ID: {fb_response.json().get('id')}")
        
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == "__main__":
    print("Starting No-Block Meme System...")
    process_and_post()

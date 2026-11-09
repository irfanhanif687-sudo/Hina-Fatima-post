import os
import random
import requests
import io
import re
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from duckduckgo_search import DDGS

# GitHub Secrets se IDs uthana
PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# ✅ Backup Image (Agar internet search fail ho jaye toh yeh use hogi)
FALLBACK_IMAGE_URL = "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop"

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
    "Mashallah, kitni pyari lag rahi hain!",
    "Bhai yeh actress toh har drama mein same acting karti hai",
    "Is drama ne toh hadd kar di hai yaar", 
    "Ek episode dekh ke hi pata chal gaya ending kya hogi"
]

HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial #DramaQueen 
#Fun #Laugh #Comedy #MemePage #DramaMeme #ViralMemes #ExplorePage #FYP 
#ForYouPage #Relatable #DesiMemes #DramaLovers #PakistanZindabad 
"""

def get_real_image():
    # Browser ki tarah DuckDuckGo se search karo
    print("Browsing DuckDuckGo for real Pakistani drama pictures...")
    try:
        results = DDGS().images(
            keywords="pakistani drama funny scene",
            region="wt-wt",
            safesearch="moderate",
            max_results=10
        )
        
        valid_urls = [res['image'] for res in results if res.get('image') and res['image'].lower().endswith(('.jpg', '.png', '.jpeg'))]
        
        if valid_urls:
            selected_url = random.choice(valid_urls)
            print(f"Found Real Picture: {selected_url}")
            return selected_url
    except Exception as e:
        print(f"❌ Search failed: {e}")
    
    print("⚠️ Using Backup Image to prevent failure...")
    return FALLBACK_IMAGE_URL

def process_and_post():
    image_url = get_real_image()
    
    try:
        # Image Download karo (Browser headers ke sath)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        img_response = requests.get(image_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        
        # Verify karo ke file sahi image hai
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        
        # Quality Enhance
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)
        
        # Kinaron se crop karo watermark hatane ke liye
        width, height = img.size
        img = img.crop((5, 5, width - 5, height - 5))

        draw = ImageDraw.Draw(img)
        line = random.choice(funny_lines)
        line_text = re.sub(r'[^\w\s\?\.,!]', '', line).strip()

        # Auto-Fit Text
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
        
        # Text Outline (Black background for white text)
        for adj in range(-3, 4):
            draw.text((x+adj, y), line_text, font=font, fill="black")
            draw.text((x, y+adj), line_text, font=font, fill="black")
        draw.text((x, y), line_text, font=font, fill="white")
        
        print(f"Added Comment: {line_text}")
        
        image_path = "final_drama_meme.jpg"
        img.save(image_path, format="JPEG", quality=100)

        # Facebook par Post
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
    print("Starting Real Web Search Meme System...")
    process_and_post()

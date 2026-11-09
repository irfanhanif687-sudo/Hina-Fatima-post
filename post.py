import os
import random
import requests
import io
import sys
from PIL import Image, ImageEnhance

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# ✅ Hashtags
HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial 
"""

# ✅ SMART FILTER: Yeh words title mein hone chahiye tabhi post hoga
keywords = [
    "drama", "hania", "sajal", "mahira", "wahaj", "fawad", "acting", 
    "serial", "scene", "episode", "actress", "actor", "jaan nisar", 
    "kabhi main kabhi tum", "geo", "hum", "ary", "meme", "funny"
]

def get_filtered_meme():
    subreddits = ["pakistanidrama", "pakistanimemes", "desimemes", "bollywoodmemes"]
    
    # 5 dafa koshish karega achi picture dhoondne ke liye
    for _ in range(5): 
        sub = random.choice(subreddits)
        url = f"https://meme-api.com/gimme/{sub}/50" # Ek sath 50 memes layega
        
        print(f"Fetching 50 memes from r/{sub} to find the right one...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'memes' in data:
                random.shuffle(data['memes']) # Shuffle karega taake random aaye
                for meme in data['memes']:
                    title = meme.get('title', '').lower()
                    meme_url = meme.get('url', '')
                    nsfw = meme.get('nsfw', False)
                    
                    if nsfw: continue # Gandi cheezein skip
                    if not meme_url.lower().endswith(('.jpg', '.jpeg', '.png')): continue
                    
                    # ✅ Check karo ke title mein drama ka word hai ya nahi
                    if any(kw in title for kw in keywords):
                        print(f"✅ Found relevant meme! Title: {title}")
                        return meme_url
                        
        except Exception as e:
            print(f"⚠️ API Error on r/{sub}: {e}")
            
    return None

def process_and_post():
    image_url = get_filtered_meme()
    
    if not image_url:
        print("❌ Aaj koi achi drama meme nahi mili. Is waqt post skip kar rahe hain (Error nahi aayega).")
        sys.exit(0) # Exit without error so GitHub doesn't show Red Cross

    try:
        # 1. Picture Download karo
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        img_response = requests.get(image_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        
        # ✅ MODIFY STEP: Crop karo taake Instagram/Reddit ka UI hat jaye
        width, height = img.size
        img = img.crop((width * 0.05, height * 0.05, width * 0.95, height * 0.85))
        
        # Quality Enhance
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)

        image_path = "auto_meme.jpg"
        img.save(image_path, format="JPEG", quality=100)

        # 2. Facebook par Post karo
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        caption = f"Tag your drama lover friend! 😂🔥\n\nAapko yeh meme kaisa laga? Comment below! 👇\n\n{HASHTAGS}"
        
        payload = {"caption": caption, "access_token": TOKEN}
        
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            fb_response = requests.post(fb_url, data=payload, files=files, timeout=20)
            
        fb_response.raise_for_status()
        print(f"✅ POST SUCCESS! ID: {fb_response.json().get('id')}")
        
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_and_post()

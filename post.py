import os
import random
import requests
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# GitHub Secrets se IDs uthana
PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Unlimited Recent Drama Memes ke liye Subreddits
subreddits = ["pakistanimemes", "indianmemes", "bollywoodmemes", "pakistanidrama", "desimemes"]

# ✅ 35+ Viral Hashtags (Reach aur Followers barhane ke liye)
HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial #DramaQueen 
#Fun #Laugh #Comedy #MemePage #DramaMeme #ViralMemes #ExplorePage #FYP 
#ForYouPage #Relatable #DesiMemes #DramaLovers #PakistanZindabad #IndianTV 
"""

def get_high_quality_meme():
    sub = random.choice(subreddits)
    url = f"https://meme-api.com/gimme/{sub}"
    
    print(f"Fetching high-quality meme from r/{sub}...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # NSFW (gandi) memes filter karo
        if data.get('nsfw', False) or data.get('spoiler', False):
            return None, None
            
        meme_url = data.get('url')
        title = data.get('title', 'Drama Lovers!')
        
        # Sirf valid static images allow karo (GIFs aur videos nahi)
        clean_url = meme_url.lower().split('?')[0] if meme_url else ""
        if clean_url.endswith(('.jpg', '.jpeg', '.png')):
            print(f"Found Meme: {meme_url}")
            return meme_url, title
        return None, None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None, None

def process_and_enhance_image(image_url, title):
    try:
        # 1. Image download karo
        img_response = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        img_response.raise_for_status()
        
        img = Image.open(io.BytesIO(img_response.content)).convert("RGB")
        
        # ✅ Quality Check: 800px se choti picture reject karo
        if img.width < 800:
            print("❌ Picture ki quality kam hai (blur), skip kar rahe hain.")
            return None
            
        # ✅ Hide Source (Crop Edges): Kinaron se 20 pixel kaat do taake watermark (jaise @username) hat jaye
        width, height = img.size
        img = img.crop((20, 20, width - 20, height - 20))
        
        # ✅ Quality Enhance: Picture ko thora sharp aur colorful karo
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2) 
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1) 

        draw = ImageDraw.Draw(img)
        
        # 2. Font set karo
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        except:
            font = ImageFont.load_default()

        # ✅ Text Wrap System: Agar title lamba ho toh multi-line ho jayega
        wrapped_title = textwrap.fill(title, width=40)
        
        # Banner ki height calculate karo text ke hisaab se
        bbox = draw.multiline_textbbox((0, 0), wrapped_title, font=font, align="center")
        text_height = bbox[3] - bbox[1]
        banner_height = text_height + 40
        
        # Top par Black Banner banao (Isse top ka watermark bhi chup jata hai)
        draw.rectangle([(0, 0), (img.width, banner_height)], fill=(0, 0, 0))
        
        # Text ko center align karo
        text_width = bbox[2] - bbox[0]
        x = (img.width - text_width) / 2
        y = 20
        
        draw.multiline_text((x, y), wrapped_title, font=font, fill="white", align="center")
        
        image_path = "premium_meme.jpg"
        # 100% High Quality par save karo
        img.save(image_path, format="JPEG", quality=100)
        return image_path
    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return None

def post_to_facebook(image_path):
    fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    
    # Engagement Hook (Log comment karenge toh reach barhegi)
    caption = f"Tag your drama lover friend! 😂🔥\n\nAapko yeh meme kaisa laga? Comment below! 👇\n\n{HASHTAGS}"
    
    payload = {
        "caption": caption,
        "access_token": TOKEN
    }

    try:
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            response = requests.post(fb_url, data=payload, files=files, timeout=20)
            
        response.raise_for_status()
        print(f"✅ Post Success! ID: {response.json().get('id')}")
    except Exception as e:
        print(f"❌ Facebook Post Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

if __name__ == "__main__":
    print("Starting Premium Meme Generation...")
    
    success = False
    # 10 dafa try karega jab tak perfect HD picture na mil jaye
    for _ in range(10):
        meme_url, title = get_high_quality_meme()
        if meme_url:
            final_img = process_and_enhance_image(meme_url, title)
            if final_img:
                print("Posting to Facebook...")
                post_to_facebook(final_img)
                success = True
                break
    
    if not success:
        print("❌ 10 koshishon ke baad bhi koi HD meme nahi mila. Agli baar try hoga.")

import os
import random
import requests
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

try:
    from duckduckgo_search import DDGS
    HAS_DDGS = True
except ImportError:
    HAS_DDGS = False
    print("DDGS library nahi mili, backup mode use hoga.")

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Fallback Images (Agar search fail ho jaye)
FALLBACK_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/0/0a/Hania_Aamir_at_Hum_Style_Awards_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f5/Sajal_Aly_at_Hum_Style_Awards_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0b/Mahira_Khan_at_Lux_Style_Awards_%282%29_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/8/8d/Yumna_Zaidi_at_Hum_Style_Awards_%28cropped%29.jpg"
]

# Emojis ke bina Funny Lines (Taake font mein error na aaye)
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

def get_image_from_search():
    if not HAS_DDGS:
        return None
    print("Try 1: Searching internet for latest memes...")
    try:
        results = DDGS().images(
            keywords="latest pakistani drama funny memes",
            region="wt-wt",
            safesearch="moderate",
            max_results=15
        )
        valid_urls = [res['image'] for res in results if res.get('image') and res['image'].lower().endswith(('.jpg', '.png', '.jpeg'))]
        if valid_urls:
            selected_url = random.choice(valid_urls)
            print(f"Found: {selected_url}")
            return selected_url
    except Exception as e:
        print(f"Search failed: {e}")
    return None

def process_and_post(image_url=None):
    img = None
    
    # Agar search se URL mila hai toh download karo
    if image_url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(image_url, headers=headers, timeout=15)
            res.raise_for_status()
            img = Image.open(io.BytesIO(res.content)).convert("RGB")
        except Exception as e:
            print(f"Download failed: {e}")
            img = None # Download fail ho toh neeche fallback chalega

    # Fallback 1: Agar search/download fail hua toh Wikipedia se uthao
    if not img:
        print("Try 2 (Backup): Downloading fallback actress image...")
        try:
            url = random.choice(FALLBACK_IMAGES)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers=headers, timeout=15)
            res.raise_for_status()
            img = Image.open(io.BytesIO(res.content)).convert("RGB")
        except Exception as e:
            print(f"Fallback download failed: {e}")
            return # Agar yeh bhi fail ho toh script ruk jayegi

    # Image Process (Crop & Enhance)
    width, height = img.size
    img = img.crop((5, 5, width - 5, height - 5)) # Watermark hide
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    # Text Add karo
    draw = ImageDraw.Draw(img)
    line = random.choice(funny_lines)
    
    font_size = 65
    max_width = img.width - 40
    while font_size > 10:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
            break
        bbox = draw.textbbox((0, 0), line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            break
        font_size -= 2

    bbox = draw.textbbox((0, 0), line, font=font)
    x = (img.width - (bbox[2] - bbox[0])) / 2
    y = img.height - 120
    
    for adj in range(-3, 4):
        draw.text((x+adj, y), line, font=font, fill="black")
        draw.text((x, y+adj), line, font=font, fill="black")
    draw.text((x, y), line, font=font, fill="white")

    image_path = "final_meme.jpg"
    img.save(image_path, format="JPEG", quality=100)

    # Post to Facebook
    print("Uploading to Facebook...")
    fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    caption = f"Tag your drama lover friend! 😂🔥\n\nAapko yeh meme kaisa laga? Comment below! 👇\n\n{HASHTAGS}"
    
    try:
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            response = requests.post(fb_url, data={"caption": caption, "access_token": TOKEN}, files=files, timeout=20)
        response.raise_for_status()
        print(f"✅ Post Success! ID: {response.json().get('id')}")
    except Exception as e:
        print(f"❌ Facebook Post Error: {e}")

if __name__ == "__main__":
    print("Starting Automatic Meme System...")
    img_url = get_image_from_search()
    process_and_post(img_url)

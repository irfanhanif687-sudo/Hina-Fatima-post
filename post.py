import os
import random
import requests
import io
import sys
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

PAGE_NAME = "Hina Fatima"

# ✅ High Quality Aesthetic Desi Pictures
aesthetic_images = [
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop"
]

# ✅ Bold & Romantic Urdu Shayari
urdu_shayari = [
    "محبت میں ہار جانا بھی ایک جیت ہے،\nکہ دل کی دنیا میں کوئی شکست نہیں ہوتی۔",
    "تیرے بغیر یہ دل ویران سا لگتا ہے،\nجیسے بارش کے بغیر موسم سوکھا سا لگتا ہے۔",
    "تم سے مل کر لگا جیسے،\nزندگی مکمل ہو گئی ہے۔",
    "ہم نے تو دل سے چاہا تھا تجھے،\nپر تو نے تو آنکھوں سے بھی نہ دیکھا۔",
    "دل کی بات لبوں تک لاتی نہیں،\nکیونکہ ہم تجھے پریشان نہیں کرنا چاہتے۔",
    "تیری مسکراہٹ پر سب کچھ قربان،\nتو بس مسکرا دے تو جنت مل جائے۔",
    "میرے خوابوں میں ہر رات آتا ہے تو،\nجیسے کوئی خوشبو فضا میں بکھرتی ہے۔",
    "تیرے نام سے ہی میری صبح ہوتی ہے،\nاور تیری یاد سے ہی میری رات ڈھلتی ہے۔",
    "محبت کی کوئی زبان نہیں ہوتی،\nبس ایک احساس ہوتا ہے جو دل سمجھ لیتا ہے۔",
    "اگر زندگی میں دوبارہ ملے،\nتو شاید تب بھی تجھے ہی چاہوں گا۔",
    "تیرے بغیر یہ دل سن سن سا ہے،\nجیسے بغیر بارش کے موسم سونا ہے۔",
    "میں نے تجھے دل سے چاہا،\nنہ جانے تیری رضا کیا ہے۔"
]

HASHTAGS = "#UrduShayari #UrduPoetry #UrduQuotes #SadShayari #RomanticShayari #LoveQuotes #Aesthetic #Trending #Viral #FYP #HinaFatima"

def download_urdu_font():
    # ✅ Font download function: Yeh direct Google Fonts se download karega
    font_path = "NotoNastaliqUrdu-Regular.ttf"
    if not os.path.exists(font_path):
        print("Downloading Urdu Font...")
        url = "https://github.com/google/fonts/raw/main/ofl/notonastaliqurdu/NotoNastaliqUrdu-Regular.ttf"
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(font_path, 'wb') as f:
                f.write(r.content)
            print("✅ Font downloaded successfully.")
        except Exception as e:
            print(f"❌ Font download failed: {e}")
    return font_path

def get_urdu_font(font_size):
    font_path = download_urdu_font()
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"⚠️ Error loading font: {e}")
        return ImageFont.load_default()

def process_and_post():
    image_url = random.choice(aesthetic_images)
    
    try:
        # 1. Image Download
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=10)
            img_response.raise_for_status()
            img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
        except Exception:
            img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255)) 
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 130))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 2. Page Name (Left Top Corner)
        try:
            wm_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            wm_font = ImageFont.load_default()
            
        wm_bbox = draw.textbbox((0, 0), PAGE_NAME, font=wm_font)
        wm_width = wm_bbox[2] - wm_bbox[0]
        wm_height = wm_bbox[3] - wm_bbox[1]
        
        wm_x, wm_y, padding = 30, 30, 15
        draw.rectangle([(wm_x - padding, wm_y - padding), (wm_x + wm_width + padding, wm_y + wm_height + padding)], fill=(0, 0, 0, 180))
        draw.text((wm_x, wm_y), PAGE_NAME, font=wm_font, fill="white")
        
        # 3. Urdu Shayari Reshaping
        shairi = random.choice(urdu_shayari)
        reshaped_text = arabic_reshaper.reshape(shairi)
        bidi_text = get_display(reshaped_text)
        
        # 4. Text Auto-Fit
        font_size = 75 
        max_width = img.width - 100   
        max_height = img.height - 300
        
        while font_size > 20:
            urdu_font = get_urdu_font(font_size)
            bbox = draw.multiline_textbbox((0, 0), bidi_text, font=urdu_font, align="center")
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width < max_width and text_height < max_height:
                break
            font_size -= 2 

        x_center = img.width / 2
        y_center = img.height / 2
        
        # 5. Draw Shayari (Center with Outline)
        draw.multiline_text(
            (x_center, y_center), 
            bidi_text, 
            font=urdu_font, 
            fill="white", 
            anchor="mm", 
            align="center",
            stroke_width=3,
            stroke_fill="black"
        )
        
        image_path = "urdu_shairi_post.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        # 6. Facebook Post
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        caption = f"{shairi}\n\nFollow for more beautiful shayari! ❤️\n\n{HASHTAGS}"
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

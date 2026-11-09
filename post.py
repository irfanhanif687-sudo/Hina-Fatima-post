import os
import random
import requests
import io
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# ✅ Page Name (Left Corner ke liye)
PAGE_NAME = "Hina Fatima"

# ✅ High-Quality Romantic & Bold Pictures
romantic_images = [
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop"
]

# ✅ Bold & Romantic Shairis
shairi_list = [
    "Tumhari yaad mein hum roz mara karte hain,\nTumhe bhoolane ki koshish mein khud ko hi bhula dete hain.",
    "Kuch is tarah se teri zindagi mein shamil hoon,\nKe khud ko dhoondhne nikloon toh tujh mein nikal aata hoon.",
    "Mohabbat mein har gham ko gale lagana padta hai,\nKabhi khud ko bhulana, kabhi unko manana padta hai.",
    "Tere bina yeh dil udaas rehta hai,\nJaise phoolon mein khushbu ki talaash rehti hai.",
    "Dil tutne ki aawaz nahi hoti,\nBas ek dard hota hai jo bayan nahi hota.",
    "Meri duaaon mein tu hai,\nMeri raaton mein tu hai,\nMeri har saans mein tu hai.",
    "Mujhe teri aadat si ho gayi hai,\nTere bina jeena mushkil si ho gayi hai.",
    "Tere naam ki khushbu mere dil mein basi hai,\nJaise kisi ne phoolon ki khushbu chura li ho.",
    "Tumhari aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan milta hai.",
    "Mera har din teri yaad se shuru hota hai,\nAur teri yaad par khatam ho jata hai.",
    "Agar zindagi mein dobara milo,\nToh shayad tab bhi tumhe hi chahunga.",
    "Mujhe teri aadat hai,\nTere bina kya guzara hoga.",
    "Teri muskurahat pe sab kuch qurban,\nTu bas muskura de toh jannat mil jaye.",
    "Mujhe teri baahon mein sukoon milta hai,\nJaise musafir ko apna ghar mil jaye.",
    "Mera dil tere naam ka ho gaya,\nJaise kisi ne mujhe teri yaadon ka tohfa de diya ho.",
    "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.",
    "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai."
]

HASHTAGS = "#Shairi #UrduPoetry #LoveQuotes #SadShayari #Zindagi #DilKiBaat #Aesthetic #Trending #Viral #FYP #HinaFatima #DeepLines #Mohabbat #Romantic"

def process_and_post():
    image_url = random.choice(romantic_images)
    
    try:
        # 1. Image Download
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=10)
            img_response.raise_for_status()
            img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
        except Exception:
            img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255)) 
        
        # Black Overlay taake text parhne mein asani ho
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 120))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # ✅ 2. Page Name (Left Corner - Attractive Box Style)
        try:
            wm_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            wm_font = ImageFont.load_default()
            
        wm_bbox = draw.textbbox((0, 0), PAGE_NAME, font=wm_font)
        wm_width = wm_bbox[2] - wm_bbox[0]
        wm_height = wm_bbox[3] - wm_bbox[1]
        
        # Left position with padding
        wm_x = 30
        wm_y = 30
        padding = 15
        
        # Semi-transparent black box
        draw.rectangle(
            [(wm_x - padding, wm_y - padding), (wm_x + wm_width + padding, wm_y + wm_height + padding)],
            fill=(0, 0, 0, 160)
        )
        
        # Page Name
        draw.text((wm_x, wm_y), PAGE_NAME, font=wm_font, fill="white")
        
        # ✅ 3. Shairi Text Logic (Perfect Fit)
        shairi = random.choice(shairi_list)
        # Text wrap width 26 rakhi hai taake line zyada lambi na ho
        wrapped_shairi = textwrap.fill(shairi, width=26)
        
        font_size = 65
        max_width = img.width - 80   
        max_height = img.height - 300
        
        # Loop chalta rahega jab tak text picture mein fit na ho jaye
        while font_size > 15:
            try:
                shairi_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                shairi_font = ImageFont.load_default()
                break
            
            bbox = draw.multiline_textbbox((0, 0), wrapped_shairi, font=shairi_font, align="center")
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            if text_width < max_width and text_height < max_height:
                break
            font_size -= 2 

        x_center = img.width / 2
        y_center = img.height / 2
        
        # ✅ 4. Draw Shairi in Center
        draw.multiline_text(
            (x_center, y_center), 
            wrapped_shairi, 
            font=shairi_font, 
            fill="white", 
            anchor="mm", 
            align="center",
            stroke_width=4,
            stroke_fill="black"
        )
        
        image_path = "shairi_post.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        # 5. Facebook par Post
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        caption = f"{shairi}\n\nFollow for more beautiful shairi! ❤️\n\n{HASHTAGS}"
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

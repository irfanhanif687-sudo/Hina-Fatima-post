import os
import random
import requests
import io
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# ✅ Aapke Page ka Naam (Watermark ke liye)
PAGE_NAME = "Hina Fatima"

# ✅ Unlimited High-Quality Aesthetic Pictures (Unsplash - Direct HD)
male_images = [
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?q=80&w=1080&auto=format&fit=crop"
]

female_images = [
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop"
]

# ✅ 50+ Unlimited Shairis
shairi_list = [
    "Tumhari yaad mein hum roz mara karte hain,\nTumhe bhoolane ki koshish mein khud ko hi bhula dete hain.",
    "Kuch is tarah se teri zindagi mein shamil hoon,\nKe khud ko dhoondhne nikloon toh tujh mein nikal aata hoon.",
    "Dard-e-dil ki dawa kya hai?\nIshq ka haal suna kya hai?",
    "Woh aaye toh mera dil khush ho gaya,\nJaise kisi ne phoolon ka guldasta bhej diya ho.",
    "Mohabbat mein har gham ko gale lagana padta hai,\nKabhi khud ko bhulana, kabhi unko manana padta hai.",
    "Aankhon mein aansu hain, labon pe hansi hai,\nYeh zindagi bhi kya ajab kahani hai.",
    "Tujhse milne ki khushi mein,\nHum apne saare gham bhula dete hain.",
    "Meri khamoshi ko meri baat mat samajhna,\nYeh toh dil ki aawaz hai jo koi sun nahi sakta.",
    "Zindagi mein sab kuch milta hai,\nBas woh ek cheez nahi milti jo hum chahte hain.",
    "Tere bina yeh dil udaas rehta hai,\nJaise phoolon mein khushbu ki talaash rehti hai.",
    "Kisi ko chahna gunah toh nahi,\nPar kisi ka ho jana aasan bhi nahi.",
    "Waqt ke saath har zakham bhar jata hai,\nPar kuch nishaan dil mein hamesha rehte hain.",
    "Hum toh unke liye duniya bhula baithe,\nAur woh humein duniya ke liye bhula gaye.",
    "Dil tutne ki aawaz nahi hoti,\nBas ek dard hota hai jo bayan nahi hota.",
    "Tumhe dekh kar lagta hai,\nJaise khwabon ki duniya mein aa gaya hoon.",
    "Meri duaaon mein tu hai,\nMeri raaton mein tu hai,\nMeri har saans mein tu hai.",
    "Ishq mein humne woh khoya hai,\nJo shayad kabhi mila hi nahi tha.",
    "Yeh raat, yeh tanhai, aur yeh chand,\nSab keh rahe hain ke tu door hai.",
    "Mujhe teri aadat si ho gayi hai,\nTere bina jeena mushkil si ho gayi hai.",
    "Kabhi kabhi lagta hai,\nKe main khud se door ho gaya hoon.",
    "Tere naam ki khushbu mere dil mein basi hai,\nJaise kisi ne phoolon ki khushbu chura li ho.",
    "Dil ki baat labon tak aati nahi,\nKyunke hum unko pareshan nahi karna chahte.",
    "Tumhari aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan milta hai.",
    "Mera har din teri yaad se shuru hota hai,\nAur teri yaad par khatam ho jata hai.",
    "Kisi ne kya khoob kaha hai,\nKe mohabbat ka matlab sirf dena hota hai, lena nahi.",
    "Tere bina yeh zindagi adhoori si lagti hai,\nJaise koi kahani bina ending ke.",
    "Mujhe dard bhi teri hi yaad dilata hai,\nAur sukoon bhi teri hi yaad se milta hai.",
    "Agar zindagi mein dobara milo,\nToh shayad tab bhi tumhe hi chahunga.",
    "Woh kehte hain ke main badal gaya hoon,\nPar sach toh yeh hai ke main unke liye hi ruk gaya hoon.",
    "Tere bina jo guzri hai raatein,\nUn raaton ka koi hisaab nahi."
]

# ✅ Viral Hashtags
HASHTAGS = "#Shairi #UrduPoetry #LoveQuotes #SadShayari #Zindagi #DilKiBaat #Aesthetic #Trending #Viral #FYP #HinaFatima #DeepLines #Mohabbat #Dosti"

def process_and_post():
    all_images = male_images + female_images
    image_url = random.choice(all_images)
    
    try:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=10)
            img_response.raise_for_status()
            img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
        except Exception:
            img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255)) 
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 120))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 1. Page Name (Top-Right)
        try:
            wm_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        except:
            wm_font = ImageFont.load_default()
            
        wm_bbox = draw.textbbox((0, 0), PAGE_NAME, font=wm_font)
        wm_x = img.width - (wm_bbox[2] - wm_bbox[0]) - 30
        wm_y = 30
        
        for adj in range(-2, 3):
            draw.text((wm_x+adj, wm_y), PAGE_NAME, font=wm_font, fill="black")
            draw.text((wm_x, wm_y+adj), PAGE_NAME, font=wm_font, fill="black")
        draw.text((wm_x, wm_y), PAGE_NAME, font=wm_font, fill="white")
        
        # 2. Shairi Text
        shairi = random.choice(shairi_list)
        wrapped_shairi = textwrap.fill(shairi, width=30)
        
        font_size = 65
        while font_size > 20:
            try:
                shairi_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                shairi_font = ImageFont.load_default()
                break
            
            bbox = draw.multiline_textbbox((0, 0), wrapped_shairi, font=shairi_font, align="center")
            text_height = bbox[3] - bbox[1]
            if text_height < img.height - 200:
                break
            font_size -= 2

        # ✅ FIX: Perfect Centering (Anchor="mm" ka use kiya hai taake lafz na katen)
        x_center = img.width / 2
        y_center = img.height / 2
        
        # Text Outline & Main Text
        for adj in range(-3, 4):
            draw.multiline_text((x_center+adj, y_center), wrapped_shairi, font=shairi_font, fill="black", anchor="mm", align="center")
            draw.multiline_text((x_center, y_center+adj), wrapped_shairi, font=shairi_font, fill="black", anchor="mm", align="center")
        draw.multiline_text((x_center, y_center), wrapped_shairi, font=shairi_font, fill="white", anchor="mm", align="center")
        
        image_path = "shairi_post.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        # 3. Facebook par Post
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

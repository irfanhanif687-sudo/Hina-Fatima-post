import os
import random
import requests
import io
import sys
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PAGE_NAME = "Hina Fatima"

def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
    font_path = "Poppins-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading Font...")
        try:
            r = requests.get(font_url, timeout=15)
            r.raise_for_status()
            with open(font_path, 'wb') as f:
                f.write(r.content)
            print("✅ Font downloaded.")
        except Exception as e:
            print(f"❌ Font download failed: {e}")
            sys.exit(1)
    return font_path

# ✅ Unique Images - Koi Duplicate Nahi
romantic_images = [
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502323777036-f29e3972d82f?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1541123437800-1bb1317badc2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1541516160071-4bb0c5af65ba?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531427186611-ecfd6d936c79?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1499996860823-5214fcc65f8f?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1485178575877-1a13bf489dfe?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517365830460-955ce3ccd263?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1501901609772-df0848060b33?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1495301839102-1e9b0a998cc3?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1485182708500-e8f1f318ba72?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522098543979-ffc7f79a56c4?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517448931760-8b278f2b56e3?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1508049173477-187e13e7d68f?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1474552226712-ac0f0961a954?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519638831568-d9897f54ed69?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1496347646636-ea47f7d6b37b?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1515023115689-589c33041d3c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521146764736-56c929d59c83?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1499952127939-9bbf5af6c51c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502378735452-bc7d86632805?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1513956589380-bad6acb9b9d4?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521341057461-6eb5f40b07ab?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1504198458649-3128b932f49e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1520854221256-17451cc331bf?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519741497674-611481863552?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1523438885200-e635ba2c371e?q=80&w=1080&auto=format&fit=crop"
]

# ✅ Romantic Shayari - Page Safe + Viral
shayari_data = [
    {"roman": "Teri baahon mein sukoon milta hai,\nJaise kisi ki dua qabool ho gayi ho.", "urdu": "تیری بانہوں میں سکون ملتا ہے،\nجیسے کسی کی دعا قبول ہو گئی ہو۔"},
    {"roman": "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.", "urdu": "تیرے بغیر یہ دل سن سن سا ہے،\nجیسے بغیر بارش کے موسم سونا ہے۔"},
    {"roman": "Tujhe dekh kar aise khoya main,\nJaise koi khwab dekh kar soya main.", "urdu": "تجھے دیکھ کر ایسے کھویا میں،\nجیسے کوئی خواب دیکھ کر سویا میں۔"},
    {"roman": "Ek tera saath chahiye, har khushi se pehle,\nEk teri yaad, sari duniya se pehle.", "urdu": "ایک تیرا ساتھ چاہیے، ہر خوشی سے پہلے،\nایک تیری یاد، ساری دنیا سے پہلے۔"},
    {"roman": "Teri zulfon ki khushbu mein kho jata hoon,\nTere chehre ko dekhta hoon toh kho jata hoon.", "urdu": "تیری زلفوں کی خوشبو میں کھو جاتا ہوں،\nتیرے چہرے کو دیکھتا ہوں تو کھو جاتا ہوں۔"},
    {"roman": "Tere ishq ki aag mein jalna acha lagta hai,\nTere liye har dard sehna acha lagta hai.", "urdu": "تیرے عشق کی آگ میں جلنا اچھا لگتا ہے،\nتیرے لیے ہر درد سہنا اچھا لگتا ہے۔"},
    {"roman": "Tujhe chahne ki koi hadd nahi,\nTere ishq ki koi hadd nahi.", "urdu": "تجھے چاہنے کی کوئی حد نہیں،\nتیرے عشق کی کوئی حد نہیں۔"},
    {"roman": "Tere paas aata hoon toh waqt ruk jata hai,\nTujhe chhod kar jata hoon toh dil ruk jata hai.", "urdu": "تیرے پاس آتا ہوں تو وقت رک جاتا ہے،\nتجھے چھوڑ کر جاتا ہوں تو دل رک جاتا ہے۔"},
    {"roman": "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.", "urdu": "تمہاری باتوں میں وہ پیار ہے،\nجو کسی اور کی باتوں میں نہیں۔"},
    {"roman": "Tere pyar mein hum toh aise doobe,\nJaise patthar paani mein doobta hai.", "urdu": "تیرے پیار میں ہم تو ایسے ڈوبے،\nجیسے پتھر پانی میں ڈوبتا ہے۔"},
    {"roman": "Mera dil tere naam ka ho gaya,\nJaise kisi ne mujhe teri yaadon ka tohfa de diya ho.", "urdu": "میرا دل تیرے نام کا ہو گیا،\nجیسے کسی نے مجھے تیری یادوں کا تحفہ دے دیا ہو۔"},
    {"roman": "Tumhi ko chaha hai, tumhi ko puja hai,\nMeri hadd toh dekho, duniya ko bhula kar tumhe dhoonda hai.", "urdu": "تمہیں چاہا ہے، تمہیں پوجا ہے،\nمیری حد تو دیکھو، دنیا کو بھلا کر تمہیں ڈھونڈا ہے۔"},
    {"roman": "Tere ishq mein jalna bhi ibadat si lagti hai,\nTeri yaad mein jeena bhi hasrat si lagti hai.", "urdu": "تیرے عشق میں جلنا بھی عبادت سی لگتی ہے،\nتیری یاد میں جینا بھی حسرت سی لگتی ہے۔"},
    {"roman": "Meri aankhon mein teri tasveer hai,\nMere dil mein tera nasha hai.", "urdu": "میری آنکھوں میں تیری تصویر ہے،\nمیرے دل میں تیرا نشہ ہے۔"},
    {"roman": "Teri baahon mein jo sukoon mila,\nWoh kisi jannat mein bhi nahi milta.", "urdu": "تیری بانہوں میں جو سکون ملا،\nوہ کسی جنت میں بھی نہیں ملتا۔"},
    {"roman": "Kisi ko chahna gunah toh nahi,\nPar kisi ka ho jana aasan bhi nahi.", "urdu": "کسی کو چاہنا گناہ تو نہیں،\nپر کسی کا ہو جانا آسان بھی نہیں۔"},
    {"roman": "Tere labon ki muskaan pe fida hoon,\nTeri har ada pe fida hoon.", "urdu": "تیرے لبوں کی مسکان پہ فدا ہوں،\nتیری ہر ادا پہ فدا ہوں۔"},
    {"roman": "Raat bhar teri yaadon mein khoya rahoon,\nTere khwabon mein hi soya rahoon.", "urdu": "رات بھر تیری یادوں میں کھویا رہوں،\nتیرے خوابوں میں ہی سویا رہوں۔"},
    {"roman": "Teri khushbu se hi meri saans chalti hai,\nTeri yaad se hi mujhe sukoon milta hai.", "urdu": "تیری خوشبو سے ہی میری سانس چلتی ہے،\nتیری یاد سے ہی مجھے سکون ملتا ہے۔"},
    {"roman": "Tere ishq mein hadd se guzar jayenge,\nTere liye duniya se lad jayenge.", "urdu": "تیرے عشق میں حد سے گزر جائیں گے،\nتیرے لیے دنیا سے لڑ جائیں گے۔"},
    {"roman": "Mujhe teri aadat si nahi, junoon hai,\nTere bina jeena toh ek saza hai.", "urdu": "مجھے تیری عادت سی نہیں، جنون ہے،\nتیرے بغیر جینا تو ایک سزا ہے۔"},
    {"roman": "Tere pyar mein hadd se guzar gaye hum,\nTujhe chahte chahte mar gaye hum.", "urdu": "تیرے پیار میں حد سے گزر گئے ہم،\nتجھے چاہتے چاہتے مر گئے ہم۔"},
    {"roman": "Woh mujhse pyar ka izhar kar rahe hain,\nMain unko dekh kar sharma raha hoon.", "urdu": "وہ مجھ سے پیار کا اظہار کر رہے ہیں،\nمیں ان کو دیکھ کر شرما رہا ہوں۔"},
    {"roman": "Teri aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan.", "urdu": "تیری آنکھوں میں جو نشہ ہے،\nوہ کسی شراب میں کہاں۔"},
    {"roman": "Dil chahta hai tujhe seene se laga loon,\nTeri yaadon mein hi kho jaoon.", "urdu": "دل چاہتا ہے تجھے سینے سے لگا لوں،\nتیری یادوں میں ہی کھو جاؤں۔"},
    {"roman": "Tere naam se shuru, tere naam pe khatam,\nMeri kahani tu hi hai, mera anjaam tu hi hai.", "urdu": "تیرے نام سے شروع، تیرے نام پہ ختم،\nمیری کہانی تو ہی ہے، میرا انجام تو ہی ہے۔"},
    {"roman": "Chandni raat mein teri yaad aayi,\nDil ne phir teri tasveer banayi.", "urdu": "چاندنی رات میں تیری یاد آئی،\nدل نے پھر تیری تصویر بنائی۔"},
    {"roman": "Tum mile toh laga, dua qabool ho gayi,\nMeri har khushi ab tere naam ho gayi.", "urdu": "تم ملے تو لگا، دعا قبول ہو گئی،\nمیری ہر خوشی اب تیرے نام ہو گئی۔"},
    {"roman": "Ishq tera meri jaan le gaya,\nTere bina jeena mushkil ho gaya.", "urdu": "عشق تیرا میری جان لے گیا،\nتیرے بغیر جینا مشکل ہو گیا۔"},
    {"roman": "Teri ek muskaan pe sab kuch luta doon,\nTere liye apni jaan bhi de doon.", "urdu": "تیری ایک مسکان پہ سب کچھ لٹا دوں،\nتیرے لیے اپنی جان بھی دے دوں۔"}
]

HASHTAGS = "#UrduShayari #UrduPoetry #RomanticShayari #LoveQuotes #Aesthetic #Trending #Viral #FYP #HinaFatima #Ishq #Mohabbat"

def process_and_post():
    if not PAGE_ID or not TOKEN:
        print("❌ FB_PAGE_ID ya FB_TOKEN secret missing hai!")
        sys.exit(1)
    font_path = download_font()
    image_url = random.choice(romantic_images)
    selected_shayari = random.choice(shayari_data)
    try:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=15)
            img_response.raise_for_status()
            img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
        except Exception as e:
            print(f"Image download fail, blank background use kar raha hoon: {e}")
            img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255))
        
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        for i in range(img.height):
            alpha = int(160 * (i / img.height))
            draw_overlay.line([(0, i), (img.width, i)], fill=(0, 0, 0, alpha))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        roman_text = selected_shayari["roman"]
        font_size = 65 
        max_width = img.width - 150   
        max_height = img.height - 400 
        
        while font_size > 20:
            try:
                shairi_font = ImageFont.truetype(font_path, font_size)
            except:
                shairi_font = ImageFont.load_default()
                break
            bbox = draw.multiline_textbbox((0, 0), roman_text, font=shairi_font, align="center")
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            if text_width < max_width and text_height < max_height:
                break
            font_size -= 2 

        x_center = img.width / 2
        y_center = (img.height / 2) - 50 
        
        draw.multiline_text((x_center, y_center), roman_text, font=shairi_font, fill="white", anchor="mm", align="center", stroke_width=4, stroke_fill="black")
        
        try:
            wm_font = ImageFont.truetype(font_path, 40)
        except:
            wm_font = ImageFont.load_default()
        draw.text((img.width / 2, img.height - 80), PAGE_NAME, font=wm_font, fill="white", anchor="mm", stroke_width=2, stroke_fill="black")
        
        image_path = "premium_shairi.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        print("Uploading to 【entity-Facebook¦canonical_name=Facebook】...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        urdu_caption = selected_shayari["urdu"]
        caption = f"{urdu_caption}\n\nTag someone! ❤\n\n{HASHTAGS}"
        payload = {"caption": caption, "access_token": TOKEN}
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            fb_response = requests.post(fb_url, data=payload, files=files, timeout=30)
        print(f"【entity-Facebook¦canonical_name=Facebook】 Response: {fb_response.status_code}")
        fb_response.raise_for_status()
        print(f"✅ POST SUCCESS! ID: {fb_response.json().get('id')}")
    except Exception as e:
        print(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_and_post()

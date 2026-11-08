import os
import random
import requests
import io
import re
from PIL import Image, ImageDraw, ImageFont

# GitHub Secrets se IDs uthana
PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# AI Prompts (Photorealistic Real Photo Style)
expressions = [
    "making a funny goofy face", "looking extremely shocked", 
    "crying in a dramatic funny way", "judging the camera", 
    "sassy attitude pose", "laughing out loud", 
    "confused expression", "angry dramatic look"
]
outfits = [
    "wearing a traditional Pakistani shalwar kameez", 
    "in a glamorous Indian TV actress saree", 
    "wearing a modern stylish dress", 
    "in a heavily embroidered bridal dress"
]
styles = [
    "raw photo, photorealistic, shot on DSLR 35mm lens, 8k resolution, ultra-detailed face, natural skin texture, realistic lighting",
    "highly detailed real photography, realistic human face, professional portrait photo, sharp focus",
    "real life photography, cinematic natural lighting, no digital art, no anime, highly realistic"
]

# Unlimited Funny Lines (Emojis hata diye hain taake font ka masla na ho)
funny_lines = [
    "Ammi ne pakka yeh scene nahi dekhna chahiye tha",
    "Kya acting hai waise!", "Yeh expression dekh ke toh meri hasi nahi ruk rahi",
    "Guys, yeh kaunsa drama hai?", "Mujhe toh bas yeh jodi pasand hai",
    "Koi batao yeh actress kaun hai?", "Aaj kal ke dramas mein bas rona hi rona hai",
    "Iska makeup toh kamaal ka hai", "Itna highlighter lagaya hai ke face chamak raha hai",
    "Contour kahan se seekha hai waise?", "Lipstick ka shade toh ekdum perfect hai",
    "Naya look, nayi vibe", "Iska expression toh ekdum 'Ammi ne daant di hai' wala hai",
    "Aankhon se hi sab keh diya isne", "Mashallah, kitni pyari lag rahi hain!",
    "Bhai yeh actress toh har drama mein same acting karti hai",
    "Is drama ne toh hadd kar di hai yaar", "Ek episode dekh ke hi pata chal gaya ending kya hogi"
]

def generate_unique_ai_image():
    exp = random.choice(expressions)
    out = random.choice(outfits)
    sty = random.choice(styles)
    
    # ✅ PROMPT FIX: Asli Photo jaisa banane ke liye strong instructions
    prompt = f"Raw photo, photorealistic portrait of a real Pakistani TV actress, {exp}, {out}, {sty}, extremely realistic, not a cartoon, not an illustration, absolutely no digital art"
    print(f"Generating Image for: {prompt}")
    
    unique_seed = random.randint(1, 9999999)
    image_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1080&height=1080&nologo=true&seed={unique_seed}&model=flux"
    
    response = requests.get(image_url)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content)).convert("RGB")
    
    # Watermark Hatane ke liye Crop
    width, height = img.size
    img = img.crop((0, 0, width, height - 50)) 
    
    return img

def add_funny_text(image):
    draw = ImageDraw.Draw(image)
    line = random.choice(funny_lines)
    
    # Text ko saaf karo
    line_text = re.sub(r'[^\w\s\?\.,!]', '', line)

    # Auto-Fit Text Logic
    font_size = 70
    max_width = image.width - 40
    while font_size > 10:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
            break
        bbox = draw.textbbox((0, 0), line_text, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_width:
            break
        font_size -= 2

    bbox = draw.textbbox((0, 0), line_text, font=font)
    x = (image.width - (bbox[2] - bbox[0])) / 2
    y = image.height - 120
    
    for adj in range(-3, 4):
        draw.text((x+adj, y), line_text, font=font, fill="black")
        draw.text((x, y+adj), line_text, font=font, fill="black")
    draw.text((x, y), line_text, font=font, fill="white")
    
    print(f"Added Comment: {line_text}")
    return image

def post_to_facebook(image):
    image_path = "unique_meme.jpg"
    image.save(image_path, format="JPEG")

    fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    payload = {
        "caption": "Drama lovers kahan hain? 😂🔥 Follow for more! #PakistaniDrama #Funny",
        "access_token": TOKEN
    }

    with open(image_path, 'rb') as img_file:
        files = {'source': img_file}
        response = requests.post(fb_url, data=payload, files=files)

    response.raise_for_status()
    print(f"✅ Post Success! ID: {response.json().get('id')}")

if __name__ == "__main__":
    try:
        print("Starting Meme Generation...")
        ai_image = generate_unique_ai_image()
        final_image = add_funny_text(ai_image)
        print("Posting to Facebook...")
        post_to_facebook(final_image)
    except Exception as e:
        print(f"❌ Error aagaya: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

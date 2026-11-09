import os
import random
import requests
import urllib.parse

# GitHub Secrets se IDs uthana
PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# ✅ Current Dramas ke Fresh aur Funny Jokes (Roman Urdu)
current_drama_jokes = [
    ("Ammi: Shaadi karlo", "Me: Pehle Jaan Nisar ka end dekh loon"),
    ("Kabhi Main Kabhi Tum", "Mera dil aur dimagh"),
    ("Drama Hero:", "Drama Heroine:"),
    ("Log: Dramas fake hote hain", "Me: (Rone lagta hoon)"),
    ("Ek episode dekhne baitha tha", "Poori raat nikal gayi"),
    ("Ammi: Phone chhoro", "Me: Bas 5 minute aur"),
    ("Jaan Nisar ke baad", "Mujhe kisi se pyar nahi hona"),
    ("Drama Villain", "Hamesha Hero ki shakal"),
    ("Background music", "Har emotional scene mein"),
    ("Ek episode ke baad", "100 ads"),
    ("Mera dimagh", "Drama ke plot holes"),
    ("Jab drama ka end aata hai", "Aur aapki zindagi khali lagti hai"),
    ("Ammi ka gussa", "Drama ki villain"),
    ("Mujhe drama nahi dekhna", "Phir 2 ghante baad: Kya scene tha!"),
    ("Padosi: Shaadi kab karoge?", "Me: Jab drama ka last episode aayega"),
    ("Zindagi mein tension", "Drama dekh kar aur badh gayi"),
    ("Mera favorite character", "Hamesha pehle mar jata hai"),
    ("Kabhi Main Kabhi Tum ka OST", "Meri ringtone"),
    ("Ammi: Bahar jao", "Me: Drama ka climax aa raha hai"),
    ("Drama dekhne ke baad", "Mujhe bhi acting ka shauk ho gaya")
]

# ✅ Famous Meme Templates (No Instagram UI, 100% Clean)
templates = [
    "drake",          # Drake wala meme
    "distracted",     # Distracted Boyfriend
    "pikachu",        # Surprised Pikachu
    "gru",            # Gru ka plan
    "rollsafe",       # Sochne wala aadmi
    "success",        # Success kid
    "woman-cat",      # Woman yelling at cat
    "two-buttons",    # Do buttons wala
    "buzz",           # Buzz Lightyear
    "yoda",           # Yoda
    "spiderman",      # Spiderman
    "batman"          # Batman
]

# 35+ Viral Hashtags (Reach barhane ke liye)
HASHTAGS = """
#PakistaniDrama #IndianDrama #Meme #FunnyMemes #Trending #Viral #HaniaAamir 
#WahajAli #JaanNisar #KabhiMainKabhiTum #SajalAly #AyezaKhan #YumnaZaidi 
#Bollywood #Lollywood #TikTokPakistan #Entertainment #DramaSerial #DramaQueen 
#Fun #Laugh #Comedy #MemePage #DramaMeme #ViralMemes #ExplorePage #FYP 
#ForYouPage #Relatable #DesiMemes #DramaLovers #PakistanZindabad 
"""

def post_meme():
    # 1. Random template aur joke select karo
    template = random.choice(templates)
    top_text, bottom_text = random.choice(current_drama_jokes)
    
    # 2. Text ko URL-safe banayo
    safe_top = urllib.parse.quote(top_text, safe='')
    safe_bottom = urllib.parse.quote(bottom_text, safe='')
    
    # 3. Memegen API ka URL banao
    meme_url = f"https://api.memegen.link/images/{template}/{safe_top}/{safe_bottom}.png"
    print(f"Generated Meme URL: {meme_url}")
    
    # 4. Image ko download karo
    try:
        headers = {'User-Agent': 'Mozilla/5.0'} 
        img_response = requests.get(meme_url, headers=headers, timeout=15)
        img_response.raise_for_status()
        
        if len(img_response.content) < 1000:
            print("❌ Image file kharab hai.")
            return
            
        image_path = "clean_drama_meme.png"
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
            
    except Exception as e:
        print(f"❌ Image download nahi ho saki: {e}")
        return

    # 5. Facebook par upload karo
    fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    payload = {
        "caption": f"Tag your drama lover friend! 😂🔥\n\nAapko yeh meme kaisa laga? Comment below! 👇\n\n{HASHTAGS}",
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
    print("Starting Clean & Current Drama Meme Generation...")
    post_meme()

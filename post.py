import os
import random
import requests
import urllib.parse

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# 1. Drama ke sab se Funny aur Relatable Jokes
jokes = [
    ("Ammi: Shaadi karlo", "Me: Pehle Jaan Nisar ka end dekh loon"),
    ("Ammi: Phone chhoro", "Me: Bas 5 minute aur"),
    ("Drama Hero:", "Drama Heroine:"),
    ("Log: Dramas fake hote hain", "Me: (Rone lagta hoon)"),
    ("Ek episode dekhne baitha tha", "Poori raat nikal gayi"),
    ("Ammi: Padhai karo", "Me: Kabhi Main Kabhi Tum dekh raha hoon"),
    ("Drama Villain", "Hamesha Hero ki shakal"),
    ("Background music", "Har emotional scene mein"),
    ("Ek episode ke baad", "100 ads"),
    ("Mera dimagh", "Drama ke plot holes"),
    ("Jab drama ka end aata hai", "Aur aapki zindagi khali lagti hai"),
    ("Drama dekhne se pehle", "Drama dekhne ke baad (Depressed)"),
    ("Ammi ka gussa", "Drama ki villain"),
    ("Mujhe drama nahi dekhna", "Phir 2 ghante baad: Kya scene tha!"),
    ("Padosi: Shaadi kab karoge?", "Me: Jab drama ka last episode aayega")
]

# 2. Famous Meme Templates (Jo internet par hamesha available hain)
templates = [
    "drake",          # Drake wala meme
    "distracted",     # Distracted Boyfriend
    "pikachu",        # Surprised Pikachu
    "gru",            # Gru ka plan
    "rollsafe",       # Sochne wala aadmi
    "success",        # Success kid
    "woman-cat",      # Woman yelling at cat
    "two-buttons"     # Do buttons wala
]

def post_meme():
    # 1. Randomly ek template aur joke select karein
    template = random.choice(templates)
    top_text, bottom_text = random.choice(jokes)
    
    # 2. Text ko URL ke liye safe banayein (spaces aur emojis handle karne ke liye)
    safe_top = urllib.parse.quote(top_text)
    safe_bottom = urllib.parse.quote(bottom_text)
    
    # 3. Memegen API ka URL banayein (Yeh automatic picture bana dega)
    meme_url = f"https://api.memegen.link/images/{template}/{safe_top}/{safe_bottom}.png"
    
    print(f"Posting Auto Meme: {meme_url}")
    
    # 4. Facebook par post karein
    fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
    payload = {
        "url": meme_url,
        "caption": "Drama lovers kahan hain? 😂🔥 Tag your friends! #PakistaniDrama #FunnyMemes",
        "access_token": TOKEN
    }
    
    try:
        response = requests.post(fb_url, data=payload)
        response.raise_for_status()
        print(f"✅ Post Success! ID: {response.json().get('id')}")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

if __name__ == "__main__":
    post_meme()

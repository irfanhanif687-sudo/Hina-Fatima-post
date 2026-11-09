import os
import random
import requests

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Memes lene ke liye subreddits (Yeh proxy API inko block nahi karegi)
subreddits = ["pakistanimemes", "indianmemes", "bollywoodmemes", "pakistanidrama"]

def get_unlimited_real_meme():
    sub = random.choice(subreddits)
    
    # ✅ Magic Proxy API jo bina block hue Reddit se meme uthata hai
    url = f"https://meme-api.com/gimme/{sub}"
    print(f"Fetching real meme from r/{sub} via Meme-API...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Agar meme NSFW (gandi) hai toh skip karo
        if data.get('nsfw', False):
            print("❌ NSFW meme mila, skip kar rahe hain.")
            return None
            
        meme_url = data.get('url')
        if meme_url:
            print(f"Found Real Meme: {meme_url}")
            return meme_url
        return None
    except Exception as e:
        print(f"❌ API Error: {e}")
        return None

def post_to_facebook(meme_url):
    if not meme_url:
        print("❌ Koi meme nahi mila.")
        return
        
    try:
        # 1. Meme download karo
        print("Downloading meme...")
        img_response = requests.get(meme_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        img_response.raise_for_status()
        
        if len(img_response.content) < 1000:
            print("❌ Image file kharab hai.")
            return
            
        image_path = "real_meme.jpg"
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
            
        # 2. Facebook par upload karo
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        payload = {
            "caption": "Tag your drama lover friend! 😂🔥 Follow for more! #PakistaniDrama #Meme #Funny",
            "access_token": TOKEN
        }
        
        with open(image_path, 'rb') as img_file:
            files = {'source': img_file}
            fb_response = requests.post(fb_url, data=payload, files=files, timeout=20)
            
        fb_response.raise_for_status()
        print(f"✅ Post Success! ID: {fb_response.json().get('id')}")
        
    except Exception as e:
        print(f"❌ Facebook Post Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(e.response.text)

if __name__ == "__main__":
    print("Starting Unlimited Real Meme Generation...")
    meme_url = get_unlimited_real_meme()
    if meme_url:
        post_to_facebook(meme_url)

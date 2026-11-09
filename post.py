import os
import random
import requests

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

# Subreddits list
subreddits = ["pakistanimemes", "indianmemes", "bollywoodmemes", "pakistanidrama"]

def get_unlimited_meme():
    sub = random.choice(subreddits)
    url = f"https://www.reddit.com/r/{sub}/hot.json?limit=100"
    
    # ✅ FIX 1: Reddit ko lagta hai koi bot hai agar proper browser header na ho
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Fetching memes from r/{sub}...")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Reddit API Error: {e}")
        return None
        
    posts = response.json()['data']['children']
    
    valid_images = []
    for post in posts:
        # Agar post hide ya remove ho chuki hai toh skip karo
        if post['data'].get('hidden') or post['data'].get('removed'):
            continue
            
        img_url = post['data']['url']
        # ✅ FIX 2: Sirf direct image links uthao (videos ya imgur pages nahi)
        if img_url.lower().endswith(('.jpg', '.jpeg', '.png')):
            valid_images.append(img_url)
            
    if not valid_images:
        print("❌ Is waqt koi valid image nahi mili is subreddit mein.")
        return None
        
    selected_meme_url = random.choice(valid_images)
    print(f"Selected Meme URL: {selected_meme_url}")
    return selected_meme_url

def post_to_facebook(meme_url):
    if not meme_url:
        print("❌ Skip: Koi valid meme nahi mila.")
        return
        
    try:
        # Image Download
        print("Downloading image...")
        img_response = requests.get(meme_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        img_response.raise_for_status()
        
        if len(img_response.content) < 1000:
            print("❌ Image file kharab hai (size bohat choti hai).")
            return
            
        image_path = "reddit_meme.jpg"
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
            
        # Facebook Upload
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
    print("Starting Unlimited Reddit Meme Generation...")
    meme_url = get_unlimited_meme()
    if meme_url:
        post_to_facebook(meme_url)

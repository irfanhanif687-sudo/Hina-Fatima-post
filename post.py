import os
import random
import requests
import io
import sys
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

PAGE_NAME = "Hina Fatima"

# ✅ Function to download Premium Font (Poppins)
def download_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
    font_path = "Poppins-Bold.ttf"
    if not os.path.exists(font_path):
        print("Downloading Premium Font...")
        r = requests.get(font_url)
        with open(font_path, 'wb') as f:
            f.write(r.content)
    return font_path

# ✅ 60+ High-Quality Romantic, Hugs & Cinematic Pictures
romantic_images = [
    "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1515023115689-589c33041d3c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521146764736-56c929d59c83?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517365830460-955ce3ccd263?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1499952127939-9bbf5af6c51c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502378735452-bc7d86632805?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1513956589380-bad6acb9b9d4?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1513956589380-bad6acb9b9d4?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502378735452-bc7d86632805?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1515023115689-589c33041d3c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521146764736-56c929d59c83?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517365830460-955ce3ccd263?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1499952127939-9bbf5af6c51c?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1521119989659-a83eee488004?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop"
]

# ✅ 60+ Deep, Bold & Romantic Shayari (Aapke diye hue text se)
shayari_data = [
    {"roman": "Apne haseen honton ko kisi parday mein chhupa liya karo,\nHum gustakh log hain nazron se choom liya karte hain.", "urdu": "اپنے حسین ہونٹوں کو کسی پردے میں چھپا لیا کرو،\nہم گستاخ لوگ ہیں نظروں سے چوم لیا کرتے ہیں۔"},
    {"roman": "Main toad leta agar tu gulab hoti,\nMain jawab banta agar tu sawaal hoti,\nSab jaante hain main nasha nahi karta,\nMain bhi pee leta agar tu sharaab hoti.", "urdu": "میں توڑ لیتا اگر تو گلاب ہوتی،\nمیں جواب بنتا اگر تو سوال ہوتی،\nسب جانتے ہیں میں نشہ نہیں کرتا،\nمیں بھی پی لیتا اگر تو شراب ہوتی۔"},
    {"roman": "Baithe hain hum us raat ke intezar mein,\nJab unke honton ki surkhiyan humare honton ke sath hongi.", "urdu": "بیٹھے ہیں ہم اس رات کے انتظار میں،\nجب ان کے ہونٹوں کی سرخیاں ہمارے ہونٹوں کے ساتھ ہوں گی۔"},
    {"roman": "Kuch nahi chahiye bas milne aa jao,\nSach mein bohot mann kar raha hai tumhare seene se lagne ka.", "urdu": "کچھ نہیں چاہیے بس ملنے آ جاؤ،\nسچ میں بہت من کر رہا ہے تمہارے سینے سے لگنے کا۔"},
    {"roman": "Palkein kab tak ruku mein rakhoge,\nHusn ka wasta, qayaam karo.", "urdu": "پلکیں کب تک رکوع میں رکھو گے،\nحسن کا واسطہ، قیام کرو۔"},
    {"roman": "Tumhe yahi lagta hai na hum tumhare husn pe marte hain,\nToh chale jao, jab husn dhal jaye toh laut aana.", "urdu": "تمہیں یہی لگتا ہے نا ہم تمہارے حسن پہ مرتے ہیں،\nتو چلے جاؤ، جب حسن ڈھل جائے تو لوٹ آنا۔"},
    {"roman": "Main rooth jaoon toh tum mana lena,\nKuch mat kehna bas seene se laga lena.", "urdu": "میں روٹھ جاؤں تو تم منا لینا،\nکچھ مت کہنا بس سینے سے لگا لینا۔"},
    {"roman": "Thore ghusse wale thore nadan ho tum,\nLekin jaise bhi ho meri jaan ho tum.", "urdu": "تھوڑے غصے والے تھوڑے نادان ہو تم،\nلیکن جیسے بھی ہو میری جان ہو تم۔"},
    {"roman": "Tumhare sath khamosh bhi rahoon toh baatein poori ho jati hain,\nTum mein, tum se, tum par hi meri duniya poori ho jati hai.", "urdu": "تمہارے ساتھ خاموش بھی رہوں تو باتیں پوری ہو جاتی ہیں،\nتم میں، تم سے، تم پر ہی میری دنیا پوری ہو جاتی ہے۔"},
    {"roman": "Reha nahi jata tere deedar ke bina,\nZindagi adhoori lagti hai meri tere pyar ke bina.", "urdu": "رہا نہیں جاتا تیرے دیدار کے بنا،\nزندگی ادھوری لگتی ہے میری تیرے پیار کے بنا۔"},
    {"roman": "Tum ho aaghosh mein magar phir bhi,\nDil nahi lag raha mera janaan.", "urdu": "تم ہو آغوش میں مگر پھر بھی،\nدل نہیں لگ رہا مرا جاناں۔"},
    {"roman": "Maine har woh lafz keh diya jiska matlab mohabbat tha,\nWoh phir bhi na samajh saka meri lafzon ki gehrai ko.", "urdu": "میں نے ہر وہ لفظ کہہ دیا جس کا مطلب محبت تھا،\nوہ پھر بھی نہ سمجھ سکا میری لفظوں کی گہرائی کو۔"},
    {"roman": "Apna bana kar humein apni aaghosh mein bhar lo,\nHonge nahi kabhi juda hum aaj yeh waada kar lo.", "urdu": "اپنا بنا کر ہمیں اپنی آغوش میں بھر لو،\nہوں گے نہیں کبھی جدا ہم آج یہ وعدہ کر لو۔"},
    {"roman": "Main na-samajh hi sahi magar woh tara hoon,\nJo teri ek khwahish ke liye sau baar bhi toot jaoon.", "urdu": "میں ناسمجھ ہی سہی مگر وہ تارا ہوں،\nجو تیری ایک خواہش کے لیے سو بار بھی ٹوٹ جاؤں۔"},
    {"roman": "Teri muskurahat pe dil haar baithe warna,\nDil toh woh Sikandar hai jo kabhi haara na tha.", "urdu": "تیری مسکراہٹ پہ دل ہار بیٹھے ورنہ،\nدل تو وہ سکندر ہے جو کبھی ہارا نہ تھا۔"},
    {"roman": "Bandh diya hai aaj maine apne dil ko rasiyon se,\nBohot zid karta hai tum se milne ke liye.", "urdu": "باندھ دیا ہے آج میں نے اپنے دل کو رسیوں سے،\nبہت ضد کرتا ہے تم سے ملنے کے لیے۔"},
    {"roman": "Zaroori toh nahi ke nazdeekiyon mein hi pyar ho,\nFaslon mein bhi ishq ki bulandiyan dekhi hain.", "urdu": "ضروری تو نہیں کہ نزدیکیوں میں ہی پیار ہو،\nفاصلوں میں بھی عشق کی بلندیاں دیکھی ہیں۔"},
    {"roman": "Aap maano ya na maano kar jo mohabbat aap se ki hai,\nWoh na kisi se thi aur na kisi se karenge.", "urdu": "آپ مانو یا نہ مانو کر جو محبت آپ سے کی ہے،\nوہ نہ کسی سے تھی اور نہ کسی سے کریں گے۔"},
    {"roman": "Ishq kya cheez hai, rukhsaar mein kya rakha hai?\nDil hi mar jaye toh sansaar mein kya rakha hai?", "urdu": "عشق کیا چیز ہے، رُخسار میں کیا رکھا ہے؟\nدل ہی مر جائے تو سَنسار میں کیا رکھا ہے؟"},
    {"roman": "Saaf niyat se maanga jaye,\nToh Rab naseeb se badh kar deta hai.", "urdu": "صاف نیت سے مانگا جائے،\nتو رب نصیب سے بڑھ کر دیتا ہے۔"},
    {"roman": "Tumhari aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan milta hai.", "urdu": "تمہاری آنکھوں میں جو نشہ ہے،\nوہ کسی شراب میں کہاں ملتا ہے۔"},
    {"roman": "Tere hothon pe apne hoth rakh doon,\nSari duniya ki fikar bhula doon.", "urdu": "تیرے ہونٹھوں پر اپنے ہونٹھ رکھ دوں،\nساری دنیا کی فکر بھلا دوں۔"},
    {"roman": "Tere jism ki khushbu mere dil mein utar jaye,\nTujhe chahoo toh meri jaan kidhar jaye.", "urdu": "تیرے جسم کی خوشبو میرے دل میں اتر جائے،\nتجھے چاہوں تو میری جان کدھر جائے۔"},
    {"roman": "Aag lagati hai teri baatein mujhmein,\nTu paas aata hai toh dhadkan tez hoti hai.", "urdu": "آگ لگاتی ہیں تیری باتیں مجھ میں،\nتو پاس آتا ہے تو دھڑکن تیز ہوتی ہے۔"},
    {"roman": "Mujhe teri aadat si nahi, junoon hai,\nTere bina jeena toh ek saza hai.", "urdu": "مجھے تیری عادت سی نہیں، جنون ہے،\nتیرے بغیر جینا تو ایک سزا ہے۔"},
    {"roman": "Tere labon ka swaad ab tak mere hothon par hai,\nYeh ishq nahi, meri jaan, ek nasha hai.", "urdu": "تیرے لبوں کا ذائقہ اب تک میرے ہونٹھوں پر ہے،\nیہ عشق نہیں، میری جان، ایک نشہ ہے۔"},
    {"roman": "Teri baahon mein aake toh jaise,\nSari kayanat mil gayi ho.", "urdu": "تیری بانہوں میں آ کے تو جیسے،\nساری کائنات مل گئی ہو۔"},
    {"roman": "Tujhe dekh kar aise khoya main,\nJaise koi nasha kar ke soya main.", "urdu": "تجھے دیکھ کر ایسے کھویا میں،\nجیسے کوئی نشہ کر کے سویا میں۔"},
    {"roman": "Tere pyar mein hadd se guzar jayenge,\nTere liye duniya se lad jayenge.", "urdu": "تیرے پیار میں حد سے گزر جائیں گے،\nتیرے لیے دنیا سے لڑ جائیں گے۔"},
    {"roman": "Teri baahon mein sukoon milta hai,\nJaise kisi ki dua qabool ho gayi ho.", "urdu": "تیری بانہوں میں سکون ملتا ہے،\nجیسے کسی کی دعا قبول ہو گئی ہو۔"},
    {"roman": "Ek tera saath chahiye, har khushi se pehle,\nEk teri baahon mein jagah, sari duniya se pehle.", "urdu": "ایک تیرا ساتھ چاہیے، ہر خوشی سے پہلے،\nایک تیری بانہوں میں جگہ، ساری دنیا سے پہلے۔"},
    {"roman": "Teri zulfon ki khushbu mein kho jata hoon,\nTere chehre ko dekhta hoon toh kho jata hoon.", "urdu": "تیری زلفوں کی خوشبو میں کھو جاتا ہوں،\nتیرے چہرے کو دیکھتا ہوں تو کھو جاتا ہوں۔"},
    {"roman": "Tere ishq ki aag mein jalna acha lagta hai,\nTere liye har dard sehna acha lagta hai.", "urdu": "تیرے عشق کی آگ میں جلنا اچھا لگتا ہے،\nتیرے لیے ہر درد سہنا اچھا لگتا ہے۔"},
    {"roman": "Tujhe chahne ki koi hadd nahi,\nTere ishq ki koi hadd nahi.", "urdu": "تجھے چاہنے کی کوئی حد نہیں،\nتیرے عشق کی کوئی حد نہیں۔"},
    {"roman": "Tere paas aata hoon toh waqt ruk jata hai,\nTujhe chhod kar jata hoon toh dil ruk jata hai.", "urdu": "تیرے پاس آتا ہوں تو وقت رک جاتا ہے،\nتجھے چھوڑ کر جاتا ہوں تو دل رک جاتا ہے۔"},
    {"roman": "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.", "urdu": "تمہاری باتوں میں وہ پیار ہے،\nجو کسی اور کی باتوں میں نہیں۔"},
    {"roman": "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.", "urdu": "تیرے بغیر یہ دل سن سن سا ہے،\nجیسے بغیر بارش کے موسم سونا ہے۔"},
    {"roman": "Tere pyar mein hum toh aise doobe,\nJaise patthar paani mein doobta hai.", "urdu": "تیرے پیار میں ہم تو ایسے ڈوبے،\nجیسے پتھر پانی میں ڈوبتا ہے۔"},
    {"roman": "Mera dil tere naam ka ho gaya,\nJaise kisi ne mujhe teri yaadon ka tohfa de diya ho.", "urdu": "میرا دل تیرے نام کا ہو گیا،\nجیسے کسی نے مجھے تیری یادوں کا تحفہ دے دیا ہو۔"},
    {"roman": "Tumhi ko chaha hai, tumhi ko puja hai,\nMeri hadd toh dekho, khuda ko bhula kar tumhe dhoonda hai.", "urdu": "تمہیں چاہا ہے، تمہیں پوجا ہے،\nمیری حد تو دیکھو، خدا کو بھلا کر تمہیں ڈھونڈا ہے۔"},
    {"roman": "Woh mujhse pyar ka izhar kar rahe hain,\nMain unko dekh kar sharma raha hoon.", "urdu": "وہ مجھ سے پیار کا اظہار کر رہے ہیں،\nمیں ان کو دیکھ کر شرما رہا ہوں۔"},
    {"roman": "Tere ishq mein jalna bhi ibadat si lagti hai,\nTeri yaad mein marna bhi hasrat si lagti hai.", "urdu": "تیرے عشق میں جلنا بھی عبادت سی لگتی ہے،\nتیری یاد میں مرنا بھی حسرت سی لگتی ہے۔"},
    {"roman": "Meri aankhon mein teri tasveer hai,\nMere dil mein tera nasha hai.", "urdu": "میری آنکھوں میں تیری تصویر ہے،\nمیرے دل میں تیرا نشہ ہے۔"},
    {"roman": "Teri baahon mein jo sukoon mila,\nWoh kisi jannat mein bhi nahi milta.", "urdu": "تیری بانہوں میں جو سکون ملا،\nوہ کسی جنت میں بھی نہیں ملتا۔"},
    {"roman": "Kisi ko chahna gunah toh nahi,\nPar kisi ka ho jana aasan bhi nahi.", "urdu": "کسی کو چاہنا گناہ تو نہیں،\nپر کسی کا ہو جانا آسان بھی نہیں۔"},
    {"roman": "Waqt ke saath har zakham bhar jata hai,\nPar kuch nishaan dil mein hamesha rehte hain.", "urdu": "وقت کے ساتھ ہر زخم بھر جاتا ہے،\nپر کچھ نشان دل میں ہمیشہ رہتے ہیں۔"},
    {"roman": "Hum toh unke liye duniya bhula baithe,\nAur woh humein duniya ke liye bhula gaye.", "urdu": "ہم تو ان کے لیے دنیا بھلا بیٹھے،\nاور وہ ہمیں دنیا کے لیے بھلا گئے۔"},
    {"roman": "Dil tutne ki aawaz nahi hoti,\nBas ek dard hota hai jo bayan nahi hota.", "urdu": "دل ٹوٹنے کی آواز نہیں ہوتی،\nبس ایک درد ہوتا ہے جو بیان نہیں ہوتا۔"},
    {"roman": "Mujhe teri aadat si ho gayi hai,\nTere bina jeena mushkil si ho gayi hai.", "urdu": "مجھے تیری عادت سی ہو گئی ہے،\nتیرے بغیر جینا مشکل سی ہو گئی ہے۔"},
    {"roman": "Tere naam ki khushbu mere dil mein basi hai,\nJaise kisi ne phoolon ki khushbu chura li ho.", "urdu": "تیرے نام کی خوشبو میرے دل میں بسی ہے،\nجیسے کسی نے پھولوں کی خوشبو چرا لی ہو۔"},
    {"roman": "Mera har din teri yaad se shuru hota hai,\nAur teri yaad par khatam ho jata hai.", "urdu": "میرا ہر دن تیری یاد سے شروع ہوتا ہے،\nاور تیری یاد پر ختم ہو جاتا ہے۔"},
    {"roman": "Tere bina yeh zindagi adhoori si lagti hai,\nJaise koi kahani bina ending ke.", "urdu": "تیرے بغیر یہ زندگی ادھوری سی لگتی ہے،\nجیسے کوئی کہانی بنا اینڈنگ کے۔"},
    {"roman": "Woh kehte hain ke main badal gaya hoon,\nPar sach toh yeh hai ke main unke liye hi ruk gaya hoon.", "urdu": "وہ کہتے ہیں کہ میں بدل گیا ہوں،\nپر سچ تو یہ ہے کہ میں ان کے لیے ہی رک گیا ہوں۔"},
    {"roman": "Tere bina jo guzri hai raatein,\nUn raaton ka koi hisaab nahi.", "urdu": "تیرے بغیر جو گزری ہیں راتیں،\nان راتوں کا کوئی حساب نہیں۔"},
    {"roman": "Meri zindagi ki kitab mein,\nTum ek aisa safha ho jo hamesha yaad rahega.", "urdu": "میری زندگی کی کتاب میں،\nتم ایک ایسا صفحہ ہو جو ہمیشہ یاد رہے گا۔"},
    {"roman": "Kuch rishtay naam ke nahi hote,\nBas ehsaas hote hain jo dil mein rehte hain.", "urdu": "کچھ رشتے نام کے نہیں ہوتے،\nبس احساس ہوتے ہیں جو دل میں رہتے ہیں۔"},
    {"roman": "Tumse shikayat nahi hai koi,\nBas apne naseeb se gila hai.", "urdu": "تم سے شکایت نہیں ہے کوئی،\nبس اپنے نصیب سے گلہ ہے۔"},
    {"roman": "Jo dil mein basa hai,\nWoh nazar se door kaise ho sakta hai.", "urdu": "جو دل میں بسا ہے،\nوہ نظر سے دور کیسے ہو سکتا ہے۔"},
    {"roman": "Mujhe teri aadat hai,\nTere bina kya guzara hoga.", "urdu": "مجھے تیری عادت ہے،\nتیرے بغیر کیا گزارہ ہوگا۔"},
    {"roman": "Har mod par tumhara intezar karte hain,\nShayad kisi mod par tumse pyar ho jaye.", "urdu": "ہر موڑ پر تمہارا انتظار کرتے ہیں،\nشاید کسی موڑ پر تم سے پیار ہو جائے۔"},
    {"roman": "Teri muskurahat pe sab kuch qurban,\nTu bas muskura de toh jannat mil jaye.", "urdu": "تیری مسکراہٹ پر سب کچھ قربان،\nتو بس مسکرا دے تو جنت مل جائے۔"},
    {"roman": "Dil ke armaan aansuon mein beh gaye,\nHum wafa karte rahe aur woh bewafa kehlaye.", "urdu": "دل کے ارمان آنسوؤں میں بہہ گئے،\nہم وفا کرتے رہے اور وہ بے وفا کہلائے۔"},
    {"roman": "Kisi ka dil todna aasan hai,\nPar kisi ka dil jodna bohat mushkil hota hai.", "urdu": "کسی کا دل توڑنا آسان ہے،\nپر کسی کا دل جوڑنا بہت مشکل ہوتا ہے۔"},
    {"roman": "Meri chahat ko tumhari zaroorat samajh lo,\nYeh sirf ek hawas nahi, ibadat hai.", "urdu": "میری چاہت کو تمہاری ضرورت سمجھ لو،\nیہ صرف ایک ہوس نہیں، عبادت ہے۔"},
    {"roman": "Zindagi mein har cheez ka waqt hota hai,\nBas mohabbat ka koi waqt nahi hota.", "urdu": "زندگی میں ہر چیز کا وقت ہوتا ہے،\nبس محبت کا کوئی وقت نہیں ہوتا۔"},
    {"roman": "Tere naam se hi meri subah hoti hai,\nAur teri yaad se hi meri raat dhalti hai.", "urdu": "تیرے نام سے ہی میری صبح ہوتی ہے،\nاور تیری یاد سے ہی میری رات ڈھلتی ہے۔"},
    {"roman": "Mujhe teri baahon mein sukoon milta hai,\nJaise musafir ko apna ghar mil jaye.", "urdu": "مجھے تیری بانہوں میں سکون ملتا ہے،\nجیسے مسافر کو اپنا گھر مل جائے۔"},
    {"roman": "Kya batayein kis se kitna pyar hai,\nBas itna jaan lo ke tumhari yaad mein din guzar jata hai.", "urdu": "کیا بتائیں کس سے کتنا پیار ہے،\nبس اتنا جان لو کہ تمہاری یاد میں دن گزر جاتا ہے۔"},
    {"roman": "Aankhon mein teri tasveer liye baitha hoon,\nTere bina bhi tujh mein khoya hua hoon.", "urdu": "آنکھوں میں تیری تصویر لیے بیٹھا ہوں،\nتیرے بغیر بھی تجھ میں کھویا ہوا ہوں۔"},
    {"roman": "Mera dil tere naam ka ho gaya,\nJaise kisi ne mujhe teri yaadon ka tohfa de diya ho.", "urdu": "میرا دل تیرے نام کا ہو گیا،\nجیسے کسی نے مجھے تیری یادوں کا تحفہ دے دیا ہو۔"},
    {"roman": "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.", "urdu": "تمہاری باتوں میں وہ پیار ہے،\nجو کسی اور کی باتوں میں نہیں۔"},
    {"roman": "Mujhe tumhari aadat hai,\nTumse door rehna mujhse ho nahi sakta.", "urdu": "مجھے تمہاری عادت ہے،\nتم سے دور رہنا مجھ سے ہو نہیں سکتا۔"},
    {"roman": "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.", "urdu": "تیرے بغیر یہ دل سن سن سا ہے،\nجیسے بغیر بارش کے موسم سونا ہے۔"},
    {"roman": "Zindagi mein tum aaye toh kya hua,\nMeri toh zindagi hi badal gayi.", "urdu": "زندگی میں تم آئے تو کیا ہوا،\nمیری تو زندگی ہی بدل گئی۔"}
]

HASHTAGS = "#UrduShayari #UrduPoetry #RomanticShayari #LoveQuotes #Aesthetic #Trending #Viral #FYP #HinaFatima #Ishq #Mohabbat #CoupleGoals"

def process_and_post():
    font_path = download_font()
    image_url = random.choice(romantic_images)
    selected_shayari = random.choice(shayari_data)
    
    try:
        # 1. Image Download
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=10)
            img_response.raise_for_status()
            img = Image.open(io.BytesIO(img_response.content)).convert("RGBA")
        except Exception:
            img = Image.new('RGBA', (1080, 1080), (20, 20, 20, 255)) 
        
        # ✅ Premium Dark Gradient Overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        for i in range(img.height):
            alpha = int(160 * (i / img.height))
            draw_overlay.line([(0, i), (img.width, i)], fill=(0, 0, 0, alpha))
        
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 2. Roman Urdu Text on Image
        roman_text = selected_shayari["roman"]
        
        # 3. Text Auto-Fit
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
        
        # 4. Draw Roman Urdu Text (Center with Outline)
        draw.multiline_text(
            (x_center, y_center), 
            roman_text, 
            font=shairi_font, 
            fill="white", 
            anchor="mm", 
            align="center",
            stroke_width=4,
            stroke_fill="black"
        )
        
        # ✅ 5. Page Name (Premium Center Bottom Style)
        try:
            wm_font = ImageFont.truetype(font_path, 40)
        except:
            wm_font = ImageFont.load_default()
        
        draw.text(
            (img.width / 2, img.height - 80), 
            PAGE_NAME, 
            font=wm_font, 
            fill="white", 
            anchor="mm", 
            stroke_width=2, 
            stroke_fill="black"
        )
        
        image_path = "premium_shairi.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        # 6. Facebook Post
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        
        urdu_caption = selected_shayari["urdu"]
        caption = f"{urdu_caption}\n\nTag someone! ❤️\n\n{HASHTAGS}"
        
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

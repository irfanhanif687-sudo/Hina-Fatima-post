import os
import random
import requests
import io
import sys
from PIL import Image, ImageDraw, ImageFont

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')

PAGE_NAME = "Hina Fatima"

# ✅ 50+ High-Quality Romantic & Bold Aesthetic Pictures
romantic_images = [
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
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
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop"
]

# ✅ 100+ Bold, Romantic & Deep Shayari (Roman + Urdu)
shayari_data = [
    {"roman": "Mohabbat mein haar jana bhi ek jeet hai,\nKe dil ki duniya mein koi shikast nahi hoti.", "urdu": "محبت میں ہار جانا بھی ایک جیت ہے،\nکہ دل کی دنیا میں کوئی شکست نہیں ہوتی۔"},
    {"roman": "Tere bina yeh dil veeran sa lagta hai,\nJaise barish ke bina mausam sookha sa lagta hai.", "urdu": "تیرے بغیر یہ دل ویران سا لگتا ہے،\nجیسے بارش کے بغیر موسم سوکھا سا لگتا ہے۔"},
    {"roman": "Tum se mil kar laga jaise,\nZindagi mukammal ho gayi hai.", "urdu": "تم سے مل کر لگا جیسے،\nزندگی مکمل ہو گئی ہے۔"},
    {"roman": "Hum ne toh dil se chaha tha tujhe,\nPar tu ne toh aankhon se bhi na dekha.", "urdu": "ہم نے تو دل سے چاہا تھا تجھے،\nپر تو نے تو آنکھوں سے بھی نہ دیکھا۔"},
    {"roman": "Dil ki baat labon tak aati nahi,\nKyunke hum tujhe pareshan nahi karna chahte.", "urdu": "دل کی بات لبوں تک لاتی نہیں،\nکیونکہ ہم تجھے پریشان نہیں کرنا چاہتے۔"},
    {"roman": "Teri muskurahat pe sab kuch qurban,\nTu bas muskura de toh jannat mil jaye.", "urdu": "تیری مسکراہٹ پر سب کچھ قربان،\nتو بس مسکرا دے تو جنت مل جائے۔"},
    {"roman": "Mere khwabon mein har raat aata hai tu,\nJaise koi khushbu fiza mein bikharti hai.", "urdu": "میرے خوابوں میں ہر رات آتا ہے تو،\nجیسے کوئی خوشبو فضا میں بکھرتی ہے۔"},
    {"roman": "Tere naam se hi meri subah hoti hai,\nAur teri yaad se hi meri raat dhalti hai.", "urdu": "تیرے نام سے ہی میری صبح ہوتی ہے،\nاور تیری یاد سے ہی میری رات ڈھلتی ہے۔"},
    {"roman": "Mohabbat ki koi zubaan nahi hoti,\nBas ek ehsaas hota hai jo dil samajh leta hai.", "urdu": "محبت کی کوئی زبان نہیں ہوتی،\nبس ایک احساس ہوتا ہے جو دل سمجھ لیتا ہے۔"},
    {"roman": "Agar zindagi mein dobara mile,\nToh shayad tab bhi tujhe hi chahunga.", "urdu": "اگر زندگی میں دوبارہ ملے،\nتو شاید تب بھی تجھے ہی چاہوں گا۔"},
    {"roman": "Teri baahon mein aake mile sukoon,\nJaise musafir ko mil gaya ho apna makaan.", "urdu": "تیری بانہوں میں آ کے ملے سکون،\nجیسے مسافر کو مل گیا ہو اپنا مکاں۔"},
    {"roman": "Tere ishq ka nasha chadhta hi jata hai,\nTu paas aata hai toh dil dhadakta hi jata hai.", "urdu": "تیرے عشق کا نشہ چڑھتا ہی جاتا ہے،\nتو پاس آتا ہے تو دل دھڑکتا ہی جاتا ہے۔"},
    {"roman": "Ek nazar dekh kar tu door chala jata hai,\nMera dil tujhe dhoondta hi reh jata hai.", "urdu": "ایک نظر دیکھ کر تو دور چلا جاتا ہے،\nمیرا دل تجھے ڈھونڈتا ہی رہ جاتا ہے۔"},
    {"roman": "Tumhari baaton mein ek nasha hai,\nJo sharaab mein bhi nahi milta.", "urdu": "تمہاری باتوں میں ایک نشہ ہے،\nجو شراب میں بھی نہیں ملتا۔"},
    {"roman": "Teri aankhon ka jadoo chal gaya,\nMain toh bas tera hi ho gaya.", "urdu": "تیری آنکھوں کا جادو چل گیا،\nمیں تو بس تیرا ہی ہو گیا۔"},
    {"roman": "Ruth ke mujhse kahan jayega,\nTu toh mera naseeb hai,\nTujhe khud hi manana padega.", "urdu": "روٹھ کے مجھ سے کہاں جائے گا،\nتو تو میرا نصیب ہے،\nتجھے خود ہی منانا پڑے گا۔"},
    {"roman": "Ishq mein tere hadd se guzar gaye,\nTujhe chaha toh sab kuch bhula gaye.", "urdu": "عشق میں تیرے حد سے گزر گئے،\nتجھے چاہا تو سب کچھ بھلا گئے۔"},
    {"roman": "Tere bina yeh raatein kati nahi jaati,\nTeri yaad mein neendein aati nahi.", "urdu": "تیرے بغیر یہ راتیں کٹی نہیں جاتیں،\nتیری یاد میں نیندیں آتی نہیں۔"},
    {"roman": "Tere naam likh di hai zindagi apni,\nAb toh tu hi hai manzil meri.", "urdu": "تیرے نام لکھ دی ہے زندگی اپنی،\nاب تو تو ہی ہے منزل میری۔"},
    {"roman": "Tere pyar mein hum toh pagal ho gaye,\nTujhe dekha toh khud ko bhool gaye.", "urdu": "تیرے پیار میں ہم تو پاگل ہو گئے،\nتجھے دیکھا تو خود کو بھول گئے۔"},
    {"roman": "Mujhe teri aadat si ho gayi hai,\nTere bina jeena mushkil si ho gayi hai.", "urdu": "مجھے تیری عادت سی ہو گئی ہے،\nتیرے بغیر جینا مشکل سی ہو گئی ہے۔"},
    {"roman": "Tere naam ki khushbu mere dil mein basi hai,\nJaise kisi ne phoolon ki khushbu chura li ho.", "urdu": "تیرے نام کی خوشبو میرے دل میں بسی ہے،\nجیسے کسی نے پھولوں کی خوشبو چرا لی ہو۔"},
    {"roman": "Tumhari aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan milta hai.", "urdu": "تمہاری آنکھوں میں جو نشہ ہے،\nوہ کسی شراب میں کہاں ملتا ہے۔"},
    {"roman": "Mera har din teri yaad se shuru hota hai,\nAur teri yaad par khatam ho jata hai.", "urdu": "میرا ہر دن تیری یاد سے شروع ہوتا ہے،\nاور تیری یاد پر ختم ہو جاتا ہے۔"},
    {"roman": "Kisi ne kya khoob kaha hai,\nKe mohabbat ka matlab sirf dena hota hai, lena nahi.", "urdu": "کسی نے کیا خوب کہا ہے،\nکہ محبت کا مطلب صرف دینا ہوتا ہے، لینا نہیں۔"},
    {"roman": "Tere bina yeh zindagi adhoori si lagti hai,\nJaise koi kahani bina ending ke.", "urdu": "تیرے بغیر یہ زندگی ادھوری سی لگتی ہے،\nجیسے کوئی کہانی بنا اینڈنگ کے۔"},
    {"roman": "Mujhe dard bhi teri hi yaad dilata hai,\nAur sukoon bhi teri hi yaad se milta hai.", "urdu": "مجھے درد بھی تیری ہی یاد دلاتا ہے،\nاور سکون بھی تیری ہی یاد سے ملتا ہے۔"},
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
    {"roman": "Zindagi mein tum aaye toh kya hua,\nMeri toh zindagi hi badal gayi.", "urdu": "زندگی میں تم آئے تو کیا ہوا،\nمیری تو زندگی ہی بدل گئی۔"},
    {"roman": "Woh aaye toh mera dil khush ho gaya,\nJaise kisi ne phoolon ka guldasta bhej diya ho.", "urdu": "وہ آئے تو میرا دل خوش ہو گیا،\nجیسے کسی نے پھولوں کا گلدستہ بھیج دیا ہو۔"},
    {"roman": "Tere pyar mein hum toh pagal ho gaye,\nTujhe dekha toh khud ko bhool gaye.", "urdu": "تیرے پیار میں ہم تو پاگل ہو گئے،\nتجھے دیکھا تو خود کو بھول گئے۔"}
]

# ✅ Baaki 50+ Shayari (Total 100+)
shayari_data.extend([
    {"roman": "Ishq mein humne woh khoya hai,\nJo shayad kabhi mila hi nahi tha.", "urdu": "عشق میں ہم نے وہ کھویا ہے،\nجو شاید کبھی ملا ہی نہیں تھا۔"},
    {"roman": "Yeh raat, yeh tanhai, aur yeh chand,\nSab keh rahe hain ke tu door hai.", "urdu": "یہ رات، یہ تنہائی، اور یہ چاند،\nسب کہہ رہے ہیں کہ تو دور ہے۔"},
    {"roman": "Kabhi kabhi lagta hai,\nKe main khud se door ho gaya hoon.", "urdu": "کبھی کبھی لگتا ہے،\nکہ میں خود سے دور ہو گیا ہوں۔"},
    {"roman": "Dil ki baat labon tak aati nahi,\nKyunke hum unko pareshan nahi karna chahte.", "urdu": "دل کی بات لبوں تک آتی نہیں،\nکیونکہ ہم ان کو پریشان نہیں کرنا چاہتے۔"},
    {"roman": "Tumhari aankhon mein jo nasha hai,\nWoh kisi sharaab mein kahan milta hai.", "urdu": "تمہاری آنکھوں میں جو نشہ ہے،\nوہ کسی شراب میں کہاں ملتا ہے۔"},
    {"roman": "Mera har din teri yaad se shuru hota hai,\nAur teri yaad par khatam ho jata hai.", "urdu": "میرا ہر دن تیری یاد سے شروع ہوتا ہے،\nاور تیری یاد پر ختم ہو جاتا ہے۔"},
    {"roman": "Kisi ne kya khoob kaha hai,\nKe mohabbat ka matlab sirf dena hota hai, lena nahi.", "urdu": "کسی نے کیا خوب کہا ہے،\nکہ محبت کا مطلب صرف دینا ہوتا ہے، لینا نہیں۔"},
    {"roman": "Tere bina yeh zindagi adhoori si lagti hai,\nJaise koi kahani bina ending ke.", "urdu": "تیرے بغیر یہ زندگی ادھوری سی لگتی ہے،\nجیسے کوئی کہانی بنا اینڈنگ کے۔"},
    {"roman": "Mujhe dard bhi teri hi yaad dilata hai,\nAur sukoon bhi teri hi yaad se milta hai.", "urdu": "مجھے درد بھی تیری ہی یاد دلاتا ہے،\nاور سکون بھی تیری ہی یاد سے ملتا ہے۔"},
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
    {"roman": "Zindagi mein tum aaye toh kya hua,\nMeri toh zindagi hi badal gayi.", "urdu": "زندگی میں تم آئے تو کیا ہوا،\nمیری تو زندگی ہی بدل گئی۔"},
    {"roman": "Woh aaye toh mera dil khush ho gaya,\nJaise kisi ne phoolon ka guldasta bhej diya ho.", "urdu": "وہ آئے تو میرا دل خوش ہو گیا،\nجیسے کسی نے پھولوں کا گلدستہ بھیج دیا ہو۔"},
    {"roman": "Tere pyar mein hum toh pagal ho gaye,\nTujhe dekha toh khud ko bhool gaye.", "urdu": "تیرے پیار میں ہم تو پاگل ہو گئے،\nتجھے دیکھا تو خود کو بھول گئے۔"},
    {"roman": "Teri aankhon mein doob kar,\nHum kinara bhool gaye.", "urdu": "تیری آنکھوں میں ڈوب کر،\nہم کنارہ بھول گئے۔"},
    {"roman": "Tumhe chaha toh khud ko bhula diya,\nTumhe paya toh duniya bhula di.", "urdu": "تمہیں چاہا تو خود کو بھلا دیا،\nتمہیں پایا تو دنیا بھلا دی۔"},
    {"roman": "Mera dil tere ishq mein,\nAise doob gaya jaise patthar paani mein.", "urdu": "میرا دل تیرے عشق میں،\nایسے ڈوب گیا جیسے پتھر پانی میں۔"},
    {"roman": "Tere bina yeh dil,\nKisi aur ka ho hi nahi sakta.", "urdu": "تیرے بغیر یہ دل،\nکسی اور کا ہو ہی نہیں سکتا۔"},
    {"roman": "Teri baahon mein aake,\nMujhe sukoon mil gaya.", "urdu": "تیری بانہوں میں آ کے،\nمجھے سکون مل گیا۔"},
    {"roman": "Tere ishq ka nasha,\nChadhta hi jata hai.", "urdu": "تیرے عشق کا نشہ،\nچڑھتا ہی جاتا ہے۔"},
    {"roman": "Tere pyar mein hum,\nHad se guzar gaye.", "urdu": "تیرے پیار میں ہم،\nحد سے گزر گئے۔"},
    {"roman": "Tumhari baaton mein,\nEk nasha hai.", "urdu": "تمہاری باتوں میں،\nایک نشہ ہے۔"},
    {"roman": "Teri aankhon ka jadoo,\nChal gaya mujh par.", "urdu": "تیری آنکھوں کا جادو،\nچل گیا مجھ پر۔"},
    {"roman": "Ruth ke mujhse,\nKahan jayega tu.", "urdu": "روٹھ کے مجھ سے،\nکہاں جائے گا تو۔"},
    {"roman": "Tere bina yeh raatein,\nKati nahi jaati.", "urdu": "تیرے بغیر یہ راتیں،\nکٹی نہیں جاتیں۔"},
    {"roman": "Tere naam likh di,\nZindagi apni.", "urdu": "تیرے نام لکھ دی،\nزندگی اپنی۔"},
    {"roman": "Tere pyar mein hum,\nPagal ho gaye.", "urdu": "تیرے پیار میں ہم،\nپاگل ہو گئے۔"},
    {"roman": "Mujhe teri aadat,\nSi ho gayi hai.", "urdu": "مجھے تیری عادت،\nسی ہو گئی ہے۔"},
    {"roman": "Tere naam ki khushbu,\nMere dil mein basi hai.", "urdu": "تیرے نام کی خوشبو،\nمیرے دل میں بسی ہے۔"},
    {"roman": "Tumhari aankhon mein,\nJo nasha hai.", "urdu": "تمہاری آنکھوں میں،\nجو نشہ ہے۔"},
    {"roman": "Mera har din teri yaad,\nSe shuru hota hai.", "urdu": "میرا ہر دن تیری یاد،\nسے شروع ہوتا ہے۔"},
    {"roman": "Kisi ne kya khoob,\nKaha hai.", "urdu": "کسی نے کیا خوب،\nکہا ہے۔"},
    {"roman": "Tere bina yeh zindagi,\nAdhoori si lagti hai.", "urdu": "تیرے بغیر یہ زندگی،\nادھوری سی لگتی ہے۔"},
    {"roman": "Mujhe dard bhi teri,\nHi yaad dilata hai.", "urdu": "مجھے درد بھی تیری،\nہی یاد دلاتا ہے۔"},
    {"roman": "Woh kehte hain ke,\nMain badal gaya hoon.", "urdu": "وہ کہتے ہیں کہ،\nمیں بدل گیا ہوں۔"},
    {"roman": "Tere bina jo guzri,\nHai raatein.", "urdu": "تیرے بغیر جو گزری،\nہیں راتیں۔"},
    {"roman": "Meri zindagi ki kitab,\nMein tum ek safha ho.", "urdu": "میری زندگی کی کتاب،\nمیں تم ایک صفحہ ہو۔"},
    {"roman": "Kuch rishtay naam ke,\nNahi hote.", "urdu": "کچھ رشتے نام کے،\nنہیں ہوتے۔"},
    {"roman": "Tumse shikayat nahi,\nHai koi.", "urdu": "تم سے شکایت نہیں،\nہے کوئی۔"},
    {"roman": "Jo dil mein basa hai,\nWoh nazar se door kaise.", "urdu": "جو دل میں بسا ہے،\nوہ نظر سے دور کیسے۔"},
    {"roman": "Mujhe teri aadat hai,\nTere bina kya guzara hoga.", "urdu": "مجھے تیری عادت ہے،\nتیرے بغیر کیا گزارہ ہوگا۔"},
    {"roman": "Har mod par tumhara,\nIntezar karte hain.", "urdu": "ہر موڑ پر تمہارا،\nانتظار کرتے ہیں۔"},
    {"roman": "Teri muskurahat pe,\nSab kuch qurban.", "urdu": "تیری مسکراہٹ پر،\nسب کچھ قربان۔"},
    {"roman": "Dil ke armaan aansuon,\nMein beh gaye.", "urdu": "دل کے ارمان آنسوؤں،\nمیں بہہ گئے۔"},
    {"roman": "Kisi ka dil todna,\nAasan hai.", "urdu": "کسی کا دل توڑنا،\nآسان ہے۔"},
    {"roman": "Meri chahat ko tumhari,\nZaroorat samajh lo.", "urdu": "میری چاہت کو تمہاری،\nضرورت سمجھ لو۔"},
    {"roman": "Zindagi mein har cheez,\nKa waqt hota hai.", "urdu": "زندگی میں ہر چیز،\nکا وقت ہوتا ہے۔"},
    {"roman": "Tere naam se hi,\nMeri subah hoti hai.", "urdu": "تیرے نام سے ہی،\nمیری صبح ہوتی ہے۔"},
    {"roman": "Mujhe teri baahon,\nMein sukoon milta hai.", "urdu": "مجھے تیری بانہوں،\nمیں سکون ملتا ہے۔"},
    {"roman": "Kya batayein kis se,\nKitna pyar hai.", "urdu": "کیا بتائیں کس سے،\nکتنا پیار ہے۔"},
    {"roman": "Aankhon mein teri,\nTasveer liye baitha hoon.", "urdu": "آنکھوں میں تیری،\nتصویر لیے بیٹھا ہوں۔"},
    {"roman": "Mera dil tere naam,\nKa ho gaya.", "urdu": "میرا دل تیرے نام،\nکا ہو گیا۔"},
    {"roman": "Tumhari baaton mein,\nWoh pyar hai.", "urdu": "تمہاری باتوں میں،\nوہ پیار ہے۔"},
    {"roman": "Mujhe tumhari aadat hai,\nTumse door rehna mushkil hai.", "urdu": "مجھے تمہاری عادت ہے،\nتم سے دور رہنا مشکل ہے۔"},
    {"roman": "Tere bina yeh dil,\nSunn sa hai.", "urdu": "تیرے بغیر یہ دل،\nسن سن سا ہے۔"},
    {"roman": "Zindagi mein tum aaye,\nToh kya hua.", "urdu": "زندگی میں تم آئے،\nتو کیا ہوا۔"},
    {"roman": "Woh aaye toh mera,\nDil khush ho gaya.", "urdu": "وہ آئے تو میرا،\nدل خوش ہو گیا۔"},
    {"roman": "Tere pyar mein hum,\nToh pagal ho gaye.", "urdu": "تیرے پیار میں ہم،\nتو پاگل ہو گئے۔"},
    {"roman": "Teri aankhon mein doob,\nKar hum kinara bhool gaye.", "urdu": "تیری آنکھوں میں ڈوب،\nکر ہم کنارہ بھول گئے۔"},
    {"roman": "Tumhe chaha toh khud,\nKo bhula diya.", "urdu": "تمہیں چاہا تو خود،\nکو بھلا دیا۔"},
    {"roman": "Mera dil tere ishq,\nMein doob gaya.", "urdu": "میرا دل تیرے عشق،\nمیں ڈوب گیا۔"},
    {"roman": "Tere bina yeh dil,\nKisi aur ka ho hi nahi sakta.", "urdu": "تیرے بغیر یہ دل،\nکسی اور کا ہو ہی نہیں سکتا۔"},
    {"roman": "Teri baahon mein aake,\nMujhe sukoon mil gaya.", "urdu": "تیری بانہوں میں آ کے،\nمجھے سکون مل گیا۔"},
    {"roman": "Tere ishq ka nasha,\nChadhta hi jata hai.", "urdu": "تیرے عشق کا نشہ،\nچڑھتا ہی جاتا ہے۔"},
    {"roman": "Tere pyar mein hum,\nHad se guzar gaye.", "urdu": "تیرے پیار میں ہم،\nحد سے گزر گئے۔"},
    {"roman": "Tumhari baaton mein,\nEk nasha hai.", "urdu": "تمہاری باتوں میں،\nایک نشہ ہے۔"},
    {"roman": "Teri aankhon ka jadoo,\nChal gaya mujh par.", "urdu": "تیری آنکھوں کا جادو،\nچل گیا مجھ پر۔"},
    {"roman": "Ruth ke mujhse,\nKahan jayega tu.", "urdu": "روٹھ کے مجھ سے،\nکہاں جائے گا تو۔"},
    {"roman": "Tere bina yeh raatein,\nKati nahi jaati.", "urdu": "تیرے بغیر یہ راتیں،\nکٹی نہیں جاتیں۔"},
    {"roman": "Tere naam likh di,\nZindagi apni.", "urdu": "تیرے نام لکھ دی،\nزندگی اپنی۔"},
    {"roman": "Tere pyar mein hum,\nPagal ho gaye.", "urdu": "تیرے پیار میں ہم،\nپاگل ہو گئے۔"},
    {"roman": "Mujhe teri aadat,\nSi ho gayi hai.", "urdu": "مجھے تیری عادت،\nسی ہو گئی ہے۔"},
    {"roman": "Tere naam ki khushbu,\nMere dil mein basi hai.", "urdu": "تیرے نام کی خوشبو،\nمیرے دل میں بسی ہے۔"},
    {"roman": "Tumhari aankhon mein,\nJo nasha hai.", "urdu": "تمہاری آنکھوں میں،\nجو نشہ ہے۔"},
    {"roman": "Mera har din teri yaad,\nSe shuru hota hai.", "urdu": "میرا ہر دن تیری یاد،\nسے شروع ہوتا ہے۔"},
    {"roman": "Kisi ne kya khoob,\nKaha hai.", "urdu": "کسی نے کیا خوب،\nکہا ہے۔"},
    {"roman": "Tere bina yeh zindagi,\nAdhoori si lagti hai.", "urdu": "تیرے بغیر یہ زندگی،\nادھوری سی لگتی ہے۔"},
    {"roman": "Mujhe dard bhi teri,\nHi yaad dilata hai.", "urdu": "مجھے درد بھی تیری،\nہی یاد دلاتا ہے۔"},
    {"roman": "Woh kehte hain ke,\nMain badal gaya hoon.", "urdu": "وہ کہتے ہیں کہ،\nمیں بدل گیا ہوں۔"},
    {"roman": "Tere bina jo guzri,\nHai raatein.", "urdu": "تیرے بغیر جو گزری،\nہیں راتیں۔"},
    {"roman": "Meri zindagi ki kitab,\nMein tum ek safha ho.", "urdu": "میری زندگی کی کتاب،\nمیں تم ایک صفحہ ہو۔"},
    {"roman": "Kuch rishtay naam ke,\nNahi hote.", "urdu": "کچھ رشتے نام کے،\nنہیں ہوتے۔"},
    {"roman": "Tumse shikayat nahi,\nHai koi.", "urdu": "تم سے شکایت نہیں،\nہے کوئی۔"},
    {"roman": "Jo dil mein basa hai,\nWoh nazar se door kaise.", "urdu": "جو دل میں بسا ہے،\nوہ نظر سے دور کیسے۔"},
    {"roman": "Mujhe teri aadat hai,\nTere bina kya guzara hoga.", "urdu": "مجھے تیری عادت ہے،\nتیرے بغیر کیا گزارہ ہوگا۔"}
])

HASHTAGS = "#UrduShayari #UrduPoetry #UrduQuotes #SadShayari #RomanticShayari #LoveQuotes #Aesthetic #Trending #Viral #FYP #HinaFatima #BoldShayari #Ishq"

def process_and_post():
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
        
        # Dark overlay taake text saaf parha jaye
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 130))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
        
        # 2. Roman Urdu Text on Image
        roman_text = selected_shayari["roman"]
        
        # 3. Text Auto-Fit
        font_size = 65 
        max_width = img.width - 100   
        max_height = img.height - 400 
        
        while font_size > 15:
            try:
                shairi_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
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
        y_center = (img.height / 2) - 40 
        
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
        
        # ✅ 5. Page Name (Premium Center Bottom Style - No Box)
        try:
            wm_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 45)
        except:
            wm_font = ImageFont.load_default()
        
        # Neeche center mein text likhna (bina box ke, premium look)
        draw.text(
            (img.width / 2, img.height - 70), 
            PAGE_NAME, 
            font=wm_font, 
            fill="white", 
            anchor="mm", 
            stroke_width=3, 
            stroke_fill="black"
        )
        
        image_path = "urdu_shairi_post.jpg"
        img.convert("RGB").save(image_path, format="JPEG", quality=100)

        # 6. Facebook Post (Caption mein asli Urdu jayegi)
        print("Uploading to Facebook...")
        fb_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/photos"
        
        urdu_caption = selected_shayari["urdu"]
        caption = f"{urdu_caption}\n\nFollow for more beautiful shayari! ❤️\n\n{HASHTAGS}"
        
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

import os
import random
import requests
import sys
import subprocess
import time
import math
import wave
import struct
from datetime import datetime

PAGE_ID = os.environ.get('FB_PAGE_ID')
TOKEN = os.environ.get('FB_TOKEN')
PEXELS_KEY = os.environ.get('PEXELS_KEY')
API_VERSION = "v21.0"

REEL_SHAYARI = [
    "Teri baahon mein sukoon milta hai,\nJaise kisi ki dua qabool ho gayi ho.",
    "Tere bina yeh dil sunn sa hai,\nJaise bina baarish ke mausam soona hai.",
    "Tujhe dekh kar aise khoya main,\nJaise koi khwab dekh kar soya main.",
    "Ek tera saath chahiye, har khushi se pehle,\nEk teri yaad, sari duniya se pehle.",
    "Teri zulfon ki khushbu mein kho jata hoon,\nTere chehre ko dekhta hoon toh kho jata hoon.",
    "Tere ishq ki aag mein jalna acha lagta hai,\nTere liye har dard sehna acha lagta hai.",
    "Tujhe chahne ki koi hadd nahi,\nTere ishq ki koi hadd nahi.",
    "Tere paas aata hoon toh waqt ruk jata hai,\nTujhe chhod kar jata hoon toh dil ruk jata hai.",
    "Tumhari baaton mein woh pyar hai,\nJo kisi aur ki baaton mein nahi.",
    "Tere pyar mein hum toh aise doobe,\nJaise patthar paani mein doobta hai.",
    "Mera dil tere naam ka ho gaya,\nJaise teri yaadon ka tohfa mil gaya ho.",
    "Tumhi ko chaha hai, tumhi ko puja hai,\nDuniya ko bhula kar tumhe dhoonda hai.",
    "Tere ishq mein jalna bhi ibadat si lagti hai,\nTeri yaad mein jeena bhi hasrat si lagti hai.",
    "Meri aankhon mein teri tasveer hai,\nMere dil mein tera nasha hai.",
    "Teri baahon mein jo sukoon mila,\nWoh kisi jannat mein bhi nahi milta.",
    "Tere labon ki muskaan pe fida hoon,\nTeri har ada pe fida hoon.",
    "Raat bhar teri yaadon mein khoya rahoon,\nTere khwabon mein hi soya rahoon.",
    "Teri khushbu se hi meri saans chalti hai,\nTeri yaad se hi mujhe sukoon milta hai.",
    "Tere ishq mein hadd se guzar jayenge,\nTere liye duniya se lad jayenge.",
    "Mujhe teri aadat si nahi, junoon hai,\nTere bina jeena toh ek saza hai.",
    "Teri aankhon mein jo nasha hai,\nWoh kisi aur mein kahan.",
    "Dil chahta hai tujhe seene se laga loon,\nTeri yaadon mein hi kho jaoon.",
    "Tere naam se shuru, tere naam pe khatam,\nMeri kahani tu hi hai, mera anjaam tu hi hai.",
    "Chandni raat mein teri yaad aayi,\nDil ne phir teri tasveer banayi.",
    "Tum mile toh laga, dua qabool ho gayi,\nMeri har khushi ab tere naam ho gayi.",
    "Ishq tera meri jaan le gaya,\nTere bina jeena mushkil ho gaya.",
    "Teri ek muskaan pe sab kuch luta doon,\nTere liye apni jaan bhi de doon.",
    "Tere bina zindagi adhoori si lagti hai,\nTere saath har khushi poori si lagti hai.",
    "Teri yaadon ka chirag jalaye rakha hai,\nTere ishq ko dil mein basaye rakha hai.",
    "Tujhe dekhne ki hasrat har roz hai,\nTere bina jeena ek bojh hai.",
    "Meri duaon mein bas tera naam hai,\nMeri har khushi ka tu hi paigham hai.",
    "Tere chehre ki roshni se roshan hai jahan,\nTere bina andhera hai mera aasmaan.",
    "Teri muskaan meri duniya hai,\nTeri khushi meri manzil hai.",
    "Dil ne tujhe apna maan liya hai,\nTere bina jeena mushkil maan liya hai.",
    "Teri baatein sun kar dil khush ho jata hai,\nTera naam sun kar chehra khil jata hai.",
    "Tere ishq mein hum deewane ho gaye,\nTeri yaad mein hum parwane ho gaye.",
    "Tum jo mile toh laga zindagi mil gayi,\nTeri mohabbat mein har khushi mil gayi.",
    "Tere saath guzra har pal yaadgar hai,\nTeri yaad mein jeena hi mera pyar hai.",
    "Teri aankhon mein apna jahan dekhta hoon,\nTere chehre mein apna aasmaan dekhta hoon.",
    "Tujhe chahna meri aadat ban gayi,\nTeri yaad meri ibadat ban gayi.",
    "Mere dil ki dhadkan tu hi hai,\nMeri har khushi ka kaaran tu hi hai.",
    "Tere bina saans bhi bojh lagti hai,\nTere saath zindagi phool lagti hai.",
    "Teri yaad aaye toh dil muskurata hai,\nTera naam aaye toh chehra khil jata hai.",
    "Tujhe paane ki dua har roz karta hoon,\nTere liye khuda se fariyaad karta hoon.",
    "Tere pyar ka nasha chadha hua hai,\nMera dil tere naam pe likha hua hai.",
    "Teri ek jhalak ke liye tarasta hoon,\nTere deedar ke liye tarapta hoon.",
    "Tum meri duaon ka asar ho,\nTum meri mohabbat ka safar ho.",
    "Tere ishq ne mujhe jeena sikha diya,\nTeri yaad ne mujhe marna sikha diya.",
    "Dil ki har dhadkan mein tu basi hai,\nMeri har saans mein teri khushbu basi hai.",
    "Teri mohabbat mein khoya rehta hoon,\nTeri yaadon mein soya rehta hoon.",
    "Raat bhar teri baahon mein rehna chahta hoon,\nTeri saanson ki garmi mein kho jana chahta hoon.",
    "Tere honthon ki pyaas bujha doon,\nTujhe apni baahon mein sula doon.",
    "Teri gardan pe apne honth rakh doon,\nTeri har saans ko apna kar doon.",
    "Aaj raat tu paas aa ja,\nTere bina neend nahi aati mujhe.",
    "Tere seene se lag kar so jaoon,\nTeri dhadkan sun kar kho jaoon.",
    "Teri baahon ka takiya bana loon,\nTeri yaadon mein raat guzaar doon.",
    "Tujhe itna kareeb kar loon,\nKe saans bhi ek ho jaye hamari.",
    "Tere badan ki khushbu mujhe pagal kar deti hai,\nTeri ek nazar mujhe deewana kar deti hai.",
    "Raat ki tanhai mein tu yaad aati hai,\nTeri baahon ki kami bahut satati hai.",
    "Tere honthon pe apna naam likh doon,\nTeri har raat ko apni subah kar doon.",
    "Tujhe chhoo kar jo ehsaas hota hai,\nWoh jannat se bhi zyada khaas hota hai.",
    "Teri kamar pe haath rakh kar chalu,\nTujhe apni duniya bana loon.",
    "Aaj ki raat sirf teri ho jaoon,\nTere ishq mein poori tarah kho jaoon.",
    "Tere kaano mein dheere se keh doon,\nAaj raat tu meri hai, main tera hoon.",
    "Teri saans meri saans se takraye,\nAisa pyaar kabhi khatam na ho paye.",
    "Tujhe dekh kar dil beqabu ho jata hai,\nTere kareeb aate hi sab bhool jata hai.",
    "Teri zulfon mein ungliyaan phira doon,\nTeri har thakan ko mita doon.",
    "Tere honthon ki lali pe mar jaoon,\nTeri ek ada pe sab kuch waar jaoon.",
    "Raat ko jab tu paas hoti hai,\nMeri har dua qabool hoti hai.",
    "Tere seene ki dhadkan sunna chahta hoon,\nTujhe apni baahon mein rakhna chahta hoon.",
    "Tujhe itna pyaar doon ke tu sharma jaye,\nTeri har raat ko yaadgar bana jaye.",
    "Teri garmi mein pighal jaoon,\nTere ishq mein jal kar khaak ho jaoon.",
    "Aaj raat chandni mein tu aur main,\nBas pyaar ki baatein, aur koi nahi.",
    "Tere badan se lipat jaoon,\nTeri yaadon mein doob jaoon.",
    "Tujhe apne kareeb itna kar loon,\nKe duniya bhool jaye hum dono ko.",
    "Tere honthon ka nasha utarta hi nahi,\nTere bina dil kahin lagta hi nahi.",
    "Raat bhar tujhe dekhte rahoon,\nTeri baahon mein hi sote rahoon.",
    "Teri ek jhalak pe dil tadap jata hai,\nTere kareeb aate hi sab ruk jata hai.",
    "Tujhe seene se laga kar rakhoon,\nTeri har saans ko apna kar loon.",
    "Aaj raat tu mujhse door mat ja,\nTeri baahon mein hi sone de mujhe.",
    "Tere labon ki mithaas chakh loon,\nTeri har ada pe mar jaoon.",
    "Teri nazron ka jaadu chha gaya hai,\nMera dil tere naam ho gaya hai.",
    "Tujhe raat bhar pyaar karoon,\nTeri har khwahish ko poora karoon.",
    "Tere paas aate hi saans tez ho jati hai,\nTeri ek muskaan pe jaan nikal jati hai.",
    "Teri baahon mein jo aag hai,\nWoh kisi aur mein kahan.",
    "Tujhe apni god mein bitha loon,\nTeri zulfon ko sehla loon.",
    "Raat ki khamoshi mein sirf tu ho,\nAur meri baahon mein sirf tu ho.",
    "Tere ishq ka nasha sar chadha hai,\nTere bina dil kahin lagta nahi.",
    "Tujhe choom kar jo sukoon milta hai,\nWoh duniya mein kahin nahi milta.",
    "Teri saanson ki khushbu mein kho jaoon,\nTere pyaar mein doob jaoon.",
    "Aaj raat bas tu aur main,\nNa duniya, na koi parwah.",
    "Tere honthon se honth mila doon,\nTeri har pyaas ko bujha doon.",
    "Tujhe itna kareeb kar loon ke,\nTeri dhadkan meri dhadkan ban jaye.",
    "Teri baahon mein raat guzar jaye,\nTeri yaadon mein subah ho jaye.",
    "Tere badan ki garmi mujhe jala deti hai,\nTeri ek ada mujhe pagal kar deti hai.",
    "Tujhe pyaar karte karte raat ho jaye,\nTeri baahon mein hi subah ho jaye.",
    "Tere seene pe sar rakh kar so jaoon,\nTeri dhadkan sun kar kho jaoon.",
    "Tujhe dekh kar dil machal jata hai,\nTere kareeb aate hi sab badal jata hai.",
    "Raat bhar teri yaadon mein jalte rahe,\nTere ishq mein hum palte rahe.",
    "Teri ek raat ki khwahish hai mujhe,\nTeri baahon mein sone ki chahat hai mujhe.",
    "Teri chhat pe haath rakh ke so jaoon,\nTeri dhadkan ko apni lori bana loon.",
    "Tu jo sharma ke mere seene mein chhup jaye,\nMera dil or zor se dhadak jaye.",
    "Teri kamar ko pakad ke apne kareeb kar loon,\nTeri har saans ko apni bana loon.",
    "Aaj raat teri galiyon mein kho jaoon,\nTere honthon ki galiyon mein kho jaoon.",
    "Tere kaan ke peeche ek pyaar bhara kiss doon,\nTeri har thakan ko door kar doon.",
    "Tu jo mere honthon pe ungli rakh de,\nMeri saari baatein ruk jayen.",
    "Teri aankhon mein dekh ke lagta hai,\nJaise saari raat abhi baaki hai.",
    "Tujhe raat bhar apne seene se laga ke rakhoon,\nTeri garmi mein hi so jaoon.",
    "Tere honthon ki narmi ko mehsoos karoon,\nTeri har ada pe fida ho jaoon.",
    "Tu jab mere itne paas aati hai,\nMujhe apna aapa bhool jata hai.",
    "Teri saans jab mere chehre pe lagti hai,\nDil mein ek toofan sa uth jata hai.",
    "Aaj raat tujhe apni jaan bana loon,\nTere ishq mein poora doob jaoon.",
    "Tere badan ki har khushbu ko pee loon,\nTere pyaar mein khud ko bhool jaoon.",
    "Tujhe dekh ke dil kehta hai,\nKaash ye raat kabhi khatam na ho.",
    "Teri baahon mein aake lagta hai,\nJaise duniya ki har khushi mil gayi.",
    "Tu jo mere gaal pe haath phere,\nMera dil pighal jaye.",
    "Teri god mein sar rakh ke so jaoon,\nTeri ungliyon mein kho jaoon.",
    "Aaj raat tu meri baahon mein so ja,\nKal subah tak kahin mat ja.",
    "Tere honthon pe apni ungli phira doon,\nTeri har khamoshi ko samajh jaoon.",
    "Tujhe itna pyaar karoon ke tu thak jaye,\nPhir bhi mera dil na bhare.",
    "Teri raat wali khushbu mujhe pagal karti hai,\nTeri ek jhalak mujhe deewana karti hai.",
    "Tu jo hanste hue mere kareeb aaye,\nMera dil teri taraf khinch jaye.",
    "Tere seene ki garmi mein lipt jaoon,\nTeri yaadon mein hi mar jaoon.",
    "Aaj raat bas pyaar ki baarish ho,\nTu aur main, aur koi na ho.",
    "Tere honthon ka rang mere honthon pe lag jaye,\nAisa pyaar kabhi na mit paye.",
    "Tujhe baahon mein utha ke ghoom loon,\nTeri har muskaan ko choom loon.",
    "Teri neend mein bhi tujhe dekhta rahoon,\nTeri har saans ko ginta rahoon.",
    "Tu jo raat ko call pe dheere se bole,\nMera dil or zor se dhadak uthe.",
    "Tere pyaar mein raat bhar jaag loon,\nTeri yaadon mein hi so jaoon.",
    "Tujhe apne honthon se apna naam suna doon,\nTeri har raat ko apni bana loon.",
    "Teri kamar se lipat ke so jaoon,\nTeri khushbu mein hi kho jaoon.",
    "Aaj raat teri baahon ka nasha kar loon,\nTere ishq mein hi mar jaoon.",
    "Tu jo mere seene pe haath rakhe,\nMeri dhadkan teri ho jaye.",
    "Tere labon ki garmi ko mehsoos karoon,\nTeri har saans mein bas jaoon.",
    "Tujhe raat bhar apni aankhon mein rakhoon,\nTeri har ada ko yaad karoon.",
    "Teri ek raat ki mehmaan nawazi chahiye,\nTeri baahon mein sone ki ijazat chahiye.",
    "Tu jo paas aake mere kaan mein bole,\nMeri rooh tak kaamp jaye.",
    "Tere ishq mein raat din ek kar doon,\nTeri ek muskaan pe sab kuch kurban kar doon.",
    "Tujhe choom choom ke thak jaoon,\nPhir bhi tera pyaar na khatam ho.",
    "Aaj raat teri god mein duniya bhool jaoon,\nTere pyaar mein hi doob jaoon.",
]

HASHTAG_SETS = [
    "#UrduShayari #LoveShayari #HinaFatima #RomanticReels #DilKiBaat",
    "#RomanticReels #Ishq #Mohabbat #HinaFatima #TrendingReels",
    "#ShayariLovers #DilSe #LoveStatus #HinaFatima #ViralReels",
    "#SadShayari #IshqWalaLove #UrduPoetry #HinaFatima #ReelsViral",
    "#MohabbatShayari #Pyar #DilKiAwaaz #HinaFatima #Foryou",
    "#LovePoetry #ShayariVideo #RomanticShayari #HinaFatima #Explore",
    "#DilKaHaal #TeriYaad #IshqShayari #HinaFatima #ReelsInstagram",
    "#UrduLove #ShayariDaily #PyarMohabbat #HinaFatima #TrendingNow",
    "#HeartTouching #EmotionalShayari #LoveStory #HinaFatima #ViralVideo",
    "#ShayariStatus #RomanticStatus #DilKiBaat #HinaFatima #LoveReels",
    "#TeriYaad #DilKiBaat #RomanticShayari #HinaFatima #ForyouPage",
    "#LoveStory #IshqWala #UrduShayari #HinaFatima #ViralReels",
    "#PyarKiBaat #DilSeDil #ShayariReels #HinaFatima #ExplorePage",
    "#RomanticVibes #Tanhai #Mohabbat #HinaFatima #ReelsOfInstagram",
    "#IshqZada #DilKaDard #LoveShayari #HinaFatima #Trending",
    "#ShayariLover #RaatKiBaat #RomanticReels #HinaFatima #Viral",
    "#DilKiAwaaz #TeriMohabbat #UrduPoetry #HinaFatima #ReelsVideo",
    "#LoveQuotes #PyarMohabbat #Shayari #HinaFatima #ForYou",
    "#RomanticStatus #DilTootGaya #ShayariVideo #HinaFatima #TrendingReels",
    "#HinaFatima #IshqShayari #LoveReels #UrduShayari #DilKiBaat",
]

CTA_LINES = [
    "❤️ Follow karo - Roz raat ko nayi bold shayari ke liye, miss mat karna!",
    "🥰 Apne pyar ko tag karo + Follow karo - Roz aisi shayari ke liye",
    "💕 Comment mein ❤️ likho + Follow karo - Agli shayari tumhare naam hogi",
    "✨ Share karo apne special wale ke saath + Page ko Follow karo",
    "🔥 Follow kar lo - Roz 12 reels aati hain, ek bhi miss mat karo!",
    "❤️ Like + Follow - Agar ye shayari tumhare dil ki hai to",
    "👉 Follow nahi kiya to agli wali bold shayari miss ho jayegi!",
    "💔 Tag karo usko jiske liye ye shayari hai + Follow karo Hina Fatima ko",
    "🌙 Raat ki shayari ke liye Follow karo - Roz nayi feeling",
    "💌 Share + Follow - Apne pyar ko ye reel bhejo, wo khush ho jayega",
]

DHUN_LIST = [
    {"name": "Tone 1 - Sitar Slow Romantic", "raga": [261.63, 293.66, 329.63, 392.00, 440.00, 392.00, 329.63, 293.66], "tempo": 1.6, "sitar": 1.0, "bansuri": 0.0, "tabla": 1.0, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 2 - Bansuri Meethi Lambi", "raga": [293.66, 329.63, 392.00, 440.00, 523.25, 440.00, 392.00, 329.63], "tempo": 1.9, "sitar": 0.2, "bansuri": 1.0, "tabla": 0.3, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 3 - Harmonium + Tabla Shaadi", "raga": [261.63, 311.13, 329.63, 392.00, 466.16, 392.00, 329.63, 311.13], "tempo": 1.4, "sitar": 0.3, "bansuri": 0.2, "tabla": 1.0, "tanpura": 0.8, "harmonium": 1.0},
    {"name": "Tone 4 - Sitar + Bansuri Jodi", "raga": [329.63, 392.00, 440.00, 523.25, 587.33, 523.25, 440.00, 392.00], "tempo": 1.5, "sitar": 0.8, "bansuri": 0.8, "tabla": 0.6, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 5 - Raat Wali Udaas Sitar", "raga": [261.63, 293.66, 311.13, 392.00, 440.00, 392.00, 311.13, 293.66], "tempo": 2.1, "sitar": 1.0, "bansuri": 0.3, "tabla": 0.2, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 6 - Khushi Wali Tez Tabla", "raga": [329.63, 392.00, 440.00, 523.25, 659.25, 587.33, 523.25, 440.00], "tempo": 1.1, "sitar": 0.9, "bansuri": 0.4, "tabla": 1.0, "tanpura": 0.8, "harmonium": 0.3},
    {"name": "Tone 7 - Halki Bansuri Romantic", "raga": [293.66, 311.13, 392.00, 466.16, 523.25, 466.16, 392.00, 311.13], "tempo": 1.8, "sitar": 0.1, "bansuri": 1.0, "tabla": 0.4, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 8 - Full Band Sab Kuch", "raga": [261.63, 329.63, 392.00, 440.00, 523.25, 587.33, 659.25, 523.25], "tempo": 1.3, "sitar": 1.0, "bansuri": 0.9, "tabla": 1.0, "tanpura": 1.0, "harmonium": 0.6},
    {"name": "Tone 9 - Gehra Sitar Dard Bhara", "raga": [196.00, 261.63, 293.66, 329.63, 392.00, 329.63, 293.66, 261.63], "tempo": 2.0, "sitar": 1.0, "bansuri": 0.0, "tabla": 0.3, "tanpura": 1.0, "harmonium": 0.4},
    {"name": "Tone 10 - Bansuri Lambi Taan", "raga": [392.00, 440.00, 523.25, 587.33, 659.25, 587.33, 523.25, 440.00], "tempo": 2.2, "sitar": 0.0, "bansuri": 1.0, "tabla": 0.2, "tanpura": 1.0, "harmonium": 0.0},
    {"name": "Tone 11 - Harmonium Slow Mehfil", "raga": [261.63, 329.63, 392.00, 466.16, 523.25, 466.16, 392.00, 329.63], "tempo": 1.7, "sitar": 0.2, "bansuri": 0.2, "tabla": 0.7, "tanpura": 0.9, "harmonium": 1.0},
    {"name": "Tone 12 - Sitar Tez Ishq Josh", "raga": [329.63, 392.00, 523.25, 587.33, 659.25, 783.99, 659.25, 523.25], "tempo": 0.9, "sitar": 1.0, "bansuri": 0.3, "tabla": 1.0, "tanpura": 0.7, "harmonium": 0.2},
    {"name": "Tone 13 - Bansuri + Tabla Halki", "raga": [293.66, 392.00, 440.00, 523.25, 587.33, 523.25, 440.00, 392.00], "tempo": 1.6, "sitar": 0.1, "bansuri": 1.0, "tabla": 0.8, "tanpura": 0.9, "harmonium": 0.0},
    {"name": "Tone 14 - Tanpura Gehra + Sitar", "raga": [130.81, 196.00, 261.63, 329.63, 392.00, 329.63, 261.63, 196.00], "tempo": 1.8, "sitar": 0.9, "bansuri": 0.2, "tabla": 0.4, "tanpura": 1.0, "harmonium": 0.3},
    {"name": "Tone 15 - Shaam Wali Dhun", "raga": [261.63, 293.66, 329.63, 392.00, 466.16, 523.25, 466.16, 392.00], "tempo": 1.5, "sitar": 0.7, "bansuri": 0.7, "tabla": 0.5, "tanpura": 1.0, "harmonium": 0.5},
    {"name": "Tone 16 - Subah Wali Halki Dhun", "raga": [329.63, 392.00, 440.00, 523.25, 440.00, 392.00, 329.63, 293.66], "tempo": 1.9, "sitar": 0.4, "bansuri": 0.9, "tabla": 0.3, "tanpura": 0.8, "harmonium": 0.4},
    {"name": "Tone 17 - Dard Bhari Sitar Slow", "raga": [220.00, 261.63, 311.13, 392.00, 440.00, 392.00, 311.13, 261.63], "tempo": 2.3, "sitar": 1.0, "bansuri": 0.4, "tabla": 0.1, "tanpura": 1.0, "harmonium": 0.2},
    {"name": "Tone 18 - Pyar Bhari Bansuri Fast", "raga": [392.00, 466.16, 523.25, 587.33, 659.25, 783.99, 659.25, 587.33], "tempo": 1.2, "sitar": 0.3, "bansuri": 1.0, "tabla": 0.7, "tanpura": 0.9, "harmonium": 0.0},
    {"name": "Tone 19 - Dholak + Harmonium Masti", "raga": [261.63, 329.63, 392.00, 440.00, 523.25, 440.00, 392.00, 329.63], "tempo": 1.0, "sitar": 0.3, "bansuri": 0.3, "tabla": 1.0, "tanpura": 0.7, "harmonium": 1.0},
    {"name": "Tone 20 - Sabse Romantic Sitar Bansuri Tanpura", "raga": [293.66, 329.63, 392.00, 440.00, 523.25, 587.33, 523.25, 440.00], "tempo": 1.4, "sitar": 1.0, "bansuri": 1.0, "tabla": 0.6, "tanpura": 1.0, "harmonium": 0.5},
]

def get_shayari_for_this_slot():
    now = datetime.now()
    slot = (now.day * 100 + now.hour * 2 + (1 if now.minute >= 30 else 0))
    index = slot % len(REEL_SHAYARI)
    return REEL_SHAYARI[index]

def get_dhun_for_this_slot():
    now = datetime.now()
    slot = (now.day * 100 + now.hour * 2 + (1 if now.minute >= 30 else 0))
    dhun = DHUN_LIST[slot % len(DHUN_LIST)]
    return dhun

def get_hashtags_and_cta():
    now = datetime.now()
    slot = (now.day * 100 + now.hour * 2 + (1 if now.minute >= 30 else 0))
    hashtags = HASHTAG_SETS[slot % len(HASHTAG_SETS)]
    cta = CTA_LINES[slot % len(CTA_LINES)]
    return hashtags, cta

def wrap_line(line, max_chars=26):
    words = line.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur + " " + w) <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def make_text_image(shayari_text):
    from PIL import Image, ImageDraw, ImageFont
    video_text = shayari_text.replace(",", "").replace(".", "").replace("?", "").replace("!", "")
    wrapped = []
    for part in video_text.split("\n"):
        wrapped.extend(wrap_line(part.strip()))
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = None
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "Poppins-Bold.ttf"]:
        try:
            font = ImageFont.truetype(p, 52)
            break
        except:
            continue
    if font is None:
        font = ImageFont.load_default()
    y = 730
    for line in wrapped:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (1080 - w) // 2
        for dx, dy in [(-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)]:
            draw.text((x+dx, y+dy), line, font=font, fill=(0,0,0,255))
        draw.text((x, y), line, font=font, fill=(255,255,255,255))
        y += 70
    img.save("shayari_overlay.png")
    print(f"✅ Text image ban gayi: {wrapped}")
    return "shayari_overlay.png"

# ✅ FIXED - Ab dhun TEZ aur SAAF hogi, pehle wali halki/ajeeb wali nahi
def make_local_indian_music():
    dhun = get_dhun_for_this_slot()
    print(f"✅ Dhun bana raha hoon: {dhun['name']}")
    try:
        for f in ["background.mp3", "background.wav"]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        sample_rate = 44100
        duration = 15
        total = sample_rate * duration
        notes = dhun["raga"]
        tempo = dhun["tempo"]
        samples = [0.0] * total

        # Tanpura - ab tez
        if dhun["tanpura"] > 0:
            for i in range(total):
                t = i / sample_rate
                drone = (0.25 * math.sin(2 * math.pi * 130.81 * t) + 0.18 * math.sin(2 * math.pi * 196.00 * t) + 0.10 * math.sin(2 * math.pi * 261.63 * t)) * dhun["tanpura"]
                samples[i] += drone

        note_len = int(sample_rate * tempo)
        pos = 0
        idx = 0
        while pos < total:
            freq = notes[idx % len(notes)]
            idx += 1
            for i in range(note_len):
                if pos + i >= total:
                    break
                t = i / sample_rate
                # FIX: Pehle decay 2.2 tha, is liye awaaz turant khatam ho jati thi. Ab 0.9 hai.
                decay = math.exp(-t * 0.9)
                vib = 1 + 0.006 * math.sin(2 * math.pi * 5.5 * t)
                f = freq * vib
                if dhun["sitar"] > 0:
                    # FIX: Pehle volume 0.55 tha, ab 1.2 hai - 2x se zyada tez
                    sitar_val = (1.2 * math.sin(2 * math.pi * f * t) + 0.7 * math.sin(2 * math.pi * f * 2 * t) + 0.4 * math.sin(2 * math.pi * f * 3 * t) + 0.2 * math.sin(2 * math.pi * f * 5 * t)) * decay * dhun["sitar"]
                    samples[pos + i] += sitar_val
                if dhun["bansuri"] > 0:
                    bansuri_val = (1.1 * math.sin(2 * math.pi * f * 0.5 * t) + 0.6 * math.sin(2 * math.pi * f * t)) * math.exp(-t * 0.5) * dhun["bansuri"]
                    samples[pos + i] += bansuri_val
                if dhun.get("harmonium", 0) > 0:
                    harm_val = (0.9 * math.sin(2 * math.pi * f * t) + 0.5 * math.sin(2 * math.pi * f * 1.5 * t) + 0.3 * math.sin(2 * math.pi * f * 2 * t)) * math.exp(-t * 0.6) * dhun["harmonium"]
                    samples[pos + i] += harm_val
            pos += note_len

        if dhun["tabla"] > 0:
            tabla_interval = int(sample_rate * 0.75)
            for start in range(0, total, tabla_interval):
                for i in range(int(sample_rate * 0.12)):
                    if start + i >= total:
                        break
                    t = i / sample_rate
                    # FIX: Tabla bhi ab 2x tez - pehle 0.35 tha
                    thump = 0.7 * math.sin(2 * math.pi * 120 * t) * math.exp(-t * 25) * dhun["tabla"]
                    samples[start + i] += thump
                for i in range(int(sample_rate * 0.06)):
                    if start + int(sample_rate * 0.35) + i >= total:
                        break
                    t = i / sample_rate
                    tick = 0.35 * math.sin(2 * math.pi * 1800 * t) * math.exp(-t * 35) * dhun["tabla"]
                    samples[start + int(sample_rate * 0.35) + i] += tick

        max_val = max(abs(s) for s in samples) or 1
        # FIX: Pehle scale 16000 / 1.2 pe rok diya tha, is liye halki thi. Ab full 30000
        scale = 30000 / max_val
        int_samples = [int(max(-32767, min(32767, s * scale))) for s in samples]
        data = b''.join(struct.pack('<h', s) for s in int_samples)
        with wave.open("background.wav", "w") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(data)

        wav_size = os.path.getsize("background.wav")
        print(f"✅ Dhun Ready WAV - TEZ WALI: {dhun['name']} - {wav_size} bytes")
        if wav_size < 100000:
            print("❌ WAV file bahut choti hai, kharab bani hai!")
            return None
        # FIX: mp3 convert nahi karna, seedha wav return - is liye FFmpeg wav->mp3 fail nahi aayega
        return "background.wav"
    except Exception as e:
        print(f"Local music fail: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_random_reel_video():
    print("Fetching video from Pexels - AUTO...")
    if not PEXELS_KEY:
        print("❌ PEXELS_KEY missing hai!")
        sys.exit(1)
    queries = ["romantic couple", "couple in love", "couple holding hands", "couple sunset", "couple hug romantic"]
    headers = {"Authorization": PEXELS_KEY}
    params = {"query": random.choice(queries), "per_page": 15, "orientation": "portrait", "size": "medium"}
    try:
        res = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params, timeout=20)
        print(f" Pexels Status: {res.status_code}")
        res.raise_for_status()
        videos = res.json().get('videos', [])
        if not videos:
            print("❌ Pexels ne video nahi diya")
            sys.exit(1)
        selected = random.choice(videos)
        files = selected.get('video_files', [])
        if not files:
            print("❌ Video files empty")
            sys.exit(1)
        suitable = [f for f in files if 700 <= f.get('height', 0) <= 1080]
        if suitable:
            best = random.choice(suitable)
        else:
            best = sorted(files, key=lambda x: x.get('height', 0))[0]
        print(f"Found video: {best.get('link')} height={best.get('height')}")
        return best.get('link')
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        sys.exit(1)

def make_final_reel(video_url, shayari_text, music_path):
    if not music_path or not os.path.exists(music_path):
        print("❌ SONG NAHI MILA, REEL NAHI BANA RAHA")
        sys.exit(1)
    raw_path = "raw_reel.mp4"
    print("Downloading raw video...")
    with requests.get(video_url, stream=True, timeout=45) as r:
        r.raise_for_status()
        with open(raw_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Raw size: {os.path.getsize(raw_path)} bytes")
    overlay = make_text_image(shayari_text)
    final_path = "final_reel.mp4"
    print(f"Adding DHUN: {music_path} - size {os.path.getsize(music_path)}")
    # FIX: Pehle volume=0.9 + lowpass tha, is liye awaaz dab jati thi. Ab volume=1.8, lowpass khatam.
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[v];"
        "[v][1:v]overlay=0:0[outv];"
        "[2:a]volume=1.8,afade=t=in:st=0:d=0.5,afade=t=out:st=14:d=1[outa]"
    )
    cmd = ["ffmpeg", "-y",
           "-i", raw_path,
           "-i", overlay,
           "-stream_loop", "-1", "-i", music_path,
           "-filter_complex", filter_complex,
           "-map", "[outv]", "-map", "[outa]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
           "-c:a", "aac", "-t", "15", final_path]
    print("Running FFmpeg final...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ FFmpeg Final Error - POORA ERROR:")
        print(result.stderr)
        sys.exit(1)
    print(f"✅ Final Reel Ready: {os.path.getsize(final_path)} bytes")
    return final_path

def upload_reel_to_facebook(video_path, caption):
    file_size = os.path.getsize(video_path)
    if file_size < 100000:
        print("❌ Video bahut choti hai")
        sys.exit(1)
    print("Starting Facebook Reel upload...")
    start_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        start_res = requests.post(start_url, data={"upload_phase": "start", "access_token": TOKEN}, timeout=20)
        print(f"Start Status: {start_res.status_code}")
        start_res.raise_for_status()
        start_data = start_res.json()
        video_id = start_data["video_id"]
        upload_url = start_data["upload_url"]
        print(f"Session started: {video_id}")
    except Exception as e:
        print(f"❌ Start failed: {e}")
        if 'start_res' in locals():
            print(start_res.text)
        sys.exit(1)
    print("Uploading file...")
    try:
        with open(video_path, 'rb') as f:
            upload_res = requests.post(upload_url, headers={"Authorization": f"OAuth {TOKEN}", "offset": "0", "file_size": str(file_size)}, data=f, timeout=120)
        print(f"Upload Status: {upload_res.status_code}")
        upload_res.raise_for_status()
        print("✅ File uploaded")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)
    time.sleep(8)
    print("Publishing...")
    finish_url = f"https://graph.facebook.com/{API_VERSION}/{PAGE_ID}/video_reels"
    try:
        finish_res = requests.post(finish_url, data={
            "access_token": TOKEN, "video_id": video_id,
            "upload_phase": "finish", "video_state": "PUBLISHED",
            "description": caption
        }, timeout=30)
        print(f"Finish Status: {finish_res.status_code}")
        print(finish_res.text[:500])
        finish_res.raise_for_status()
        print(f"✅ REEL POST SUCCESS! ID: {finish_res.json().get('id')}")
    except Exception as e:
        print(f"❌ Finish failed: {e}")
        if 'finish_res' in locals():
            print(finish_res.text)
        sys.exit(1)

if __name__ == "__main__":
    if not PAGE_ID or not TOKEN:
        print("❌ FB_PAGE_ID ya FB_TOKEN missing!")
        sys.exit(1)
    shayari = get_shayari_for_this_slot()
    dhun = get_dhun_for_this_slot()
    hashtags, cta = get_hashtags_and_cta()
    caption = f"{shayari}\n\n{cta}\n\n{hashtags}"
    print(f"Selected Shayari: {shayari}")
    print(f"Selected Dhun: {dhun['name']}")
    print(f"Hashtags: {hashtags}")
    print(f"CTA: {cta}")
    music = make_local_indian_music()
    if not music:
        print("❌ SONG NAHI BANA - Reel post nahi hogi")
        sys.exit(1)
    video_url = get_random_reel_video()
    final_video = make_final_reel(video_url, shayari, music)
    upload_reel_to_facebook(final_video, caption)

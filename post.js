const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Funny Comments
const funnyComments = [
    "Yeh expression dekh ke toh meri hasi nahi ruk rahi 😂😂",
    "Kya acting hai waise! 🔥",
    "Ammi ne pakka yeh scene nahi dekhna chahiye tha 🤣",
    "Is drama ne toh hadd kar di hai yaar 😭",
    "Background music toh kamaal ka tha 🎵",
    "Guys, yeh kaunsa drama hai? 😅",
    "Mujhe toh bas yeh jodi pasand hai ❤️",
    "Yeh dialogue delivery toh kamaal ki hai! 👏",
    "Ek episode dekh ke hi pata chal gaya ending kya hogi 😅",
    "Koi batao yeh actress kaun hai? 🤔",
    "Iska makeup toh kamaal ka hai 💄✨",
    "Aankhon se hi sab keh diya isne 👀❤️",
    "Mashallah, kitni pyari lag rahi hain! 🥰",
    "Ekdum natural beauty hai yaar 🌸"
];

// ✅ ASLI PAKISTANI ACTRESSES KI DIRECT HD IMAGE LINKS (Wikimedia Original Files)
const dramaActressPics = [
    "https://upload.wikimedia.org/wikipedia/commons/3/3e/Mahira_Khan.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2c/Hania_Aamir.png",
    "https://upload.wikimedia.org/wikipedia/commons/a/ae/Yumna_Zaidi.png",
    "https://upload.wikimedia.org/wikipedia/commons/c/ce/Saba_Qamar_%28cropped%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/c/c5/Mehwish_Hayat.PNG",
    "https://upload.wikimedia.org/wikipedia/commons/1/15/Pakistani_Actress_Sanam_Saeed.jpg"
];

async function publishPost() {
    try {
        const randomPic = dramaActressPics[Math.floor(Math.random() * dramaActressPics.length)];
        const randomComment = funnyComments[Math.floor(Math.random() * funnyComments.length)];
        
        console.log("Posting Actress Picture:", randomPic);
        console.log("With Comment:", randomComment);

        // ✅ Yahan User-Agent header add kiya gaya hai (Hotlink Protection bypass ke liye)
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: randomPic,         
                caption: randomComment, 
                access_token: TOKEN
            },
            {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            }
        );
        
        console.log("✅ Post Success! ID:", response.data.id);
    } catch (error) {
        console.error("❌ Error aagaya:");
        if (error.response) {
            console.error(JSON.stringify(error.response.data, null, 2));
        } else {
            console.error(error.message);
        }
        process.exit(1);
    }
}

publishPost();

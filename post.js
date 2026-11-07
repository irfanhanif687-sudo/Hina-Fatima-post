const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Funny Comments ki Categories
const comments = {
    makeup: [
        "Iska makeup toh kamaal ka hai 💄✨",
        "Itna highlighter lagaya hai ke face chamak raha hai ✨",
        "Contour kahan se seekha hai waise? 🤔",
        "Lipstick ka shade toh ekdum perfect hai 💋",
        "Naya look, nayi vibe 💅",
        "Ye dress aur makeup ekdum match kar raha hai! 🔥"
    ],
    expression: [
        "Yeh expression dekh ke toh meri hasi nahi ruk rahi 😂😂",
        "Kya acting hai waise! 🔥",
        "Iska expression toh ekdum 'Ammi ne daant di hai' wala hai 🤣",
        "Aankhon se hi sab keh diya isne 👀❤️",
        "Yeh look dekh ke toh mera din ban gaya 😍",
        "Iske expressions toh award jeetne wale hain! 🏆"
    ],
    cute: [
        "Kya cute lag rahi hai yaar! ❤️",
        "Aaj kal ki actresses toh ek se badh kar ek hain ✨",
        "Yeh style toh sabki favourite hai 💃",
        "Iska smile toh dil le gaya 😊",
        "Ekdum natural beauty hai yaar 🌸",
        "Mashallah, kitni pyari lag rahi hain! 🥰"
    ],
    general: [
        "Guys, yeh kaunsa drama hai? 😅",
        "Koi batao yeh actress kaun hai? 🤔",
        "Pakistani dramas > Indian dramas (Kabhi kabhi) 😉",
        "Ek episode dekh ke hi pata chal gaya ending kya hogi 😅",
        "Background music toh kamaal ka tha 🎵",
        "Aaj kal ke dramas mein bas rona hi rona hai 😭",
        "Isko dekh ke toh drama dekhne ka dil kar gaya 📺"
    ]
};

// ASLI PAKISTANI DRAMA ACTRESSES KI HD PICTURES (Wikipedia se direct links)
const dramaActressPics = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Sajal_Aly_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Sajal_Aly_at_Hum_Style_Awards_%28cropped%29.jpg", // Sajal Aly
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Mahira_Khan_at_Lux_Style_Awards_%282%29_%28cropped%29.jpg/800px-Mahira_Khan_at_Lux_Style_Awards_%282%29_%28cropped%29.jpg", // Mahira Khan
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Ayeza_Khan_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Ayeza_Khan_at_Hum_Style_Awards_%28cropped%29.jpg", // Ayeza Khan
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Hania_Aamir_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Hania_Aamir_at_Hum_Style_Awards_%28cropped%29.jpg", // Hania Aamir
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Yumna_Zaidi_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Yumna_Zaidi_at_Hum_Style_Awards_%28cropped%29.jpg", // Yumna Zaidi
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Iqra_Aziz_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Iqra_Aziz_at_Hum_Style_Awards_%28cropped%29.jpg", // Iqra Aziz
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Mawra_Hocane_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Mawra_Hocane_at_Hum_Style_Awards_%28cropped%29.jpg", // Mawra Hocane
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Saba_Qamar_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Saba_Qamar_at_Hum_Style_Awards_%28cropped%29.jpg", // Saba Qamar
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Mehwish_Hayat_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Mehwish_Hayat_at_Hum_Style_Awards_%28cropped%29.jpg", // Mehwish Hayat
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Sanam_Saeed_at_Hum_Style_Awards_%28cropped%29.jpg/800px-Sanam_Saeed_at_Hum_Style_Awards_%28cropped%29.jpg"  // Sanam Saeed
];

async function publishPost() {
    try {
        // 1. Random HD picture uthao
        const randomPic = dramaActressPics[Math.floor(Math.random() * dramaActressPics.length)];

        // 2. Random category aur comment uthao
        const categories = Object.keys(comments);
        const randomCategory = categories[Math.floor(Math.random() * categories.length)];
        const categoryComments = comments[randomCategory];
        const randomComment = categoryComments[Math.floor(Math.random() * categoryComments.length)];
        
        console.log("Posting Actress Picture:", randomPic);
        console.log("With Comment:", randomComment);

        // 3. Facebook par post karo
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: randomPic,         
                caption: randomComment, 
                access_token: TOKEN
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

const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Funny Comments ki list
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
    "Koi batao yeh actress kaun hai? 🤔"
];

// ✅ RELIABLE IMAGE SOURCE
// Yeh link hamesha kaam karega kyunke yeh ek fixed image hai
const dramaPics = [
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop"
];

async function publishPost() {
    try {
        // 1. Random picture select karo
        const randomPic = dramaPics[Math.floor(Math.random() * dramaPics.length)];

        // 2. Random funny comment select karo
        const randomComment = funnyComments[Math.floor(Math.random() * funnyComments.length)];
        
        console.log("Posting Picture:", randomPic);
        console.log("With Comment:", randomComment);

        // 3. Facebook par post karo
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: randomPic,         // Valid image link
                caption: randomComment, // Funny Comment
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

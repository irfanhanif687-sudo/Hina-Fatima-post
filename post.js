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

async function publishPost() {
    try {
        // 1. Internet se ek random funny/portrait image uthao
        // Hum 'thispersondoesnotexist.com' use kar rahe hain jo random face deta hai, 
        // ya Unsplash ka random portrait source use kar sakte hain.
        // Yahan humne direct source use kiya hai jo har call pe nayi image deta hai:
        const randomPic = "https://source.unsplash.com/random/1080x1080/?portrait,woman,expressions";

        // 2. Random funny comment select karo
        const randomComment = funnyComments[Math.floor(Math.random() * funnyComments.length)];
        
        console.log("Image URL:", randomPic);
        console.log("Comment:", randomComment);

        // 3. Facebook par post karo
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: randomPic,         // Image ka direct link
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

const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// 1. Funny Comments ki List (Tum apne hisaab se aur add kar sakte ho)
const funnyComments = [
    "Yeh scene dekh ke meri hasi nahi ruk rahi 😂",
    "Kya acting hai waise! 🔥",
    "Aaj kal ke dramas mein bas rona hi rona hai 😭",
    "Ye character mujhe bilkul pasand nahi aaya 🤦‍♂️",
    "Pakistani dramas > Indian dramas (Kabhi kabhi) 😉",
    "Ammi ne pakka yeh scene nahi dekhna chahiye tha 🤣",
    "Background music toh kamaal ka tha 🎵",
    "Guys, is drama ka naam kya hai?",
    "Ek episode dekh ke hi pata chal gaya ending kya hogi 😅",
    "Mujhe toh bas yeh jodi pasand hai ❤️"
];

// 2. Image URL (Abhi ke liye ek high-quality random image use kar rahe hain)
// Baad mein tum yahan apni drama pics ke links dal sakte ho
const imageUrl = "https://picsum.photos/1080/1080";

async function publishPost() {
    // Random comment select karo
    const randomComment = funnyComments[Math.floor(Math.random() * funnyComments.length)];
    console.log("Aaj ka comment:", randomComment);

    try {
        // Step 1: Pehle image upload karo (Facebook ko image URL chahiye hota hai post karne ke liye)
        // Note: Graph API mein direct URL se post karne ke liye 'link' use hota hai ya 'source' se image upload hoti hai.
        // Aasaan tareeqa yeh hai ke hum direct 'link' mein image ka URL de dein aur caption mein comment.
        
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: imageUrl,          // Image ka link
                caption: randomComment, // Neeche likha hua comment
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

const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Comments ki Categories (Vibe ke hisaab se)
const comments = {
    makeup: [
        "Iska makeup se zyada toh meri behen ka makeup acha hai 💄😂",
        "Itna highlighter lagaya hai ke face chamak raha hai ✨",
        "Contour kahan se seekha hai waise? 🤔",
        "Lipstick ka shade toh kamaal ka hai 💋",
        "Naye drama ki nayi actress, naya makeup look 💅"
    ],
    expression: [
        "Yeh expression dekh ke toh meri hasi nahi ruk rahi 😂😂",
        "Kya acting hai waise! 🔥",
        "Iska expression toh ekdum 'Ammi ne daant di hai' wala hai 🤣",
        "Bhai yeh actress toh har drama mein same acting karti hai 🤦‍♂️",
        "Aankhon se hi sab keh diya isne 👀❤️",
        "Yeh look dekh ke toh mera din ban gaya 😍"
    ],
    cute: [
        "Kya cute lag rahi hai yaar! ❤️",
        "Mujhe toh bas yeh jodi pasand hai 🥰",
        "Aaj kal ki actresses toh ek se badh kar ek hain ✨",
        "Yeh style toh sabki favourite hai 💃",
        "Iska smile toh dil le gaya 😊"
    ],
    general: [
        "Guys, yeh kaunsa drama hai? 😅",
        "Koi batao yeh actress kaun hai? 🤔",
        "Pakistani dramas > Indian dramas (Kabhi kabhi) 😉",
        "Ek episode dekh ke hi pata chal gaya ending kya hogi 😅",
        "Background music toh kamaal ka tha 🎵",
        "Aaj kal ke dramas mein bas rona hi rona hai 😭"
    ]
};

// Picture generate karne ka function
async function getImageAndComment() {
    // 1. Ek random portrait uthao (0 se 99 tak)
    const randomId = Math.floor(Math.random() * 100); 
    const imageUrl = `https://randomuser.me/api/portraits/women/${randomId}.jpg`;

    // 2. Random category chuno
    const categories = Object.keys(comments);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    
    // 3. Us category se ek comment uthao
    const categoryComments = comments[randomCategory];
    const randomComment = categoryComments[Math.floor(Math.random() * categoryComments.length)];

    return { imageUrl, randomComment };
}

async function publishPost() {
    try {
        // Picture aur uske mutabiq comment nikalo
        const { imageUrl, randomComment } = await getImageAndComment();
        
        console.log("Posting Picture:", imageUrl);
        console.log("With Comment:", randomComment);

        // Facebook par post karo
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/photos`,
            {
                url: imageUrl,         
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

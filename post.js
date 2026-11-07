const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Comments categories
const comments = {
    makeup: [
        "Iska makeup toh kamaal ka hai 💄✨",
        "Itna highlighter lagaya hai ke face chamak raha hai ✨",
        "Contour kahan se seekha hai waise? 🤔",
        "Lipstick ka shade toh ekdum perfect hai 💋",
        "Naya look, nayi vibe 💅"
    ],
    expression: [
        "Yeh expression dekh ke toh meri hasi nahi ruk rahi 😂😂",
        "Kya acting hai waise! 🔥",
        "Iska expression toh ekdum 'Ammi ne daant di hai' wala hai 🤣",
        "Aankhon se hi sab keh diya isne 👀❤️",
        "Yeh look dekh ke toh mera din ban gaya 😍"
    ],
    cute: [
        "Kya cute lag rahi hai yaar! ❤️",
        "Aaj kal ki actresses toh ek se badh kar ek hain ✨",
        "Yeh style toh sabki favourite hai 💃",
        "Iska smile toh dil le gaya 😊",
        "Ekdum natural beauty hai yaar 🌸"
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

// 12 High-Quality HD Pictures (Drama actress style)
const hdPics = [
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1518577915332-c2a19f149a75?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524250502761-1ac6f2e30d43?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453?q=80&w=1080&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=1080&auto=format&fit=crop"
];

async function publishPost() {
    try {
        // 1. Random HD picture uthao
        const randomPic = hdPics[Math.floor(Math.random() * hdPics.length)];

        // 2. Random category aur comment uthao
        const categories = Object.keys(comments);
        const randomCategory = categories[Math.floor(Math.random() * categories.length)];
        const categoryComments = comments[randomCategory];
        const randomComment = categoryComments[Math.floor(Math.random() * categoryComments.length)];
        
        console.log("Posting HD Picture:", randomPic);
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

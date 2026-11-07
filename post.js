const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Comments jo portraits ke saath match karein
const comments = [
    "Yeh expression dekh ke toh meri hasi nahi ruk rahi 😂😂",
    "Kya acting hai waise! 🔥",
    "Iska style toh ekdum drama wali hai 💃",
    "Aankhon se hi sab keh diya isne 👀❤️",
    "Yeh look dekh ke toh mera din ban gaya 😍",
    "Kya cute lag rahi hai yaar! ❤️",
    "Ekdum natural beauty hai yaar 🌸",
    "Mashallah, kitni pyari lag rahi hain! 🥰",
    "Guys, yeh kaunsa drama hai? 😅",
    "Koi batao yeh actress kaun hai? 🤔",
    "Background music toh kamaal ka tha 🎵",
    "Iska makeup toh kamaal ka hai 💄✨"
];

async function publishPost() {
    try {
        // ✅ Unsplash Source API se random portrait image uthao
        // Yeh link har call par ek nayi image dega aur hotlink protected nahi hai
        const randomPic = "https://source.unsplash.com/1080x1080/?portrait,woman,actress";

        // Random comment select karo
        const randomComment = comments[Math.floor(Math.random() * comments.length)];
        
        console.log("Posting Picture:", randomPic);
        console.log("With Comment:", randomComment);

        // Facebook par post karo
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

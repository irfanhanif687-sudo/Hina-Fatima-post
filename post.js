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

// ✅ ASLI PAKISTANI ACTRESSES KI DIRECT HD IMAGE LINKS (Pak101.com se)
// (dot) ko . mein badal diya gaya hai taake Facebook accept kare
const dramaActressPics = [
    "https://www.pak101.com/gallery/ActressesTv/Ayesha_Gul/2014/8/8/Ayesha_Gul_Pakistani_Female_Television_Drama_Actress_Celebrity_14_cdrqc_Pak101.com.jpg",
    "https://www.pak101.com/gallery/ActressesTv/Sana_Javed/2018/10/24/Sana_Javed_Pakistani_Female_Model_and_Television_Drama_Actress_17_lsdqe_Pak101.com.jpg",
    "https://www.pak101.com/gallery/ActressesTv/Anmol_Baloch/2018/7/27/Anmol_Baloch_Pakistani_Television_Drama_Actress_And_Host_Celebrity_19_wcfax_Pak101.com.jpg",
    // Aap yahan aur bhi actresses ke links add kar sakte hain
];

async function publishPost() {
    try {
        const randomPic = dramaActressPics[Math.floor(Math.random() * dramaActressPics.length)];

        const categories = Object.keys(comments);
        const randomCategory = categories[Math.floor(Math.random() * categories.length)];
        const categoryComments = comments[randomCategory];
        const randomComment = categoryComments[Math.floor(Math.random() * categoryComments.length)];
        
        console.log("Posting Actress Picture:", randomPic);
        console.log("With Comment:", randomComment);

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

const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

console.log("Token shuru ke 10 characters:", TOKEN ? TOKEN.substring(0, 10) : "Token nahi mila");
console.log("Page ID:", PAGE_ID);

const postContent = {
    message: "Assalam o Alaikum! Yeh mera automatic post hai. 😂 #PakistaniDrama"
};

async function publishPost() {
    try {
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/feed`,
            postContent,
            {
                params: { access_token: TOKEN }
            }
        );
        console.log("✅ POST SUCCESSFUL! ID:", response.data.id);
    } catch (error) {
        console.log("❌ ERROR AAGAYA BHAI:");
        if (error.response) {
            console.log(JSON.stringify(error.response.data, null, 2));
        } else {
            console.log(error.message);
        }
        process.exit(1);
    }
}

publishPost();

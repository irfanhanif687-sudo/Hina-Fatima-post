const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Yahan apni post ka content likho
const postContent = {
    message: "Assalam o Alaikum! Yeh mera pehla automatic post hai. 😂 #PakistaniDrama"
};

async function publishPost() {
    console.log("Post karni ki koshish kar rahe hain...");
    
    try {
        const response = await axios.post(
            `https://graph.facebook.com/v20.0/${PAGE_ID}/feed`,
            postContent,
            {
                params: { access_token: TOKEN }
            }
        );
        console.log("✅ Post Successful! Post ID:", response.data.id);
    } catch (error) {
        console.error("❌ Facebook API Error:");
        if (error.response) {
            console.error(JSON.stringify(error.response.data, null, 2));
        } else {
            console.error(error.message);
        }
        process.exit(1);
    }
}

publishPost();

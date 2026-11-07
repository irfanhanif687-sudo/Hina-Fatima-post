const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_TOKEN;

// Yahan apna content set karo. 
// Filhal test ke liye text post hai:
const postContent = {
    message: "Assalam o Alaikum dosto! Yeh mera pehla auto-post hai GitHub se. 😂 #PakistaniDrama #Funny"
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
        console.log("Post successful! Post ID:", response.data.id);
    } catch (error) {
        console.error("Error aagaya bhai:", error.response ? error.response.data : error.message);
        process.exit(1);
    }
}

publishPost();

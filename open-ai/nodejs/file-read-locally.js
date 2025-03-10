import OpenAI from "openai";
import fs from "fs";

const openai = new OpenAI({
    apiKey: process.env.apiKey
})

async function uploadFile() {
    try {
        const file = await openai.files.create({
            file: fs.createReadStream("/Downloads/test1.pdf"), // File from local system
            purpose: "assistants"
        });

        console.log("File uploaded:", file);
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}

uploadFile();
